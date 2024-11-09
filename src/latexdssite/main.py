import argparse
from typing import NoReturn

from aiohttp.web import Application, HTTPNotFound, get, HTTPFound, Request, run_app, static


class LaTeXDSSite(Application):
    def __init__(self, www_path: str = "www", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_routes(
            [
                get("/", self.root_redirect),
                get("/source/{which}", self.source_redirect),
                get("/tos", self.tos_redirect),
                get("/privacy", self.privacy_redirect),
                static("/", www_path),
            ]
        )

    async def root_redirect(self, _: Request) -> NoReturn:
        raise HTTPFound("https://discord.com/oauth2/authorize?client_id=1269223729267740703")

    async def tos_redirect(self, _: Request) -> NoReturn:
        raise HTTPFound("https://latexds.pwn3t.ru/tos.html")

    async def privacy_redirect(self, _: Request) -> NoReturn:
        raise HTTPFound("https://latexds.pwn3t.ru/privacy.html")

    async def source_redirect(self, request: Request) -> NoReturn:
        match request.match_info["which"]:
            case "bot":
                raise HTTPFound("https://github.com/latexds/latexds")
            case "site":
                raise HTTPFound("https://github.com/latexds/latexds.pwn3t.ru")
            case _:
                raise HTTPNotFound


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
    parser.add_argument(
        "-r", "--root",
        default="www",
        metavar="PATH",
        help="Root where static pages are"
    )
    args = parser.parse_args()

    try:
        run_app(LaTeXDSSite(args.root), host=args.host, port=args.port)
    except KeyboardInterrupt:
        pass
