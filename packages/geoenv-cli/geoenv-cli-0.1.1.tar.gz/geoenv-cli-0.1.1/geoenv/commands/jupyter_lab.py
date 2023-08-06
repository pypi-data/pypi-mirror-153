import os
import subprocess
import uuid

from .core import EXPOSED_PORTS, interactive, sub_parsers

EXPOSED_PORTS.append(8001)


def _open_browser(key):
    os.system(f"python -m webbrowser http://localhost:8001/lab?token={key}")
    print("test")


@interactive
def handler(parser_args, *args, **kwargs):
    jl_key = ""
    if parser_args.no_browser is False:
        key = uuid.uuid4()
        jl_key = f"--NotebookApp.token='{key}'"
        subprocess.Popen(
            [f"sleep 3;python -m webbrowser http://localhost:8001/lab?token={key}"],
            shell=True,
        )

    interactive(
        lambda: f"jupyter lab {jl_key} --app_dir=/app/ --port=8001 --ip=0.0.0.0 --allow-root"
    )()


jl_parser = sub_parsers.add_parser("jl", help="Start jupyter lab server")
jl_parser.add_argument(
    "--no-browser", action="store_true", help="Don't open Jupyter in browser"
)

jl_parser.set_defaults(handler=handler)
