import click
from . import config
from .watcher import main

@click.command()
@click.help_option('--help', '-h')
@click.version_option()
@click.option('--port', '-p', default=8888, help='Server port')
@click.argument('root', default='.', type=click.Path(exists=True, dir_okay=True, readable=True, resolve_path=True))
def start(port, root):
    config.SERVER_PORT = int(port)
    config.SERVER_ROOT = root
    try:
        main()
    except OSError:
        print('Port {} is already in use. Use `-P` flag and specify a different port.'.format(config.SERVER_PORT))
