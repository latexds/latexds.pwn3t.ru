import argparse
from os.path import isfile

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn


class LaTeXDSSite(FastAPI):
    def __init__(self) -> None:
        super().__init__(docs_url=None, redoc_url=None)

        @self.get("/", response_class=RedirectResponse)
        def invite() -> RedirectResponse:
            return RedirectResponse("https://discord.com/oauth2/authorize?client_id=1269223729267740703")

        @self.get("/source/{who}", response_class=RedirectResponse)
        def source(who: str) -> RedirectResponse:
            if who == "bot":
                return RedirectResponse("https://github.com/latexds/latexds")
            elif who == "site":
                return RedirectResponse("https://github.com/latexds/latexds.nakidai.ru")
            raise HTTPException(status_code=404, detail="Not found")

        @self.get("/{path}", response_class=HTMLResponse)
        def static(path: str) -> HTMLResponse:
            if not isfile(f"{path}.html"):
                raise HTTPException(status_code=404, detail="Not found")
            with open(f"{path}.html") as page, open("base") as base:
                return HTMLResponse(base.read() + page.read())


def main() -> None:
    parser = argparse.ArgumentParser(description="Site for LaTeXDS")
    parser.add_argument(
        "-p", "--port",
        default=8000,
        type=int,
        metavar="PORT",
        help="Port where app should be run"
    )
    parser.add_argument(
        "-i", "--host",
        default="127.0.0.1",
        metavar="HOST",
        help="IP of your host"
    )
    args = parser.parse_args()

    try:
        uvicorn.run(
            LaTeXDSSite(),
            host=args.host,
            port=args.port,
            log_level="info"
        )
    except KeyboardInterrupt:
        pass
