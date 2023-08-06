import argparse
from multiprocessing import Process, Queue
from typing import Dict

from .server import run_server
from .types import RunFn, SetupFn

from .sources import demo, rpctask


def main():
    parser = argparse.ArgumentParser(
        prog='lidia',
        description='serve an aircraft instruments panel as a web page',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog='you can also see help for a specific source: "lidia <src> --help"')
    parser.add_argument('--http-host', '-H', type=str,
                        help='hosts to accept for web page', default='0.0.0.0')
    parser.add_argument('--http-port', '-P', type=int,
                        help='port to serve the web page on', default=5555)
    subparsers = parser.add_subparsers(title='source', required=True, dest='source',
                                       help='source name', description='select where to get aircraft state')

    sources: Dict[str, RunFn] = {}
    for source_module in [demo, rpctask]:
        setup: SetupFn = source_module.setup
        name, run_function = setup(subparsers)
        sources[name] = run_function

    args = parser.parse_args()

    queue = Queue()
    server_process = Process(target=run_server, args=(
        queue, args.http_host, args.http_port))
    server_process.start()

    print(f'Lidia GUI for {args.source} on http://localhost:{args.http_port}')
    try:
        (sources[args.source])(queue, args)

    except KeyboardInterrupt:
        print('Exiting main loop')

    server_process.terminate()


if __name__ == '__main__':
    main()
