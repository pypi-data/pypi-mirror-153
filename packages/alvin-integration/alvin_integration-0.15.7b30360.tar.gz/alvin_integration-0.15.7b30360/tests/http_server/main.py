import json
import traceback

from fastapi import FastAPI, Request

app = FastAPI()

INISGHTS_MAP = {}


def _get_bearer(request: Request) -> str:
    req_headers = request.headers
    print(f"===> headers? {req_headers}")
    return req_headers.get("authorization")


def _save_payload(payload):
    with open("/code/data/payloads.json", "a") as f:
        f.write(f"{payload}\n")


@app.api_route("/{path_name:path}", methods=["POST", "GET"])
async def catch_all(request: Request, path_name: str):
    """
    curl -d '{"foo":"bar"}' -H "Content-Type: application/json" -X POST http://localhost:9003/foo
    """
    try:
        req_body = await request.json()
        print(_get_bearer(request))
        req_body_str = json.dumps(req_body)  # JSON string
        print(
            f"===> INIT request.method {request.method} path_name: {path_name}\nreq_body:{req_body_str}\n"
        )
        _save_payload(req_body_str)
    except Exception as exc:
        print(f"!!! {str(exc)}")
        traceback.print_exc()
        # https://www.starlette.io/requests/
        req_body_bytes = await request.body()
        req_body_str = str(req_body_bytes.decode())
        req_body_len = len(req_body_str)
        print(f"!!! not JSON req body? '{req_body_str}': len? {req_body_len}")
        pass
    return {}
