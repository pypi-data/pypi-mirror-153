from django.apps import apps
from django.conf import settings
from django.db import models
from djangoldp.models import Model
from djangoldp_notification.models import send_request, Subscription
from djangoldp_notification.middlewares import MODEL_MODIFICATION_USER_FIELD

class technical_user:
  urlid = settings.BASE_URL

def add_arguments(parser):
  parser.add_argument(
    "--ignore-subscriptions",
    default=False,
    nargs="?",
    const=True,
    help="Ignore subscriptions related check",
  )
  parser.add_argument(
    "--send-subscription-notifications",
    default=False,
    nargs="?",
    const=True,
    help="Send an update notification for every local resources to every subscribers",
  )

def check_integrity(options):
  print('---')
  print("DjangoLDP Notification")
  if(not options["ignore_subscriptions"]):

    models_list = apps.get_models()

    resources = set()
    resources_map = dict()

    for model in models_list:
      for obj in model.objects.all():
        if hasattr(obj, "urlid"):
          if(obj.urlid):
            if(obj.urlid.startswith(settings.BASE_URL)):
              if(type(obj).__name__ != "ScheduledActivity" and type(obj).__name__ != "LogEntry" and type(obj).__name__ != "Activity"):
                resources.add(obj.urlid)
                resources_map[obj.urlid] = obj
    
    print("Found "+str(len(resources_map))+" local resources on "+str(len(models_list))+" models for "+str(Subscription.objects.count())+" subscribers")

    if(options["send_subscription_notifications"]):
      sent=0
      for resource in sorted(resources):
        resource = resources_map[resource]
        recipients = []
        try:
          url_container = settings.BASE_URL + Model.container_id(resource)
          url_resource = settings.BASE_URL + Model.resource_id(resource)
        except NoReverseMatch:
          continue
        for subscription in Subscription.objects.filter(models.Q(object=url_resource) | models.Q(object=url_container)):
          if subscription.inbox not in recipients and not subscription.is_backlink:
            # I may have configured to send the subscription to a foreign key
            if subscription.field is not None and len(subscription.field) > 1:
              try:
                resource = getattr(resource, subscription.field, resource)

                # don't send notifications for foreign resources
                if hasattr(resource, 'urlid') and Model.is_external(resource.urlid):
                    continue

                url_resource = settings.BASE_URL + Model.resource_id(resource)
              except NoReverseMatch:
                continue
              except ObjectDoesNotExist:
                continue
            setattr(resource, MODEL_MODIFICATION_USER_FIELD, technical_user)
            try:
              send_request(subscription.inbox, url_resource, resource, False)
              sent+=1
            except:
              print("Failed to create subscription activity for "+url_resource)
            recipients.append(subscription.inbox)
      print("Sent "+str(sent)+" activities to "+str(Subscription.objects.count())+" subscribers")
      print("Depending on your server configuration, you may have to restart the ActivityQueue or the server to properly process em.")
    else:
      print("Send an update notification for all those resources to all of their subscribers with  `./manage.py check_integrity --send-subscription-notifications`")
  else:
    print("Ignoring djangoldp-notification checks")