from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"])
async def handle_all_routes(request: Request, path: str):
    response_data = {"path": path, "method": request.method}  # 新增路径参数

    # GET请求处理（保留原有查询参数逻辑）
    if request.method == "GET":
        response_data["query_params"] = dict(request.query_params) if request.query_params else {}

    # 非GET请求处理（保留原有body处理逻辑）
    if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
        try:
            body = await request.json()
            response_data["body"] = body
        except:
            try:
                body = await request.body()
                response_data["body"] = body.decode() if isinstance(body, bytes) else body
            except:
                response_data["body"] = {}

    # 保留原有的headers处理逻辑
    response_headers = dict(request.headers)
    headers_to_exclude = ["content-length", "content-encoding", "transfer-encoding"]
    for header in headers_to_exclude:
        response_headers.pop(header, None)

    return JSONResponse(content=response_data, headers=response_headers)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
