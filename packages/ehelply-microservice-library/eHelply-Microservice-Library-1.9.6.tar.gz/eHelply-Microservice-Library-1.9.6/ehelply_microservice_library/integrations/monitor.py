from __future__ import annotations
from ehelply_bootstrapper.integrations.integration import Integration
from ehelply_microservice_library.integrations.fact import get_fact_endpoint

from ehelply_bootstrapper.utils.state import State

from ehelply_microservice_library.integrations.sdk import SDK

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import json


class UsageMQ(BaseModel):
    project_uuid: str
    usage_key: str
    quantity: int  # Quantity formats represented by a x10000000 integer. Precision to the millonth


class Monitor(Integration):
    """
    Monitor integration is used to talk to the ehelply-meta microservice
    """

    def __init__(self) -> None:
        super().__init__("monitor")

        self.sqs = State.aws.make_client("sqs")

    def load(self):
        pass

    def add_usage(self, usage: UsageMQ) -> bool:
        """
        Add usage to a project

        NOTE: Quantity formats represented by a x10000000 integer. Precision to the millonth

        :return:
        """
        if usage.project_uuid == 'ehelply-resources' or usage.project_uuid == 'ehelply-cloud':
            return False

        self.sqs.send_message(
            QueueUrl=get_fact_endpoint("mq-usage"),
            MessageBody=json.dumps(jsonable_encoder(usage.dict()))
        )

        return True
