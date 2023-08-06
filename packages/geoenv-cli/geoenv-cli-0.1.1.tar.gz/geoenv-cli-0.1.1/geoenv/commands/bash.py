from .core import interactive, sub_parsers


@interactive
def handler(*args, **kwargs):
    return "bash"


bash_parser = sub_parsers.add_parser("bash", help="Start interactive bash session")
bash_parser.set_defaults(handler=handler)
