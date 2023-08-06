from globus_sdk._testing.models import RegisteredResponse, ResponseSet

from .get_job import JOB_ID, JOB_JSON

metadata = {"job_id": JOB_ID}

RESPONSES = ResponseSet(
    metadata=metadata,
    default=RegisteredResponse(
        service="timer",
        path=f"/jobs/{JOB_ID}",
        method="DELETE",
        json=JOB_JSON,
        metadata=metadata,
    ),
)
