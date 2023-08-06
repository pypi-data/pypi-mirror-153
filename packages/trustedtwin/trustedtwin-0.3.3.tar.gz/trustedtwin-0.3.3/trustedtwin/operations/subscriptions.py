"""Definition of Subscriptions access methods."""
import urllib.parse
from typing import TYPE_CHECKING, Dict, Any

from trustedtwin.misc import RESTMethod
from trustedtwin.models.responses import process_response

if TYPE_CHECKING:
    from trustedtwin.service import RestService


class SubscriptionsOperations:
    """Interfaces for accessing Subscriptions API operations"""

    def __init__(self, service: "RestService"):
        """Initialize object"""
        self._service = service
        self._http_client = self._service.http_client

    def webhook_subscribe(self, **kwargs: Any) -> Dict:
        """Subscribe to webhook"""
        endpoint = "notifications/webhooks/subscribe"
        endpoint = urllib.parse.quote(endpoint)

        body = {
            "callback_url": kwargs.get("callback_url"),
            "topic": kwargs.get("callback_url"),
            "user_secret": kwargs.get("user_secret"),
            "expires": kwargs.get("expires"),
        }
        body = {x: y for x, y in body.items() if y}

        resp = self._http_client.execute_request(
            method=RESTMethod.POST,
            url_root=self._http_client.host_name,
            endpoint=endpoint,
            body=body,
        )

        return process_response(resp, "webhookSubscribe", **self._service.kwargs)

    def webhook_unsubscribe(self) -> Dict:
        pass

    def webhook_refresh(self) -> Dict:
        pass

    def webhook_confirm(self) -> Dict:
        pass
