import mysql.connector
from mysql.connector import Error

class RestaurantDatabase():
    def __init__(self,
                 host="localhost",
                 port="3306",
                 database="restaurant_reservations",
                 user='root',
                 password='root'):

        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password)
            
            if self.connection.is_connected():
                print("Successfully connected to the database")
                return
        except Error as e:
            print("Error while connecting to MySQL", e)

    def addReservation(self, customer_name, contact_info, reservation_time, number_of_guests, special_requests):
        ''' Method to insert a new reservation, ensuring the customer exists '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "CALL addReservation(%s, %s, %s, %s, %s)"
            self.cursor.execute(query, (customer_name, contact_info, reservation_time, number_of_guests, special_requests))
            self.connection.commit()
            print("Reservation added successfully")
            return

    def getAllReservations(self):
        ''' Method to get all reservations from the reservations table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "SELECT * FROM Reservations"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records

    def addCustomer(self, customer_name, contact_info):
        ''' Method to add a new customer to the customers table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "INSERT INTO Customers (customerName, contactInfo) VALUES (%s, %s)"
            self.cursor.execute(query, (customer_name, contact_info))
            self.connection.commit()
            print("Customer added successfully")
            return

    def getAllCustomers(self):
        ''' Method to get all customers from the customers table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "SELECT * FROM Customers"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records

    def deleteCustomer(self, customer_id):
        ''' Method to delete a customer from the customers table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "DELETE FROM Customers WHERE customerId = %s"
            self.cursor.execute(query, (customer_id,))
            self.connection.commit()
            print("Customer deleted successfully")
            return

    def modifyCustomer(self, customer_id, customer_name, contact_info):
        ''' Method to modify a customer's details in the customers table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "UPDATE Customers SET customerName = %s, contactInfo = %s WHERE customerId = %s"
            self.cursor.execute(query, (customer_name, contact_info, customer_id))
            self.connection.commit()
            print("Customer modified successfully")
            return

    def modifyCustomerPreferences(self, customer_id, favorite_table, dietary_restrictions):
        ''' Method to modify a customer's dining preferences in the dining preferences table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = """
            INSERT INTO DiningPreferences (customerId, favoriteTable, dietaryRestrictions)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE favoriteTable = VALUES(favoriteTable), dietaryRestrictions = VALUES(dietaryRestrictions)
            """
            self.cursor.execute(query, (customer_id, favorite_table, dietary_restrictions))
            self.connection.commit()
            print("Customer preferences modified successfully")
            return

    def getCustomerPreferences(self, customer_id):
        ''' Method to retrieve dining preferences for a specific customer '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "SELECT * FROM DiningPreferences WHERE customerId = %s"
            self.cursor.execute(query, (customer_id,))
            preferences = self.cursor.fetchall()
            return preferences

    def findReservations(self, customer_id):
        ''' Method to find reservations for a specific customer '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "CALL findReservations(%s)"
            self.cursor.execute(query, (customer_id,))
            records = self.cursor.fetchall()
            return records

    def addSpecialRequest(self, reservation_id, requests):
        ''' Method to update the special requests for a specific reservation '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "CALL addSpecialRequest(%s, %s)"
            self.cursor.execute(query, (reservation_id, requests))
            self.connection.commit()
            print("Special request updated successfully")
            return

    def deleteReservation(self, reservation_id):
        ''' Method to delete a reservation from the reservations table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "DELETE FROM Reservations WHERE reservationId = %s"
            self.cursor.execute(query, (reservation_id,))
            self.connection.commit()
            print("Reservation deleted successfully")
            return

    def modifyReservation(self, reservation_id, customer_id, reservation_time, number_of_guests, special_requests):
        ''' Method to modify a reservation in the reservations table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = """
            UPDATE Reservations
            SET customerId = %s, reservationTime = %s, numberOfGuests = %s, specialRequests = %s
            WHERE reservationId = %s
            """
            self.cursor.execute(query, (customer_id, reservation_time, number_of_guests, special_requests, reservation_id))
            self.connection.commit()
            print("Reservation modified successfully")
            return

    def getAllCustomersWithPreferences(self):
        ''' Method to get all customers along with their dining preferences '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = """
            SELECT c.customerId, c.customerName, c.contactInfo, dp.favoriteTable, dp.dietaryRestrictions
            FROM Customers c
            LEFT JOIN DiningPreferences dp ON c.customerId = dp.customerId
            """
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records