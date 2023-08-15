# AWS Lambda

from pydantic import BaseModel


class InvokeResponse(BaseModel):
    StatusCode: int
    FunctionError: str
    Payload: bytes
    LogResult: str
    ExecutedVersion: str
