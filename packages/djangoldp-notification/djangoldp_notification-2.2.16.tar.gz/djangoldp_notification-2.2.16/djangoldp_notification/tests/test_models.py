import uuid
from rest_framework.test import APITestCase, APIClient

from djangoldp_account.models import LDPUser
from djangoldp_notification.models import Subscription


class TestModel(APITestCase):
    circle_user1_url = "http://localhost:8000/circles/1/"
    circle_user2_url = "http://localhost:8000/circles/2/"

    def _get_random_user(self):
        return LDPUser.objects.create(email='{}@test.co.uk'.format(str(uuid.uuid4())), first_name='Test',
                                      last_name='Test', username=str(uuid.uuid4()))

    def _auth_as_user(self, user):
        self.client.force_authenticate(user=user)

    def setUpLoggedInUser(self):
        self.user = self._get_random_user()
        self._auth_as_user(self.user)

    def setUp(self):
        self.client = APIClient()

        self.user1 = self._get_random_user()
        Subscription.objects.create(object=self.circle_user1_url, inbox="http://testserver/users/karl_marx/inbox/")

        self.user2 = self._get_random_user()
        Subscription.objects.create(object=self.circle_user2_url,
                                    inbox="http://testserver/users/piotr_kropotkine/inbox/")

    def test_not_logged_fails(self):
        response = self.client.get("/subscriptions/")
        self.assertEqual(response.status_code, 403)

    def test_logged_in_succeeds(self):
        self._auth_as_user(self.user2)
        response = self.client.get("/subscriptions/").data.get("ldp:contains")
        self.assertEqual(len(response), 2)
        response = response[1]
        self.assertEqual(response["object"], self.circle_user2_url)
        self.assertEqual(response["inbox"], "http://testserver/users/piotr_kropotkine/inbox/")
        self.assertIn({'mode': {'@type': 'view'}}, response["permissions"])
        self.assertIn({'mode': {'@type': 'delete'}}, response["permissions"])
