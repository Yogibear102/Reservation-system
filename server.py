# server.py
import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

# Dictionary of table number -> (name, time)
reservations = {}
MAX_TABLES = 5

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    conn.sendall(b"Connected to EasyEats Server!\n")

    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            parts = data.split(",")
            cmd = parts[0]

            if cmd == "SHOW":
                response = ",".join(
                    [f"{i+1}:{'Free' if (i+1) not in reservations else 'Booked'}" for i in range(MAX_TABLES)]
                )
            elif cmd == "BOOK":
                table = int(parts[1])
                name = parts[2]
                time = parts[3]

                if table in reservations:
                    response = f"Table {table} is already booked."
                elif table > MAX_TABLES or table < 1:
                    response = "Invalid table number."
                else:
                    reservations[table] = (name, time)
                    response = f"Table {table} booked for {name} at {time}."
            else:
                response = "Unknown command."

            conn.sendall(response.encode())
        except:
            break

    conn.close()
    print(f"[DISCONNECTED] {addr}")

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start()
