import struct
from .message_protocol import MessageProtocol
from ...logging import log
from ...domain.exceptions.could_not_connect_to_server import CouldNotConnectToServerException

# TODO: Duplicado en server y SDK, ver de usar uno en comun
class MessageProtocolRS232(MessageProtocol):
    def __init__(self, rs232_connection):
        self._connection = rs232_connection
        if not self._connection.isOpen():
            self._connection.open()

    def disconnect(self):
        self._connection.close()

    def send_msg(self, msg, encode=True):
        if encode:
            msg = msg.encode()
        # Prefix each message with a 4-byte length
        msg = struct.pack('>I', len(msg)) + msg
        self._connection.write(msg)

    def receive_msg(self, decode=True):
        # Read message length and unpack it into an integer
        raw_msglen = self.__recvall(4)
        if not raw_msglen:
            raise ConnectionResetError
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        data = self.__recvall(msglen)
        if decode:
            data = data.decode()
        return data

    def __recvall(self, n):
        # Helper function to recv n bytes or raise ConnectionResetError if EOF is hit
        data = bytearray()
        while len(data) < n:
            bytes_to_read = max(1, min(2048, self._connection.in_waiting, n - len(data)))
            packet = self._connection.read(bytes_to_read)
            if not packet:
                raise ConnectionResetError
            data.extend(packet)
        return data