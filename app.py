from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn
import asyncio  # 新增导入

app = FastAPI()


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"])
async def handle_all_routes(request: Request, path: str):
    response_data = {"path": path, "method": request.method}

    # 获取查询参数
    query_params = dict(request.query_params) if request.query_params else {}

    # 从查询参数中获取 status_code
    status_code = 200  # 默认状态码
    if "status_code" in query_params:
        try:
            status_code = int(query_params.pop("status_code"))
        except (ValueError, TypeError):
            pass  # 如果转换失败，使用默认状态码

    # 新增：从查询参数中获取 delay
    delay = 0  # 默认延迟为0秒
    if "delay" in query_params:
        try:
            delay = int(query_params.pop("delay"))
        except (ValueError, TypeError):
            pass  # 如果转换失败，使用默认延迟

    # 如果有延迟，执行异步等待
    if delay > 0:
        await asyncio.sleep(delay)

    # GET请求处理
    if request.method == "GET":
        response_data["query_params"] = query_params

    # 非GET请求处理
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

    # 处理headers
    response_headers = dict(request.headers)
    headers_to_exclude = ["content-length", "content-encoding", "transfer-encoding"]
    for header in headers_to_exclude:
        response_headers.pop(header, None)

    # 将 delay 添加到响应数据中
    response_data["delay"] = delay

    return JSONResponse(content=response_data, headers=response_headers, status_code=status_code)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
