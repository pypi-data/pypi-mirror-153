from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response

from djangoldp.models import Model
from djangoldp.serializers import LDPSerializer
from djangoldp.views import LDPViewSet
from djangoldp.pagination import LDPPagination
import logging


logger = logging.getLogger('djangoldp')


class LDPNotificationsPagination(LDPPagination):
    default_limit = 80


def filter_object_is_permitted(recipient, data):
        '''
        applies filter on passed object data
        returns True if the object is permitted, False if not
        '''
        obj = data['object']

        # if a str (urlid) is given then no filtering is to be applied
        if isinstance(obj, str):
            return True

        # the type must be given for a filter to be resolved successfully
        if not '@type' in obj or obj['@type'] is None:
            logger.error('djangoldp_notification filter ERR in object serialization. received ' + str(obj) + ' without serialized type to identify model. Please include the @type in your serialization')
            return False

        object_model = Model.get_subclass_with_rdf_type(obj['@type'])

        if object_model is None:
            logger.error('djangoldp_notification filter ERR in object serialization. Cannot resolve type given ' + str(obj['type']))
            return False
        
        if not hasattr(object_model, 'permit_notification'):
            logger.error('djangoldp_notification filter ERR. Resolved type ' + str(obj['@type']) + ' but this Model did not have the required function permit_notification defined on it')
            return False

        return object_model.permit_notification(recipient, data)


class LDPNotificationsViewSet(LDPViewSet):
    '''overridden LDPViewSet to force pagination'''
    pagination_class = LDPNotificationsPagination
    depth = 0
