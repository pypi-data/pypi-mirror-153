from django.db.models import signals


MODEL_MODIFICATION_USER_FIELD = 'modification_user'


class CurrentUserMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        signals.pre_save.disconnect(dispatch_uid=request)
        signals.pre_delete.disconnect(dispatch_uid=request)
        return response

    def process_request(self, request):
        if request.method in ('GET', 'HEAD', 'OPTION'):
            # this request shouldn't update anything
            # so no signal handler should be attached
            return

        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user
        else:
            user = None

        def _update_users(sender, instance, **kwargs):
            if(type(instance).__name__ != "ScheduledActivity" and type(instance).__name__ != "LogEntry" and type(instance).__name__ != "Activity"):
                setattr(instance, MODEL_MODIFICATION_USER_FIELD, user)

        signals.pre_save.connect(_update_users, dispatch_uid=request, weak=False)
        signals.pre_delete.connect(_update_users, dispatch_uid=request, weak=False)
