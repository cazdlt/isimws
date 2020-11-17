from .request import Request
from typing import TYPE_CHECKING
from zeep.helpers import serialize_object

if TYPE_CHECKING:
    from pyisim.auth import Session


class Response:
    def __init__(self, session: "Session", raw, content=None) -> None:

        if raw is None:
            self.raw=None
            self.type="SOAP"
        elif "zeep" in type(raw).__module__:
            self.raw = serialize_object(raw, dict)
            self.type = "SOAP"
        else:
            self.raw = raw.json()
            self.type = "REST"

        if self.raw:
            if "WSRequest" in type(raw).__name__:
                self.request = Request(session, request=raw)
            elif isinstance(self.raw, dict):
                if self.raw.get("request_id"):
                    request_id = self.raw["request_id"]
                elif self.raw.get("requestID"):
                    request_id = self.raw["requestID"]
                elif self.raw.get("requestId"):
                    request_id = self.raw["requestId"]
                elif self.raw.get("_links", {}).get("result", {}).get("href"):
                    request_id = self.raw["_links"]["result"]["href"]
                else:
                    request_id = None

                if request_id:
                    self.request = Request(session, id=request_id)

        if content:
            self.result = content
        else:
            if self.type=="REST":
                self.result={
                    "status_code":raw.status_code,
                    "reason":raw.reason,
                }
            else:
                self.result={
                    "reason":"Accepted"
                }
