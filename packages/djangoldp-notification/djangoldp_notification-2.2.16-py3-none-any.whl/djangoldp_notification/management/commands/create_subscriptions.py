from django.core.management.base import BaseCommand
from django.conf import settings
from djangoldp_notification.models import Subscription

class Command(BaseCommand):
  help = 'Create required subscriptions'

  def handle(self, *args, **options):
    host = getattr(settings, 'SITE_URL')
    jabber_host = getattr(settings, 'JABBER_DEFAULT_HOST')
    xmpp = getattr(settings, 'PROSODY_HTTP_URL')

    try:
        sub = Subscription.objects.get(object="{}/circles/".format(host))
        sub.delete()
    except Subscription.DoesNotExist:
        pass

    try:
        sub = Subscription.objects.get(object="{}/projects/".format(host))
        sub.delete()
    except Subscription.DoesNotExist:
        pass

    try:
        sub = Subscription.objects.get(object="{}/circle-members/".format(host))
        sub.delete()
    except Subscription.DoesNotExist:
        pass

    try:
        sub = Subscription.objects.get(object="{}/project-members/".format(host))
        sub.delete()
    except Subscription.DoesNotExist:
        pass

    Subscription.objects.get_or_create(object=host+"/circles/", inbox=xmpp + "/conference." + jabber_host + "/startinblox_muc_admin", field=None)
    Subscription.objects.get_or_create(object=host+"/projects/", inbox=xmpp + "/conference." + jabber_host + "/startinblox_muc_admin", field=None)
    
    Subscription.objects.get_or_create(object=host+"/users/", inbox=xmpp + "/" + jabber_host + "/happydev_user_admin", field=None)
    Subscription.objects.get_or_create(object=host+"/profiles/", inbox=xmpp + "/" + jabber_host + "/happydev_user_admin", field="user")
    Subscription.objects.get_or_create(object=host+"/chatprofiles/", inbox=xmpp + "/" + jabber_host + "/happydev_user_admin", field="user")
    Subscription.objects.get_or_create(object=host+"/accounts/", inbox=xmpp + "/" + jabber_host + "/happydev_user_admin", field="user")

    Subscription.objects.get_or_create(object=host+"/circle-members/", inbox=xmpp + "/conference." + jabber_host + "/startinblox_muc_members_admin", field=None)
    Subscription.objects.get_or_create(object=host+"/project-members/", inbox=xmpp + "/conference." + jabber_host + "/startinblox_muc_members_admin", field=None)

    self.stdout.write(self.style.SUCCESS("Successfully  created subscriptions\nhost: "+host+"\nxmpp server: "+xmpp+"\njabber host: "+jabber_host))
