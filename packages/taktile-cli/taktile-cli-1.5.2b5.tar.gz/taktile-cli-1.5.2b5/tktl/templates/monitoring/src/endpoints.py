"""Template demonstrating Feature Monitoring.
Documentation https://docs.taktile.com/using-taktile/monitoring
"""
from pydantic import BaseModel

from tktl.future import Tktl
from tktl.future.monitor import Tracker

# instantiate client
client = Tktl()


class Payload(BaseModel):
    feature: str


class Response(BaseModel):
    result: str


# endpoints
@client.endpoint(
    X=Payload, y=Response, track_inputs=["feature"], track_outputs=["result"]
)
def func(x: Payload, tracker: Tracker) -> Response:
    tracker.log_numerical("feature_len", len(x.feature))
    return Response(result=x.feature)
