# ZipLoot Optimized Production Server
import http.server
import socketserver

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

if __name__ == '__main__':
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        print(f'ZipLoot Server Running on Port {PORT}')
        httpd.serve_forever()
