from time import sleep

import zmq
from album.api import Album
from album.core.model.default_values import DefaultValues
from album.runner.album_logging import get_active_logger
from album.socket.server import AlbumSocketServer
from requests.exceptions import InvalidSchema
from urllib3.exceptions import MaxRetryError, NewConnectionError


class ServerLauncher:
    server = None

    def __init__(self, args, album_instance):
        self.args = args
        self.album_instance = album_instance

    def launch(self, event):
        self.server = AlbumSocketServer(self.args['port'])
        self.server.setup(self.album_instance)
        self.server.start()
        max_tries = 5
        while max_tries > 0:
            try:
                context = zmq.Context()
                rep = context.socket(zmq.REQ)
                rep.connect("tcp://%s:%s" % (self.args['host'], self.args['port']))
                rep.send_pyobj({"action": "ping"})
                res = rep.recv_pyobj()
                assert res["status"] == 200
                break
            except InvalidSchema as e:
                get_active_logger().debug(str(e))
                sleep(1)
                max_tries -= 1
            except (ConnectionError, ConnectionRefusedError, MaxRetryError, NewConnectionError) as e:
                get_active_logger().debug(str(e))
                sleep(1)
                max_tries -= 1

    def stop(self, event):
        self.server.shutdown()


def launch_server(album_instance: Album, solution_coordinates, args):
    get_active_logger().debug("Launching server thread....")
    args["host"] = "127.0.0.1"
    server_launcher = ServerLauncher(args, album_instance)
    album_instance.add_event_listener(DefaultValues.before_run_event_name.value, server_launcher.launch, solution_coordinates)
    album_instance.add_event_listener(DefaultValues.after_run_event_name.value, server_launcher.stop, solution_coordinates)
    get_active_logger().debug("Done with server thread.")
