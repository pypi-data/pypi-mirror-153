import os
import uuid
from mlflow.tracking.request_header.abstract_request_header_provider import (
    RequestHeaderProvider,
)
from mlflow.tracking.fluent import active_run, _get_experiment_id, get_experiment


class DeploifaiRequestHeaderProvider(RequestHeaderProvider):
    # set class variable to identify deploifai experiment run so that all mlflow runs get associated with the same deploifai experiment run
    # if USER_EXPERIMENT_RUN_ID environment variable is not set, generate a new deploifai experiment run using a new uuid
    _deploifai_run_id = os.environ.get("USER_EXPERIMENT_RUN_ID", default=str(uuid.uuid4()))

    def in_context(self):
        return True

    def request_headers(self):
        added_headers = {}

        added_headers.update({"deploifai-runid": self._deploifai_run_id})

        _run = active_run()
        if _run is not None:
            added_headers.update({"mlflow-runid": _run.info.run_id})

        experiment_id = str(_get_experiment_id())
        added_headers.update({"experiment": experiment_id, "client": "deploifai"})

        return added_headers
