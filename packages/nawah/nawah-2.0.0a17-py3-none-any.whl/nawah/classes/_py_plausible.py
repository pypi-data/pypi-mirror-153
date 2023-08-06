from dataclasses import dataclass
from typing import Any, MutableMapping, Optional

import requests


class UrlNotSetException(Exception):
    pass


class UserAgentNotSetException(Exception):
    pass


class ForwardedNotSetException(Exception):
    pass


class EventRequestException(Exception):
    pass


# lyh1UwLGd5XVgsuTe4zDNVwXshlifHAEfP_dy6KEIA9W2Ur7sBVe4PSHMmTEMmab


@dataclass(kw_only=True)
class Plausible:

    host: str
    app_domain: str
    ssl: bool = True
    default_url: Optional[str] = None
    default_user_agent: Optional[str] = None
    default_forwarded: Optional[str] = None

    def register_event(
        self,
        *,
        name='pageview',
        url: str = None,
        user_agent: str = None,
        forwarded: str = None,
        screen_width: str = None,
        props: MutableMapping[str, Any] = None,
    ):
        if not (url or self.default_url):
            raise UrlNotSetException()

        if not (user_agent or self.default_user_agent):
            raise UserAgentNotSetException()

        if not (forwarded or self.default_forwarded):
            raise ForwardedNotSetException()

        api_uri = f'http{"s" if self.ssl else ""}://{self.host}/api/event'
        r = requests.post(
            url=api_uri,
            headers={
                'User-Agent': user_agent or self.default_user_agent,
                'X-Forwarded-For': forwarded or self.default_forwarded,
            },
            json={
                'name': name,
                'url': url,
                'domain': self.app_domain,
                'screen_width': screen_width,
                'props': props or {},
            },
        )

        if r.status_code != 202:
            raise EventRequestException(r.text)
