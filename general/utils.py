import logging
import six
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import Http404
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import set_rollback

logger = logging.getLogger(__name__)


class ServiceUnavailable(exceptions.APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


def render_mail(subject, email, context, template_name):
    """
    Renders an e-mail to `email`.  `template_prefix` identifies the
    e-mail that is to be sent, e.g. "account/email/email_confirmation"
    """
    try:
        bodies = render_to_string(template_name, context).strip()
    except TemplateDoesNotExist:
        raise
    msg = EmailMessage(subject, bodies, settings.DEFAULT_FROM_EMAIL, [email])
    msg.content_subtype = 'html'  # Main content is now text/html
    return msg


def custom_exception_handler(exc, context):

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, dict):
            data = parse_exc_details(exc.detail)
            data = {'errors': data}
        elif isinstance(exc.detail, list):
            if isinstance(exc.detail[0], dict):
                data = []
                for exc_detail in exc.detail:
                    data.append(parse_exc_details(exc_detail))
            else:
                data = {'message': exc.detail[0]}
        else:
            data = {'message': exc.detail}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    elif isinstance(exc, Http404) or isinstance(exc, NotFound):
        msg = _('Not found.')
        data = {'message': msg}

        set_rollback()
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, PermissionDenied):
        msg = _('Permission denied.')
        data = {'message': six.text_type(msg)}

        set_rollback()
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    # Note: Unhandled exceptions will raise a 500 error.
    return None


def parse_exc_details(detail):
    def trim_nest_errors(errors_list):
        errors_list = [i for i in errors_list if i]
        result = []
        for opt_dict in errors_list:
            result.append(parse_exc_details(opt_dict))
        return result
    results = []
    for key, value in detail.items():
        result = {'field': key}
        if isinstance(value, list) and isinstance(value[0], dict):
            result['errors'] = trim_nest_errors(value)
        elif isinstance(value, list):
            result['message'] = value[0]
            result['code'] = value[0].code
        elif isinstance(value, dict):
            # previous version
            result = {**result, **value}
        results.append(result)
    return results
