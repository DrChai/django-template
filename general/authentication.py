import logging

from rest_framework.authentication import SessionAuthentication, CSRFCheck
from rest_framework import exceptions

logger = logging.getLogger(__name__)


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):

        return

        # reason = CSRFCheck().process_view(request, None, (), {})
        # if reason:
        #     logger.warning('CsrfExemptSessionAuthentication', extra={'stack': True, })
        #     # CSRF failed, bail with explicit error message
        #     raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)