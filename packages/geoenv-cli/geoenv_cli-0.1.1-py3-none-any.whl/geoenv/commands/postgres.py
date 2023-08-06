from .core import GEOENV_NETWORK, is_container_running, run, sub_parsers

PG_CONTAINER_NAME = "geoenv-postgres-container"
PG_USER = "postgres"
PG_PASSWORD = "postgres"


@run
def handler(parser_args, *args, **kwargs):
    if is_container_running(PG_CONTAINER_NAME):
        if parser_args.stop:
            return f"docker kill {PG_CONTAINER_NAME}"
        return
    return f"docker run --rm -d --network {GEOENV_NETWORK} --name '{PG_CONTAINER_NAME}' -e POSTGRES_USER={PG_USER} -e POSTGRES_PASSWORD={PG_PASSWORD} postgis/postgis"


postgres_parser = sub_parsers.add_parser(
    "postgres", help="Start postgres docker container"
)
postgres_parser.add_argument(
    "--stop", action="store_true", help="Stop postgres docker container"
)

postgres_parser.set_defaults(handler=handler)
