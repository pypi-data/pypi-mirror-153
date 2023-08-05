import uuid
import json
from rest_framework.test import APITestCase, APIClient

from django.conf import settings
from djangoldp.models import Model
from djangoldp.serializers import GLOBAL_SERIALIZER_CACHE
from djangoldp_account.models import LDPUser
from djangoldp_notification.models import Notification


class TestSubscription(APITestCase):
    def _get_random_user(self):
        return LDPUser.objects.create(email='{}@test.co.uk'.format(str(uuid.uuid4())), first_name='Test',
                                      last_name='Test', username=str(uuid.uuid4()))

    def _get_random_notification(self, recipient, author):
        return Notification.objects.create(user=recipient, author=author.urlid, object=author.urlid,
                                           unread=True)

    def setUpLoggedInUser(self):
        self.user = self._get_random_user()
        self.client.force_authenticate(user=self.user)

    def setUp(self):
        self.client = APIClient()

    def test_indirect_cache(self):
        self.setUpLoggedInUser()
        author_user = self._get_random_user()
        notification = self._get_random_notification(recipient=self.user, author=author_user)
        self.assertEqual(notification.unread, True)

        # GET the inbox - should set the cache
        response = self.client.get("/users/{}/inbox/".format(self.user.username))
        self.assertEqual(response.status_code, 200)
        notif_serialized = response.data["ldp:contains"][0]
        self.assertEqual(notif_serialized["unread"], True)

        # PATCH the notification - should wipe the cache
        patch = {
            "unread": False,
            "@context": {
                "@vocab":"http://happy-dev.fr/owl/#",
                "unread": "http://happy-dev.fr/owl/#unread"
            }
        }
        response = self.client.patch("/notifications/{}/".format(notification.pk), data=json.dumps(patch),
                                     content_type="application/ld+json")
        notif_obj = Notification.objects.get(pk=notification.pk)
        self.assertEqual(notif_obj.unread, False)

        # GET the inbox - should now be read
        response = self.client.get("/users/{}/inbox/".format(self.user.username))
        self.assertEqual(response.status_code, 200)
        notif_serialized = response.data["ldp:contains"][0]
        self.assertEqual(notif_serialized["unread"], False)

    # NOTE: this would be our ideal cache behaviour
    # the functionality for optimising it was removed because of an issue with extensibility
    #  https://git.startinblox.com/djangoldp-packages/djangoldp-notification/merge_requests/42#note_58559
    '''def test_custom_cache_clear(self):
        # going to create two notifications in two different inboxes
        self.setUpLoggedInUser()
        other_user = self._get_random_user()
        notification = self._get_random_notification(recipient=self.user, author=other_user)
        notification2 = self._get_random_notification(recipient=other_user, author=self.user)

        # GET the inboxes and asser that the cache is set for both
        self.client.get("/users/{}/inbox/".format(self.user.username))
        self.client.get("/users/{}/inbox/".format(other_user.username))

        # assert cache is set
        my_container_urlid = '{}/users/{}/inbox/'.format(settings.SITE_URL, self.user.username)
        their_container_urlid = '{}/users/{}/inbox/'.format(settings.SITE_URL, other_user.username)

        self.assertTrue(GLOBAL_SERIALIZER_CACHE.has(Model.get_meta(Notification, 'label'), my_container_urlid))
        self.assertTrue(GLOBAL_SERIALIZER_CACHE.has(Model.get_meta(Notification, 'label'), their_container_urlid))

        # save my notification - should wipe the cache for my inbox...
        notification.unread = False
        notification.save()
        self.assertFalse(GLOBAL_SERIALIZER_CACHE.has(Model.get_meta(Notification, 'label'), my_container_urlid))

        # ...but not for theirs
        self.assertTrue(GLOBAL_SERIALIZER_CACHE.has(Model.get_meta(Notification, 'label'), their_container_urlid))'''
