import argparse
from time import sleep
from multiprocessing import Process, Queue

from .server import run_server


def main():
    parser = argparse.ArgumentParser(
        prog='lidia',
        description='serve an aircraft instruments panel as a web page',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--http-host', '-H', type=str,
                        help='hosts to accept for web page', default='0.0.0.0')
    parser.add_argument('--http-port', '-P', type=int,
                        help='port to serve the web page on', default=5555)
    args = parser.parse_args()

    queue = Queue()

    server_process = Process(target=run_server, args=(
        queue, args.http_host, args.http_port))
    server_process.start()
    try:
        print('Blocking loop in main process')
        while True:
            queue.put(('echo', 'message from main loop'))
            sleep(1)
    except KeyboardInterrupt:
        print('Exiting main loop')

    server_process.terminate()


if __name__ == '__main__':
    main()
