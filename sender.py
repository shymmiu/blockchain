import socket
import json

# Server configuration
HOST = '127.0.0.1'  # Server IP address
PORT = 65432        # Server port
BUFFER_SIZE = 65536  # Larger buffer for blockchain data


def recv_all(sock: socket.socket) -> bytes:
    """Receive all data from socket until connection closes."""
    chunks = []
    while True:
        chunk = sock.recv(BUFFER_SIZE)
        if not chunk:
            break
        chunks.append(chunk)
    return b''.join(chunks)


def send_command(command: str) -> str:
    """Send a command to the blockchain server and return the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(command.encode())
        s.shutdown(socket.SHUT_WR)  # Signal we're done sending
        data = recv_all(s)
        return data.decode()


def main():
    """Interactive blockchain client."""
    print("Blockchain Client")
    print("Commands:")
    print("  ADD <json_data>  - Add data to pending transactions")
    print("  MINE             - Mine a new block with pending data")
    print("  CHAIN            - Get the entire blockchain")
    print("  VALIDATE         - Check if blockchain is valid")
    print("  LENGTH           - Get blockchain length")
    print("  quit             - Exit the client")
    print()
    
    while True:
        try:
            command = input("Enter command: ").strip()
            if not command:
                continue
            if command.lower() == "quit":
                print("Goodbye!")
                break
            
            response = send_command(command)
            try:
                parsed = json.loads(response)
                print("Response:", json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                print("Response:", response)
            print()
        except ConnectionRefusedError:
            print("Error: Cannot connect to server. Make sure the server is running.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()

