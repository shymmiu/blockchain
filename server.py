import socket
import json
from blockchain import Blockchain

# Server configuration
HOST = '127.0.0.1'  # Server IP address (localhost)
PORT = 65432        # Server port

# Initialize blockchain
blockchain = Blockchain(difficulty=2)

def handle_command(command: str, data: str) -> str:
    """Handle blockchain commands from clients."""
    if command == "ADD":
        try:
            transaction = json.loads(data)
            blockchain.add_data(transaction)
            return json.dumps({"status": "success", "message": "Data added to pending"})
        except json.JSONDecodeError:
            blockchain.add_data(data)
            return json.dumps({"status": "success", "message": "Data added to pending"})
    
    elif command == "MINE":
        block = blockchain.mine_pending_data()
        if block:
            return json.dumps({"status": "success", "message": f"Block {block.index} mined", "hash": block.hash})
        return json.dumps({"status": "info", "message": "No pending data to mine"})
    
    elif command == "CHAIN":
        return json.dumps({"status": "success", "chain": blockchain.get_chain_data()})
    
    elif command == "VALIDATE":
        is_valid = blockchain.is_chain_valid()
        return json.dumps({"status": "success", "valid": is_valid})
    
    elif command == "LENGTH":
        return json.dumps({"status": "success", "length": len(blockchain)})
    
    else:
        return json.dumps({"status": "error", "message": f"Unknown command: {command}"})


def run_server():
    """Run the blockchain server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()

        print(f"Blockchain server listening on {HOST}:{PORT}")
        print("Commands: ADD <json_data>, MINE, CHAIN, VALIDATE, LENGTH")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    
                    message = data.decode().strip()
                    print(f"Received: {message}")
                    
                    # Parse command and data
                    parts = message.split(" ", 1)
                    command = parts[0].upper()
                    cmd_data = parts[1] if len(parts) > 1 else ""
                    
                    # Handle legacy image command
                    if message.startswith("image"):
                        with open("image.txt", "w") as f:
                            f.write(message)
                        response = json.dumps({"status": "success", "message": "Image data saved"})
                    else:
                        response = handle_command(command, cmd_data)
                    
                    conn.sendall(response.encode())
                    print(f"Response: {response}")

                print("Connection closed")


if __name__ == "__main__":
    run_server()

