from django.db import models

class UserMixin:
    """Defines helper methods to access legacy identity json object.
    """

    identity = {}
    
    def has_perm(self, perm, obj=None):
        return perm in self.identity.get('groups', ())

    def has_role(self, role):
        return role in self.identity.get('groups', ())

    @property
    def etna_user_id(self):
        return int(self.identity['id'])

    @property
    def etna_login(self):
        return int(self.identity['login'])


class AbstractBaseUser(models.Model, UserMixin):
    "Based on django's AbstractBaseUser"
    #last_login = models.DateTimeField(_("last login"), blank=True, null=True)
    is_active = True

    REQUIRED_FIELDS = []

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_username()

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    def natural_key(self):
        return (self.get_username(),)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True


