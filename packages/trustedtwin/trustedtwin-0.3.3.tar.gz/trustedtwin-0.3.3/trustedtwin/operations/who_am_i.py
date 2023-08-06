"""Definition of who_am_i operation"""
from typing import TYPE_CHECKING, Dict

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


def who_am_i(service: "RestService") -> Dict:
    """Execute who_am_i API operation"""
    endpoint = "whoami"

    resp = service.http_client.execute_request(
        method=RESTMethod.GET,
        url_root=service.http_client.host_name,
        endpoint=endpoint,
    )

    return process_response(resp, "who_am_i")
