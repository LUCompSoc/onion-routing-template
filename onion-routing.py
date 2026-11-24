from __future__ import annotations
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os


class Node:
    def __init__(self, name):
        self.name = name
        self.next: Node | None = None
        self.key = algorithms.AES(os.urandom(16))

    # Called first called by the previous node, returns to that node
    def forward_message(self, message: bytes) -> bytes:
        raise NotImplementedError(
                "Subclasses must implement receive_message()"
        )

    def set_next_node(self, next_node: Node) -> None:
        self.next = next_node

    def debug_send(self, message: bytes, type: str) -> None:
        print(f"{self.name}: sending {type}: {message}")

    def debug_receive(self, message: bytes, type: str) -> None:
        print(f"{self.name}: received {type}: {message}")


class Client(Node):
    def __init__(self, name):
        self.name = name
        self.next: Node | None = None
        self.keys = []

    def forward_message(self, message) -> bytes:
        if self.next is not None:  # Start Client
            print(f"{self.name} sending: {message}")
            ciphertext = pad_message(message)  # Padding the message
            print(f"{self.name} padded: {ciphertext}")

            # Encrypt 'ciphertext' with all the keys in self.keys
            # n.b. remember how the layers of encryption resemble an onion

            # Encryption goes here!
            raise NotImplementedError("Encryption on start node")

            self.debug_send(ciphertext, "request")
            response = self.next.forward_message(ciphertext)  # Starting the chain

            self.debug_receive(response, "response")
            # Decrypt 'response' with all the keys in self.keys
            # Again, you should recall the order in which the response is encrypted

            # Decryption goes here!
            raise NotImplementedError("decryption on start node")

            response = unpad_message(response) # Unpadding the message

            print(f"{self.name} received response: {bytes.decode(response)}")
            return response
        else:  # End Client
            print(f"{self.name} received: {message}")
            message = unpad_message(message)
            print(f"{self.name} received: {bytes.decode(message)}")
            return_msg = "This is a test response!"

            print(f"{self.name} responding: {message}")
            return_bytes = str.encode(return_msg)
            return_bytes = pad_message(return_bytes)
            print(f"{self.name} padded: {return_bytes}")
            return return_bytes

    def send_message(self, message) -> None:
        message_bytes = message.encode()
        self.forward_message(message_bytes)


class Relay(Node):
    def forward_message(self, message: bytes) -> bytes:
        self.debug_receive(message, "request")
        cipher = Cipher(self.key, modes.ECB())

        # Remove this relays layer of Encryption
        raise NotImplementedError("Decryption on Relay")

        self.debug_send(message, "request")
        response = self.next.forward_message(message)  # Passing on the message to the next node
        self.debug_receive(response, "response")

        # Add a layer of encryption for this node
        raise NotImplementedError("Encryption on Relay")

        self.debug_send(response, "response")
        return response


def pad_message(message: bytes) -> bytes:
    # Pad 'message' and return it
    raise NotImplementedError("pad_message function")
    pass


def unpad_message(message: bytes) -> bytes:
    # Pad 'message' and return it
    raise NotImplementedError("unpad_message function")
    pass


def main():
    start_client = Client("start client")
    end_client = Client("end client")
    relay_1 = Relay("relay 1")
    relay_2 = Relay("relay 2")
    relay_3 = Relay("relay 3")

    start_client.set_next_node(relay_1)
    relay_1.set_next_node(relay_2)
    relay_2.set_next_node(relay_3)
    relay_3.set_next_node(end_client)

    start_client.keys.append(relay_1.key)
    start_client.keys.append(relay_2.key)
    start_client.keys.append(relay_3.key)
    start_client.send_message("This is a test message!")


if __name__ == "__main__":
    main()
