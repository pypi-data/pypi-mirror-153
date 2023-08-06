from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def any_role_required(*roles, login_url=None, raise_exception=True):
    """
    Decorator for views that checks whether a user has any of the given roles
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    # implementation is based on django's permission_required decorator.
    def check_perms(user):
        has_role = getattr(user, 'has_role', None)
        if callable(has_role) and any(has_role(r) for r in roles):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False

    return user_passes_test(check_perms, login_url=login_url)
