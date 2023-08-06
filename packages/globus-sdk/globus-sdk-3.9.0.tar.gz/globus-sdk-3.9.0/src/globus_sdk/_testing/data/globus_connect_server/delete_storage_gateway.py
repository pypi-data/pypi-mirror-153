from globus_sdk._testing.models import RegisteredResponse, ResponseSet

_common_meta = {
    "id": "daa09846-eb92-11e9-b89c-9cb6d0d9fd63",
    "display_name": "example gateway 1",
}

RESPONSES = ResponseSet(
    metadata=_common_meta,
    default=RegisteredResponse(
        service="gcs",
        method="DELETE",
        path=f"/storage_gateways/{_common_meta['id']}",
        json={
            "DATA_TYPE": "result#1.0.0",
            "http_response_code": 200,
            "detail": "success",
            "message": "Operation successful",
            "code": "success",
            "data": [{}],
        },
        metadata=_common_meta,
    ),
)
