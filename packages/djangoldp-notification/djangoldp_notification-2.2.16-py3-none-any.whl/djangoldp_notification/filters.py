from djangoldp.filters import LDPPermissionsFilterBackend


class InboxFilterBackend(LDPPermissionsFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if not request.user.is_anonymous:
            return queryset.filter(user=request.user)
        else:
            from djangoldp_notification.models import Notification
            return Notification.objects.none()


class SubscriptionsFilterBackend(LDPPermissionsFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.method == "OPTIONS":
            return queryset
        else:
            return super().filter_queryset(request, queryset, view)
