from globus_sdk._testing.models import RegisteredResponse, ResponseSet

_common_meta = {
    "id": "daa09846-eb92-11e9-b89c-9cb6d0d9fd63",
    "display_name": "example gateway 1",
}

RESPONSES = ResponseSet(
    metadata=_common_meta,
    default=RegisteredResponse(
        service="gcs",
        method="PATCH",
        path=f"/storage_gateways/{_common_meta['id']}",
        json={
            "DATA_TYPE": "result#1.0.0",
            "http_response_code": 200,
            "detail": "success",
            "message": "Operation successful",
            "code": "success",
            "data": [
                {
                    "DATA_TYPE": "storage_gateway#1.0.0",
                    "id": _common_meta["id"],
                    "display_name": _common_meta["display_name"],
                    "connector_id": "145812c8-decc-41f1-83cf-bb2a85a2a70b",
                    "require_high_assurance": False,
                    "high_assurance": False,
                    "authentication_assurance_timeout": 15840,
                    "authentication_timeout_mins": 15840,
                    "allowed_domains": ["example.edu"],
                    "mapping": "username_without_domain",
                    "restrict_paths": {
                        "DATA_TYPE": "path_restrictions#1.0.0",
                        "read": ["/"],
                    },
                    "policies": {
                        "DATA_TYPE": "posix_storage_gateway#1.0.0",
                        "groups_allow": ["globus"],
                        "groups_deny": ["nonglobus"],
                    },
                    "users_allow": ["user1"],
                    "users_deny": ["user2"],
                }
            ],
        },
        metadata=_common_meta,
    ),
)
