import asyncio
from typing import Dict, List
from uuid import UUID

from asyncblink import signal  # type: ignore
from fastapi.logger import logger
from watchdog.observers.api import ObservedWatch  # type: ignore
from wsgidav.wsgidav_app import WsgiDAVApp  # type: ignore

from .settings import settings
from .signals import WATCHDOG_FILE_SYSTEM_EVENT

try:
    if not settings.WATCHDOG_ENABLED:
        raise ImportError("settings.WATCHDOG_ENABLED is False")
    from watchdog.events import FileSystemEvent  # type: ignore
    from watchdog.events import PatternMatchingEventHandler
    from watchdog.observers import Observer  # type: ignore

    has_watchdog = True
    logger.debug("Successfully loaded watchdog.")
except ImportError as e:
    has_watchdog = False
    logger.debug(f"Watchdog disabled.  Failed to import - {e}")


if has_watchdog:

    async def send_watchdog_event(event: FileSystemEvent):
        signal(WATCHDOG_FILE_SYSTEM_EVENT).send(
            event_type=event.event_type,
            src_path=event.src_path,
            dest_path=getattr(event, "dest_path", None),
        )

    class D1FileSystemEventHandler(PatternMatchingEventHandler):
        def __init__(self, loop, *args, **kwargs):
            self.loop = loop
            super().__init__(*args, **kwargs)

        def on_any_event(self, event: FileSystemEvent):
            asyncio.run_coroutine_threadsafe(
                send_watchdog_event(event), self.loop,
            )

    class WatchdogManager:
        def __init__(self, loop):
            self.watches: Dict[str, ObservedWatch] = {}
            self.observer = Observer()
            self.event_handler = D1FileSystemEventHandler(
                loop, ignore_patterns=settings.WATCHDOG_IGNORE_PATTERNS
            )

        def start_watchdog(self):
            if not self.observer.is_alive():
                self.observer.schedule(
                    self.event_handler, settings.ROOT_DIR, recursive=True
                )
                self.observer.start()

        def stop_watchdog(self):
            self.observer.stop()

        def schedule(self, directory: str):
            watch = self.observer.schedule(
                self.event_handler, directory, recursive=True
            )
            self.watches[directory] = watch

        def unschedule(self, directory: str):
            watch = self.watches.pop(directory, None)
            if watch:
                self.observer.unschedule(watch)

    def create_watchdog(loop):
        return WatchdogManager(loop)


else:

    def create_watchdog(loop):
        return None


class D1WsgiDAVApp(WsgiDAVApp):
    def remove_providers(self, shares: List[str]):
        for share in shares:
            self.provider_map.pop(share, None)

        # Store the list of share paths, ordered by length, so route lookups
        # will return the most specific match
        self.sorted_share_list = [s.lower() for s in self.provider_map.keys()]
        self.sorted_share_list = sorted(
            self.sorted_share_list, key=len, reverse=True
        )


dav = D1WsgiDAVApp(settings.DAV_SETTINGS)


def format_share(directory: str) -> str:
    return "/" + directory.lower().strip("/")


class DAVManager:
    def __init__(self):
        # Dict of shares used by notebooks (excluding the D1 working
        # directory and any default shares that wsgi_dav provides).
        # A share is just a route exposed by wsgi_dav,
        # i.e. "/tmp/docs" is the share for the /tmp/docs directory, where
        # https://host/dav/tmp/docs is its dav url
        self.nb_to_directory: Dict[UUID, str] = {}
        self.root_share = format_share(settings.ROOT_DIR)
        self.watchdog_manager = None

    def start_watchdog(self, loop):
        if self.watchdog_manager is None:
            watchdog_manager = create_watchdog(loop)
            if watchdog_manager:
                watchdog_manager.start_watchdog()
            self.watchdog_manager = watchdog_manager

    def stop_watchdog(self):
        if self.watchdog_manager:
            self.watchdog_manager.stop_watchdog()
            self.watchdog_manager = None

    def add_provider(self, directory: str, uuid: UUID) -> None:
        self.nb_to_directory[uuid] = directory
        self.update_providers()

    def remove_provider(self, uuid: UUID) -> None:
        self.nb_to_directory.pop(uuid, None)
        self.update_providers()

    def clear_providers(self) -> None:
        self.nb_to_directory = {}
        self.update_providers()

    def update_providers(self):
        """
        Iterate through working directories for all open notebooks in order
        of length and find the resolved dav providers. If the provider is
        for a less specific directory the first time a provider is resolved
        to, then the provider should be replaced with a more specific
        provider. If a provider is never resolved to, remove it.
        If a provider is not found for a directory, add a provider for that
        directory. The nb_to_directory dict should reflect the desired state
        before this method is called.
        """

        # Order directories by ascending length so that shares that are too
        # general will be caught first
        directories = [s.lower() for s in self.nb_to_directory.values()]
        directories = sorted(directories, key=len, reverse=False)
        used_shares = set()
        unused_shares = set()
        add_shares = set()

        for directory in directories:
            # Check if an existing provider contains the required directory
            dav_share, _ = dav.resolve_provider(directory.lower())
            if dav_share is not None:
                # if the share is the root dir share, do nothing
                if dav_share == self.root_share:
                    continue
                if dav_share not in used_shares and len(dav_share) < len(
                    directory
                ):
                    # share needs to be more specific, so mark it
                    # for replacement
                    unused_shares.add(dav_share)
                    add_shares.add(directory)
                else:
                    # share found, add to list of used shares
                    used_shares.add(dav_share)
            else:
                # share not found, add to list of provider to add
                add_shares.add(directory)

        # Get unused shares
        for share in dav.sorted_share_list:
            if share == self.root_share:
                continue
            if share not in used_shares:
                unused_shares.add(share)
            # check if any shares being added can replace an old share
            for add_share in add_shares:
                if share.lower().startswith(add_share + "/"):
                    unused_shares.add(share)

        if len(unused_shares) > 0:
            dav.remove_providers(unused_shares)
        if self.watchdog_manager:
            for share in unused_shares:
                self.watchdog_manager.unschedule(share)

        for directory in add_shares:
            formatted_share = format_share(directory)
            dav.add_provider(formatted_share, directory)
            if self.watchdog_manager:
                self.watchdog_manager.schedule(directory)


dav_manager = DAVManager()
