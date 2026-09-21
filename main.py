import socket

HOST = "localhost"
PORT = 1903

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))


def requestHandler(data):
    data = data.decode()
    body = data.split("\r\n")

    header = body[0].split()
    endpoint = header[1]

    content = "404 NOT FOUND"
    status = "404 Not Found"

    if endpoint == "/check":
        content = "Working Correctly!"
        status = "200 OK"

    elif endpoint == "/hi":
        content = "Hi back!"
        status = "200 OK"

    response = (
        f"HTTP/1.1 {status}\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(content)}\r\n"
        "\r\n"
        f"{content}"
    )
    return response


with server as s:
    print("Server is listening...")
    s.listen(5)

    while True:
        conn, addr = s.accept()

        # print(f"Connection: {conn}\nAddress: {addr}")

        with conn:
            data = conn.recv(1024)

            if not data:
                continue

            response = requestHandler(data)

            conn.sendall(response.encode("utf-8"))
