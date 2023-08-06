from uuid import UUID

import jupyter_client  # type: ignore
from fastapi import APIRouter, Depends, status

from ..deps import write_access
from ..models.kernel import KernelIsAlive, KernelsIdle
from ..models.kernel_spec import KernelSpec, KernelSpecsWrapper
from ..storage import kmanager, manager

router = APIRouter()
kspec = jupyter_client.kernelspec.KernelSpecManager()


@router.get("/specs", response_model=KernelSpecsWrapper)
async def list_kernel_specs():
    "Return a list of all kernel specs available on the server."
    kspecs = kspec.get_all_specs()
    specs = []
    for key in kspecs.keys():
        tmp_spec = kspecs[key]
        tmp_spec["kernel_name"] = key
        new_spec = KernelSpec(**tmp_spec)
        specs.append(new_spec)
    return KernelSpecsWrapper(kernel_specs=specs)


@router.get(
    "/shutdown/{uuid}",
    dependencies=[Depends(write_access)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def shutdown_kernel(uuid: UUID):
    "Shutdown the kernel identified by the uuid"
    await kmanager.shutdown_kernel(uuid)


@router.get(
    "/restart/{uuid}",
    dependencies=[Depends(write_access)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def restart_kernel(uuid: UUID):
    "Restart the kernel identified by the uuid"
    await kmanager.restart_kernel(uuid)


@router.get(
    "/interrupt/{uuid}",
    dependencies=[Depends(write_access)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def interrupt_kernel(uuid: UUID):
    "Interrupt the kernel identified by the uuid"
    await kmanager.interrupt_kernel(uuid)


@router.get("/is_alive/{uuid}", response_model=KernelIsAlive)
async def kernel_is_alive(uuid: str, status_code=status.HTTP_204_NO_CONTENT):
    "Check that kernel process is running."
    is_alive = kmanager.kernel_is_alive(uuid)
    return KernelIsAlive(kernel_is_alive=is_alive, kernel_id=uuid)


@router.get(
    "/idle", status_code=status.HTTP_200_OK, response_model=KernelsIdle
)
def idle_status():
    "Check if all kernels are idle"
    return KernelsIdle(idle=manager.is_idle(), last_idle=manager.last_idle)
