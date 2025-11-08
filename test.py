import socket

URLS: dict = {
    '/': '<h1>Hello index!</h1><p>Welcome to the homepage!</p>',
    '/blog': "<h1>Blog</h1><p>Hello blog!</p>",
}

def parse_request(request) -> tuple:
    parsed: list = request.split(' ')
    
    if len(parsed) < 2:
        return ('', '')
    
    method: str = parsed[0]
    url: str = parsed[1]

    print(f"METHOD: {method}\nURL: {url}")

    return (method, url)

def gen_headers(method, url):
    if not (method == 'GET'):
        return ("HTTP/1.1 405 Method not Allowed\r\n", 405)

    if url not in URLS:
        return ("HTTP/1.1 404 Not found\r\n", 404)

    return ("HTTP/1.1 200 OK\r\n", 200)

def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not Found</p>'
    
    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'
    
    return URLS[url]

def gen_response(request: str) -> bytes:
    method, url = parse_request(request)
    headers, code = gen_headers(method, url)
    
    # Добавляем заголовки Content-Type и Content-Length
    body = generate_content(code, url)
    headers += f"Content-Type: text/html; charset=utf-8\r\n"
    headers += f"Content-Length: {len(body.encode('utf-8'))}\r\n"
    headers += "\r\n"  # Пустая строка, разделяющая заголовки и тело
    
    return (headers + body).encode('utf-8')

def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    try:
        while True:
            client_socket, addr = server_socket.accept()
            
            request: bytes = client_socket.recv(1024)
            
            # Проверяем, что запрос не пустой
            if request:
                response: bytes = gen_response(request.decode('utf-8'))
                
                print(request.decode('utf-8'))
                print(f"Client address: {addr}")
                print("-" * 50)
                
                client_socket.sendall(response)
            
            client_socket.close()

    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == "__main__":
    run()