import boto3

from typing import Callable
from app.types.lmbd import InvokeResponse

LAMBDA = boto3.client('lambda')


def catchLambdaError(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        # TODO: Catch specific Lambda errors
        except Exception:
            # TODO: SEND ERROR NOTIFICATION
            return {}
    return wrapper


@catchLambdaError
def invokeEvent(payload: str, functionName: str) -> InvokeResponse:
    return LAMBDA.invoke(
        FunctionName=functionName,
        InvocationType='Event',
        LogType='None',
        Payload=payload,
    )
