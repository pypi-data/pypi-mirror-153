import datetime
from contextlib import contextmanager
from typing import Dict, Optional

import OpenSSL
from django.urls import reverse
from django_etna.auth.legacy_auth import make_etna_token
from django.http import HttpResponse
from django.conf import settings


"""
This file contains utilities useful when unit-testing authentication
and authorization.
"""


class IdentityMixin:
    """Provide test case helper methods to mock client identity and
    test response status (w/ regard to identity).
    """

    @contextmanager
    def auth_identity(self, identity:Dict, key:Optional[OpenSSL.crypto.PKey] = None):
        "Mock beeing logged in with a raw identity dict. Consider using self.auth_user instead."
        try:
            token = make_etna_token(identity, key)
            self.client.cookies['authenticator'] = token
            yield None
        finally:
            del self.client.cookies['authenticator']

    def auth_user(self, user_id=1, login="moulin_e", email="edouard.moulin@etna.io", roles=[]):
        "Mock beeing logged in with given `user`."
        identity = {
            "id": user_id,
            "login": login,
            "email": email,
            "logas": False,
            "groups": roles,
            "login_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        return self.auth_identity(identity)


    def auth_roles(self, *roles):
        "Mock beeing logged in with a user having *only* given `roles`."
        return self.auth_user(roles=roles)


    def assertRedirectToLogin(self, response:HttpResponse, next_url=None):
        """Fail if response does not redirect to the login page.
        Optionnaly ensure the next? query arg is set to given `next_url`
        """
        self.assertEqual(response.status_code, 302)
        location = response.get('Location')
        wanted_redirect = settings.LOGIN_URL + '?next='
        if next_url is not None:
            self.assertEqual(location, wanted_redirect + next_url)
        else:
            self.assertTrue(location.startsWith(wanted_redirect))
