import uuid
import json

from django.conf import settings
from rest_framework.test import APITestCase, APIClient

from djangoldp_account.models import LDPUser
from djangoldp_notification.models import Notification, Subscription


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def _get_random_user(self):
        return LDPUser.objects.create(email='{}@test.co.uk'.format(str(uuid.uuid4())), first_name='Test',
                                      last_name='Test', username=str(uuid.uuid4()))

    def _auth_as_user(self, user):
        self.client.force_authenticate(user=user)

    def setUpLoggedInUser(self):
        self.user = self._get_random_user()
        self._auth_as_user(self.user)

    def test_can_subscribe_to_container(self):
        self.setUpLoggedInUser()

        users_container = "{}/users/".format(settings.SITE_URL)
        Subscription.objects.create(object=users_container, inbox=self.user.urlid + "inbox/")
        self.assertEqual(self.user.inbox.count(), 0)

        self._get_random_user()
        self.assertEqual(self.user.inbox.count(), 2)
        notification = self.user.inbox.all()[0]
        self.assertTrue(notification.object, users_container)
