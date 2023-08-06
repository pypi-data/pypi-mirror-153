from pathlib import Path
from trame.app import get_server, dev

SERVER = None


def main(server=None, **kwargs):
    from . import engine, ui

    global SERVER
    if server is None:
        server = get_server()

    # Add CLI
    server.cli.add_argument(
        "--data", help="Path to browse", dest="data", default=str(Path.home())
    )
    server.cli.add_argument(
        "--plugins", help="List of distributed plugins to load", dest="plugins"
    )

    # Make UI auto reload
    def _reload():
        dev.reload(ui)
        ui.initialize(SERVER)

    server.controller.on_server_reload.add(_reload)

    # Init application
    SERVER = server

    engine.initialize(server)
    ui.initialize(server)

    # Start server
    server.start(**kwargs)


if __name__ == "__main__":
    server = get_server()
    main(server)
