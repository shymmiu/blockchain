import socket

# Definir la dirección y el puerto en el que el servidor escuchará
HOST = '127.0.0.1'  # Dirección IP del servidor (localhost)
PORT = 65432        # Puerto en el que el servidor escuchará

# Crear un socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # Asignar la dirección y el puerto al socket
    s.listen()            # Escuchar conexiones entrantes

    print(f"Servidor escuchando en {HOST}:{PORT}")

    # Esperar a que una conexión entrante
    conn, addr = s.accept()  # Aceptar la conexión
    with conn:
        print(f"Conectado por {addr}")
        while True:
            data = conn.recv(1024)  # Recibir datos del cliente
            if not data:
                break
            print(f"Recibido: {data.decode()}")
            if (data.decode()).startswith("image"):
                f = open("image.txt", "w")
                f.write(data.decode())

            conn.sendall(data)  # Enviar de vuelta los datos recibidos (eco)

        print("Conexión cerrada")
