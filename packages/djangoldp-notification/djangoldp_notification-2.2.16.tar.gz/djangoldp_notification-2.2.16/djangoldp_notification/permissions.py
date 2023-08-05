from django.contrib.auth import get_user_model

from djangoldp.permissions import LDPPermissions
from djangoldp_notification.filters import InboxFilterBackend, SubscriptionsFilterBackend
from rest_framework.reverse import reverse


class InboxPermissions(LDPPermissions):
    filter_backends = [InboxFilterBackend]


class SubscriptionsPermissions(LDPPermissions):
    filter_backends = [SubscriptionsFilterBackend]

    def has_permission(self, request, view):
        if request.user.is_anonymous and not request.method == "OPTIONS":
            return False

        if request.method in ["GET", "PATCH", "DELETE", "PUT"]:
            return True

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous and not request.method == "OPTIONS":
            return False

        reverse_path_key = "{}-notification-list".format(get_user_model()._meta.object_name.lower())
        user_inbox = reverse(reverse_path_key, kwargs={"slug": request.user.slug}, request=request)
        if obj.inbox == user_inbox:
            return True

        return False
