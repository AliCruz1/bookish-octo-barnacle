from http.server import HTTPServer, BaseHTTPRequestHandler
from restaurantDatabase import RestaurantDatabase
import cgi

class RestaurantPortalHandler(BaseHTTPRequestHandler):
    
    def __init__(self, *args):
        self.database = RestaurantDatabase()
        BaseHTTPRequestHandler.__init__(self, *args)
    
    def do_POST(self):
        css = """
        <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            margin: 0;
            padding: 0;
        }
        header {
            background-color: #333;
            color: white;
            padding: 10px 0;
            text-align: center;
        }
        header h1 {
            margin: 0;
        }
        nav {
            margin: 20px 0;
            text-align: center;
        }
        nav a {
            margin: 0 10px;
            text-decoration: none;
            color: #333;
            font-weight: bold;
        }
        nav a:hover {
            color: #007BFF;
        }
        .container {
            width: 80%;
            margin: 20px auto;
            padding: 20px;
            background: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        form {
            margin: 20px 0;
        }
        form input[type="text"], form input[type="number"], form input[type="datetime-local"] {
            width: calc(100% - 22px);
            padding: 10px;
            margin-bottom: 10px;
        }
        form input[type="submit"] {
            padding: 10px 20px;
            background-color: #007BFF;
            color: white;
            border: none;
            cursor: pointer;
        }
        form input[type="submit"]:hover {
            background-color: #0056b3;
        }
        </style>
        """

        try:
            if self.path == '/addReservation':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                customer_name = form.getvalue("customer_name")
                contact_info = form.getvalue("contact_info")
                reservation_time = form.getvalue("reservation_time")
                number_of_guests = int(form.getvalue("number_of_guests"))
                special_requests = form.getvalue("special_requests")
                
                # Add a new reservation using data from the form
                self.database.addReservation(customer_name, contact_info, reservation_time, number_of_guests, special_requests)
                
                self.wfile.write(b"<html><head><title>Restaurant Portal</title>" + css.encode() + b"</head>")
                self.wfile.write(b"<body><header><h1>Restaurant Portal</h1></header>")
                self.wfile.write(b"<nav><a href='/'>Home</a>|<a href='/addReservation'>Add Reservation</a>|<a href='/viewReservations'>View Reservations</a>|<a href='/viewCustomers'>View Customers</a></nav>")
                self.wfile.write(b"<div class='container'><h3>Reservation has been added</h3>")
                self.wfile.write(b"<div><a href='/addReservation'>Add Another Reservation</a></div></div>")
                self.wfile.write(b"</body></html>")
                
            elif self.path == '/deleteReservation':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                reservation_id = int(form.getvalue("reservation_id"))
                
                # Delete a reservation using the provided reservation ID
                self.database.deleteReservation(reservation_id)
                
                self.wfile.write(b"<html><head><title>Restaurant Portal</title>" + css.encode() + b"</head>")
                self.wfile.write(b"<body><header><h1>Restaurant Portal</h1></header>")
                self.wfile.write(b"<nav><a href='/'>Home</a>|<a href='/addReservation'>Add Reservation</a>|<a href='/viewReservations'>View Reservations</a>|<a href='/viewCustomers'>View Customers</a></nav>")
                self.wfile.write(b"<div class='container'><h3>Reservation has been deleted</h3>")
                self.wfile.write(b"<div><a href='/viewReservations'>View Reservations</a></div></div>")
                self.wfile.write(b"</body></html>")

            elif self.path == '/modifyReservation':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                reservation_id = int(form.getvalue("reservation_id"))
                customer_id = int(form.getvalue("customer_id"))
                reservation_time = form.getvalue("reservation_time")
                number_of_guests = int(form.getvalue("number_of_guests"))
                special_requests = form.getvalue("special_requests")
                
                # Modify an existing reservation using the provided details
                self.database.modifyReservation(reservation_id, customer_id, reservation_time, number_of_guests, special_requests)
                
                self.wfile.write(b"<html><head><title>Restaurant Portal</title>" + css.encode() + b"</head>")
                self.wfile.write(b"<body><header><h1>Restaurant Portal</h1></header>")
                self.wfile.write(b"<nav><a href='/'>Home</a>|<a href='/addReservation'>Add Reservation</a>|<a href='/viewReservations'>View Reservations</a>|<a href='/viewCustomers'>View Customers</a></nav>")
                self.wfile.write(b"<div class='container'><h3>Reservation has been modified</h3>")
                self.wfile.write(b"<div><a href='/viewReservations'>View Reservations</a></div></div>")
                self.wfile.write(b"</body></html>")

            elif self.path == '/deleteCustomer':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                customer_id = int(form.getvalue("customer_id"))
                
                # Delete a customer using the provided customer ID
                self.database.deleteCustomer(customer_id)
                
                self.wfile.write(b"<html><head><title>Restaurant Portal</title>" + css.encode() + b"</head>")
                self.wfile.write(b"<body><header><h1>Restaurant Portal</h1></header>")
                self.wfile.write(b"<nav><a href='/'>Home</a>|<a href='/addReservation'>Add Reservation</a>|<a href='/viewReservations'>View Reservations</a>|<a href='/viewCustomers'>View Customers</a></nav>")
                self.wfile.write(b"<div class='container'><h3>Customer has been deleted</h3>")
                self.wfile.write(b"<div><a href='/viewCustomers'>View Customers</a></div></div>")
                self.wfile.write(b"</body></html>")

            elif self.path == '/modifyCustomer':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                customer_id = int(form.getvalue("customer_id"))
                customer_name = form.getvalue("customer_name")
                contact_info = form.getvalue("contact_info")
                favorite_table = form.getvalue("favorite_table")
                dietary_restrictions = form.getvalue("dietary_restrictions")
                
                # Modify customer details and preferences using provided data
                self.database.modifyCustomer(customer_id, customer_name, contact_info)
                self.database.modifyCustomerPreferences(customer_id, favorite_table, dietary_restrictions)
                
                self.wfile.write(b"<html><head><title>Restaurant Portal</title>" + css.encode() + b"</head>")
                self.wfile.write(b"<body><header><h1>Restaurant Portal</h1></header>")
                self.wfile.write(b"<nav><a href='/'>Home</a>|<a href='/addReservation'>Add Reservation</a>|<a href='/viewReservations'>View Reservations</a>|<a href='/viewCustomers'>View Customers</a></nav>")
                self.wfile.write(b"<div class='container'><h3>Customer has been modified</h3>")
                self.wfile.write(b"<div><a href='/viewCustomers'>View Customers</a></div></div>")
                self.wfile.write(b"</body></html>")

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
        return
    
    def do_GET(self):
        css = """
        <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            margin: 0;
            padding: 0;
        }
        header {
            background-color: #333;
            color: white;
            padding: 10px 0;
            text-align: center;
        }
        header h1 {
            margin: 0;
        }
        nav {
            margin: 20px 0;
            text-align: center;
        }
        nav a {
            margin: 0 10px;
            text-decoration: none;
            color: #333;
            font-weight: bold;
        }
        nav a:hover {
            color: #007BFF;
        }
        .container {
            width: 80%;
            margin: 20px auto;
            padding: 20px;
            background: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        form {
            margin: 20px 0;
        }
        form input[type="text"], form input[type="number"], form input[type="datetime-local"] {
            width: calc(100% - 22px);
            padding: 10px;
            margin-bottom: 10px;
        }
        form input[type="submit"] {
            padding: 10px 20px;
            background-color: #007BFF;
            color: white;
            border: none;
            cursor: pointer;
        }
        form input[type="submit"]:hover {
            background-color: #0056b3;
        }
        </style>
        """

        try:
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title>Restaurant Portal</title>" + css.encode() + b"</head>")
                self.wfile.write(b"<body><header><h1>Welcome to the Restaurant Portal</h1></header>")
                self.wfile.write(b"<nav><a href='/'>Home</a>|<a href='/addReservation'>Add Reservation</a>|<a href='/viewReservations'>View Reservations</a>|<a href='/viewCustomers'>View Customers</a></nav>")
                self.wfile.write(b"<div class='container'><h2>Manage your restaurant reservations and customer information.</h2>")
                self.wfile.write(b"<p>Use the links above to navigate through the portal. You can add, view, modify, and delete reservations and customer details.</p>")
                self.wfile.write(b"<p>This portal helps restaurant managers streamline their operations and provide excellent service to their customers.</p></div>")
                self.wfile.write(b"</body></html>")
                return
            
            if self.path == '/addReservation':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title>Add Reservation</title>" + css.encode() + b"</head>")
                self.wfile.write(b"<body><header><h1>Add Reservation</h1></header>")
                self.wfile.write(b"<nav><a href='/'>Home</a>|<a href='/addReservation'>Add Reservation</a>|<a href='/viewReservations'>View Reservations</a>|<a href='/viewCustomers'>View Customers</a></nav>")
                self.wfile.write(b"<div class='container'><form action='/addReservation' method='post'>")
                self.wfile.write(b"Customer Name: <input type='text' name='customer_name'><br>")
                self.wfile.write(b"Contact Info: <input type='text' name='contact_info'><br>")
                self.wfile.write(b"Reservation Time: <input type='datetime-local' name='reservation_time'><br>")
                self.wfile.write(b"Number of Guests: <input type='number' name='number_of_guests'><br>")
                self.wfile.write(b"Special Requests: <input type='text' name='special_requests'><br>")
                self.wfile.write(b"<input type='submit' value='Add Reservation'></form></div>")
                self.wfile.write(b"</body></html>")
                return
            
            if self.path == '/viewReservations':
                data = []
                records = self.database.getAllReservations()
                data = records
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title>View Reservations</title>" + css.encode() + b"</head>")
                self.wfile.write(b"<body><header><h1>View Reservations</h1></header>")
                self.wfile.write(b"<nav><a href='/'>Home</a>|<a href='/addReservation'>Add Reservation</a>|<a href='/viewReservations'>View Reservations</a>|<a href='/viewCustomers'>View Customers</a></nav>")
                self.wfile.write(b"<div class='container'><h2>All Reservations</h2>")
                self.wfile.write(b"<table><tr><th>Reservation ID</th><th>Customer ID</th><th>Reservation Time</th><th>Number of Guests</th><th>Special Requests</th><th>Actions</th></tr>")
                for row in data:
                    self.wfile.write(b'<tr><td>')
                    self.wfile.write(str(row[0]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[1]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[2]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[3]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[4]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(b"<form action='/modifyReservation' method='post' style='display:inline;'>")
                    self.wfile.write(b"<input type='hidden' name='reservation_id' value='")
                    self.wfile.write(str(row[0]).encode())
                    self.wfile.write(b"'><br>Customer ID: <input type='number' name='customer_id' value='")
                    self.wfile.write(str(row[1]).encode())
                    self.wfile.write(b"'><br>Reservation Time: <input type='datetime-local' name='reservation_time' value='")
                    self.wfile.write(str(row[2]).encode())
                    self.wfile.write(b"'><br>Number of Guests: <input type='number' name='number_of_guests' value='")
                    self.wfile.write(str(row[3]).encode())
                    self.wfile.write(b"'><br>Special Requests: <input type='text' name='special_requests' value='")
                    self.wfile.write(str(row[4]).encode())
                    self.wfile.write(b"'><br><input type='submit' value='Modify'></form>")
                    self.wfile.write(b"<form action='/deleteReservation' method='post' style='display:inline;'>")
                    self.wfile.write(b"<input type='hidden' name='reservation_id' value='")
                    self.wfile.write(str(row[0]).encode())
                    self.wfile.write(b"'><input type='submit' value='Delete'></form></td></tr>")
                
                self.wfile.write(b"</table></div>")
                self.wfile.write(b"</body></html>")
                return

            if self.path == '/deleteCustomer':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title>Delete Customer</title>" + css.encode() + b"</head>")
                self.wfile.write(b"<body><header><h1>Delete Customer</h1></header>")
                self.wfile.write(b"<nav><a href='/'>Home</a>|<a href='/addReservation'>Add Reservation</a>|<a href='/viewReservations'>View Reservations</a>|<a href='/viewCustomers'>View Customers</a></nav>")
                self.wfile.write(b"<div class='container'><form action='/deleteCustomer' method='post'>")
                self.wfile.write(b"Customer ID: <input type='number' name='customer_id'><br>")
                self.wfile.write(b"<input type='submit' value='Delete Customer'></form></div>")
                self.wfile.write(b"</body></html>")
                return

            if self.path == '/modifyCustomer':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title>Modify Customer</title>" + css.encode() + b"</head>")
                self.wfile.write(b"<body><header><h1>Modify Customer</h1></header>")
                self.wfile.write(b"<nav><a href='/'>Home</a>|<a href='/addReservation'>Add Reservation</a>|<a href='/viewReservations'>View Reservations</a>|<a href='/viewCustomers'>View Customers</a></nav>")
                self.wfile.write(b"<div class='container'><form action='/modifyCustomer' method='post'>")
                self.wfile.write(b"Customer ID: <input type='number' name='customer_id'><br>")
                self.wfile.write(b"Customer Name: <input type='text' name='customer_name'><br>")
                self.wfile.write(b"Contact Info: <input type='text' name='contact_info'><br>")
                self.wfile.write(b"Favorite Table: <input type='text' name='favorite_table'><br>")
                self.wfile.write(b"Dietary Restrictions: <input type='text' name='dietary_restrictions'><br>")
                self.wfile.write(b"<input type='submit' value='Modify Customer'></form></div>")
                self.wfile.write(b"</body></html>")
                return

            if self.path == '/viewCustomers':
                data = []
                records = self.database.getAllCustomersWithPreferences()
                data = records
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title>View Customers</title>" + css.encode() + b"</head>")
                self.wfile.write(b"<body><header><h1>View Customers</h1></header>")
                self.wfile.write(b"<nav><a href='/'>Home</a>|<a href='/addReservation'>Add Reservation</a>|<a href='/viewReservations'>View Reservations</a>|<a href='/viewCustomers'>View Customers</a></nav>")
                self.wfile.write(b"<div class='container'><h2>All Customers</h2>")
                self.wfile.write(b"<table><tr><th>Customer ID</th><th>Customer Name</th><th>Contact Info</th><th>Favorite Table</th><th>Dietary Restrictions</th><th>Actions</th></tr>")
                for row in data:
                    self.wfile.write(b'<tr><td>')
                    self.wfile.write(str(row[0]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[1]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[2]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[3]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[4]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(b"<form action='/modifyCustomer' method='post' style='display:inline;'>")
                    self.wfile.write(b"<input type='hidden' name='customer_id' value='")
                    self.wfile.write(str(row[0]).encode())
                    self.wfile.write(b"'><br>Name: <input type='text' name='customer_name' value='")
                    self.wfile.write(str(row[1]).encode())
                    self.wfile.write(b"'><br>Contact: <input type='text' name='contact_info' value='")
                    self.wfile.write(str(row[2]).encode())
                    self.wfile.write(b"'><br>Favorite Table: <input type='text' name='favorite_table' value='")
                    self.wfile.write(str(row[3]).encode())
                    self.wfile.write(b"'><br>Dietary Restrictions: <input type='text' name='dietary_restrictions' value='")
                    self.wfile.write(str(row[4]).encode())
                    self.wfile.write(b"'><br><input type='submit' value='Modify'></form>")
                    self.wfile.write(b"<form action='/deleteCustomer' method='post' style='display:inline;'>")
                    self.wfile.write(b"<input type='hidden' name='customer_id' value='")
                    self.wfile.write(str(row[0]).encode())
                    self.wfile.write(b"'><input type='submit' value='Delete'></form></td></tr>")
                
                self.wfile.write(b"</table></div>")
                self.wfile.write(b"</body></html>")
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

def run(server_class=HTTPServer, handler_class=RestaurantPortalHandler, port=8000):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()

run()