from typing import Optional, cast

import requests
import responses


def get_last_request() -> Optional[requests.PreparedRequest]:
    try:
        return cast(requests.PreparedRequest, responses.calls[-1].request)
    except IndexError:
        return None
