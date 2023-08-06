# NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
#
# Copyright 2008-2021 Neongecko.com Inc. | All Rights Reserved
#
# Notice of License - Duplicating this Notice of License near the start of any file containing
# a derivative of this software is a condition of license for this software.
# Friendly Licensing:
# No charge, open source royalty free use of the Neon AI software source and object is offered for
# educational users, noncommercial enthusiasts, Public Benefit Corporations (and LLCs) and
# Social Purpose Corporations (and LLCs). Developers can contact developers@neon.ai
# For commercial licensing, distribution of derivative works or redistribution please contact licenses@neon.ai
# Distributed on an "AS IS” basis without warranties or conditions of any kind, either express or implied.
# Trademarks of Neongecko: Neon AI(TM), Neon Assist (TM), Neon Communicator(TM), Klat(TM)
# Authors: Guy Daniels, Daniel McKnight, Regina Bloomstine, Elon Gasper, Richard Leeds
#
# Specialized conversational reconveyance options from Conversation Processing Intelligence Corp.
# US Patents 2008-2021: US7424516, US20140161250, US20140177813, US8638908, US8068604, US8553852, US10530923, US10530924
# China Patent: CN102017585  -  Europe Patent: EU2156652  -  Patents Pending

from socketio import exceptions as sio_exceptions
from socketio import Client
from threading import Thread
from time import time, sleep
from .logger import LOG
from .legacy_socket_adapter import SocketIOCompat


# Default server connection
server_addr = "2222.us"
server_port = 8888


def _run_listener(socket):
    """
    Runs socket listeners indefinitely
    """
    socket.wait()


def _establish_socket_connection(socket: Client, addr: str, port: int):
    if addr == "0.0.0.0":
        url = f"http://{addr}:{port}"
    else:
        url = f"https://{addr}:{port}"
    socket.connect(url, wait_timeout=10, transports=['websocket', 'polling'],
                   namespaces='/')
    event_thread = Thread(target=_run_listener, args=[socket])
    event_thread.setDaemon(True)
    event_thread.start()
    LOG.debug(f"returning {socket}")
    return socket


def _establish_legacy_socket_connection(socket: SocketIOCompat):
    socket.connect(None)


def start_socket(addr=server_addr, port=server_port, retry_timeout=120):
    """
    Initialize a socketIO connection to the specified server and port
    :param addr: url of socketIO server to connect to
    :param port: port used for socketIO
    :param retry_timeout: max seconds to try to establish a connection
    :return: socketIO Client
    """
    # global socket
    socket = Client(request_timeout=30)

    timeout = time() + retry_timeout

    # Catch connected socket
    while not socket.connected and time() < timeout:
        try:
            if isinstance(socket, Client):
                _establish_socket_connection(socket, addr, port)
            elif isinstance(socket, SocketIOCompat):
                _establish_legacy_socket_connection(socket)
        except sio_exceptions.ConnectionError as e:
            if isinstance(socket, Client) and e.args[0] == "Unexpected response from server":
                LOG.warning("Falling back to SocketIOCompat connection")
                socket = SocketIOCompat(f"https://{addr}", port, verify=False)
            else:
                LOG.exception(e)
                LOG.error("Retrying in 5 seconds")
                sleep(5)
    return socket
