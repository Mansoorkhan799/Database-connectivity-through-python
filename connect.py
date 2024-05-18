from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import pymysql.cursors

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('F:/xamp/htdocs/form.html', 'rb') as file: 
            self.wfile.write(file.read())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_params = parse_qs(post_data.decode('utf-8'))
        name = post_params.get('name', [''])[0]
        email = post_params.get('email', [''])[0]
        password = post_params.get('password', [''])[0]

        # Connect to MySQL database
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='connections',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `form` (`name`, `email`, `password`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (name, email, password))
            
            # Commit changes
            connection.commit()
            print("Data submitted successfully!")
            
        except Exception as e:
            print("Error:", e)
            
        finally:
            # Close the connection
            connection.close()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Data submitted successfully!')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print("Server stopped.")

if __name__ == '__main__':
    run()