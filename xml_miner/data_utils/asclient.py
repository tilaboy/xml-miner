"""A module to communicate the TK annotation server"""
from typing import List, Iterator
import re
import socket
from .. import LOGGER


class ASClient:
    """Python version of annotation server client"""
    BUFFER_SIZE = 2 * 1024
    ENCODING = 'utf-8'

    def __init__(self, host: str, port: str,
                 as_user: str = '', as_pass: str = ''):
        """
        Init a new socket client to the annotation server

        params:
            host (str): hostname of the annotationserver
            port (str/int): port of the AnnotationServer
            as_user (str): AnnotationServer username, optional
            as_pass (str): AnnotationServer password, optional
        """
        self.host = host
        self.port = int(port)
        self.as_user = as_user
        self.as_pass = as_pass

        self.tk_socket = None

    def make_connection(self) -> bool:
        """Build connect to the Annotation Server"""
        self.tk_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not self.tk_socket:
            raise IOError('Socket not initialized')
        self.tk_socket.connect((self.host, self.port))
        self.check_user_password()
        return

    def check_user_password(self):
        """send server the username and password and confirm the loggin"""
        response = None
        try:
            # The commnunication is to
            # - receive message "user" send the username
            # - receive message "password" and send the password
            self.tk_socket.recv(self.BUFFER_SIZE)
            self.tk_socket.send(self.prepare_message(self.as_user))
            self.tk_socket.recv(self.BUFFER_SIZE)
            self.tk_socket.send(self.prepare_message(self.as_pass))

            response = self.tk_socket.recv(self.BUFFER_SIZE)
        except IOError as error:
            raise IOError("Unexpected welcome message: {}:{}{}".format(
                self.host, self.port, error))

        response = response.decode(self.ENCODING)
        if not response.startswith("OK"):
            raise IOError("Unexpected welcome message:{}".format(response))

        return

    def prepare_message(self, message: str) -> str:
        """
        prepare the query message:
        - add new line
        - encode with utf8
        """
        if not message.endswith('\n'):
            message += "\n"
        return message.encode(self.ENCODING)

    def close_socket(self):
        """shutdown the connect"""
        try:
            self.tk_socket.close()
        except IOError as error:
            raise IOError("unable to close the connection from \
                {}:{}, {}".format(self.host, self.port, error))
        return

    def socket_output(self) -> str:
        """Receive response from Annotation Server and decode"""
        output = b''
        while 1:
            try:
                data = self.tk_socket.recv(self.BUFFER_SIZE)
            except IOError as error:
                raise IOError("wrong response from {}:{}, {}".format(
                    self.host, self.port, error))
            else:
                if not data:
                    break
                output += data
        try:
            output = output.decode(self.ENCODING)
        except UnicodeDecodeError as error:
            raise IOError("failed to decode the message.\n" + error)
        return output

    def send_and_receive(self, query: str) -> str:
        """send the query to AS and decode the received response"""
        try:
            self.make_connection()
            self.tk_socket.send(self.prepare_message(query))
            result = self.socket_output()
            self.close_socket()
        except IOError as error:
            raise IOError("not able to send or receive data from \
            {}:{}, {}".format(self.host, self.port, error))
        return result

    def get_ids(self, query: str = '') -> List[str]:
        """get all document ids of all the queried documents"""
        ids_string = self.send_and_receive('GIVE ids ' + query)
        ids = [id for id in ids_string.split("\n") if re.match("^[0-9]+$", id)]
        return ids

    def get_docs(self, query='') -> Iterator[str]:
        """get all queried documents"""
        ids = self.get_ids(query)
        for doc_index in ids:
            try:
                document = self.send_and_receive('GIVE xml id ' + doc_index)
            except IOError:
                LOGGER.warning("WARNING: failed to fetch document: %s",
                               doc_index)
            else:
                yield document
