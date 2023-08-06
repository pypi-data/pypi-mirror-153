from wsgidav.dc.base_dc import BaseDomainController  # type: ignore

from .deps import extract_permission


class JWTDomainController(BaseDomainController):
    def get_domain_realm(self, path_info, environ):
        """Resolve a relative url to the appropriate realm name."""
        realm = self._calc_realm_from_path_provider(path_info, environ)
        # This solves a bug in send_basic_auth_response in HTTPAuthenticator
        # where it tries to concatenate realm to a string and fails if
        # it's None
        return realm if realm is not None else "None"

    def require_authentication(self, realm, environ):
        """Return True if this realm requires authentication."""
        return True

    def basic_auth_user(self, realm, user_name, password, environ):
        """Returns True if this user_name/password pair is valid for the 
        realm, False otherwise. Used for basic authentication."""
        try:
            permission = extract_permission(user_name)
            roles = ()
            permissions = ()
            if permission.read_access is True:
                roles = ("reader",)
                permissions = ("browse_dir",)
            if permission.write_access is True:
                roles = ("admin", "editor", "reader")
                permissions = (
                    "browse_dir",
                    "delete_resource",
                    "edit_resource",
                )
            environ["wsgidav.auth.roles"] = roles
            environ["wsgidav.auth.permissions"] = permissions
            return (
                permission.read_access is True
                or permission.write_access is True
            )
        except Exception as e:
            print(e)
            return False

    def supports_http_digest_auth(self):
        return False
