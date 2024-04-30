from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="tourism"
)

# Function to close database connection
def close_db_connection(cursor):
    cursor.close()
    db.close()

# Get bookings with destination information for all bookings
@app.route('/booking/destination/')
def get_bookings_with_destination():
    try:
        with db.cursor() as cursor:
            sql = '''
                SELECT bookings.BookingID, customer.CustomerName, customer.Email, destinations.DestinationName, destinations.Location 
                FROM bookings 
                JOIN customer ON bookings.CustomerID = customer.CustomerID
                JOIN destinations ON bookings.DestinationID = destinations.DestinationID
                ORDER BY bookings.BookingID ASC
            '''
            cursor.execute(sql)
            result = cursor.fetchall()
            bookings = []
            for row in result:
                booking = {
                    'BookingID': row[0],
                    'CustomerName': row[1],
                    'Email': row[2],
                    'DestinationName': row[3],
                    'Location': row[4]
                }
                bookings.append(booking)
            return jsonify(bookings)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# Get bookings with destination information by BookingID
@app.route('/booking/destination/<int:BookingID>')
def get_bookings_with_destinationID(BookingID):
    try:
        with db.cursor() as cursor:
            sql = '''
                SELECT bookings.BookingID, customer.CustomerName, customer.Email, destinations.DestinationName, destinations.Location 
                FROM bookings 
                JOIN customer ON bookings.CustomerID = customer.CustomerID
                JOIN destinations ON bookings.DestinationID = destinations.DestinationID
                WHERE bookings.BookingID = %s
            '''
            cursor.execute(sql, (BookingID,))
            result = cursor.fetchone()
            if result:
                booking = {
                    'BookingID': result[0],
                    'CustomerName': result[1],
                    'Email': result[2],
                    'DestinationName': result[3],
                    'Location': result[4]
                }
                return jsonify(booking)
            else:
                return jsonify({"message": "Booking not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    



# Get detail bookings with destination information for all bookings
@app.route('/detailbooking/destination/')
def get_detail_bookings():
    try:
        with db.cursor() as cursor:
            sql = '''
                SELECT bookings.BookingID, customer.CustomerID, customer.CustomerName, customer.NIK, customer.Email, customer.Address, destinations.DestinationID, destinations.DestinationName, destinations.Location, destinations.Rating, destinations.Viewers, destinations.Price 
                FROM bookings 
                JOIN customer ON bookings.CustomerID = customer.CustomerID
                JOIN destinations ON bookings.DestinationID = destinations.DestinationID
                ORDER BY bookings.BookingID ASC
            '''
            cursor.execute(sql)
            result = cursor.fetchall()
            bookings = []
            for row in result:
                booking = {
                    'BookingID': row[0],
                    'CustomerID': row[1],
                    'CustomerName': row[2],
                    'NIK' : row[3],
                    'Email': row[4],
                    'Address' : row[5],
                    'DestinationID': row[6],
                    'DestinationName': row[7],
                    'Location': row[8],
                    'Rating': row[9],
                    'Viewers': row[10],
                    'Price': row[11]
                }
                bookings.append(booking)
            return jsonify(bookings)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# Get detail bookings with destination information by BookingID
@app.route('/detailbooking/destination/<int:BookingID>')
def get_booking_details(BookingID):
    try:
        with db.cursor() as cursor:
            sql = '''
                SELECT bookings.BookingID, customer.CustomerID, customer.CustomerName, customer.NIK, customer.Email, customer.Address, destinations.DestinationID, destinations.DestinationName, destinations.Location, destinations.Rating, destinations.Viewers, destinations.Price 
                FROM bookings 
                JOIN customer ON bookings.CustomerID = customer.CustomerID
                JOIN destinations ON bookings.DestinationID = destinations.DestinationID
                WHERE bookings.BookingID = %s
            '''
            cursor.execute(sql, (BookingID,))
            result = cursor.fetchone()
            if result:
                booking = {
                    'BookingID': result[0],
                    'CustomerID': result[1],
                    'CustomerName': result[2],
                    'NIK' : result[3],
                    'Email': result[4],
                    'Address' : result[5],
                    'DestinationID': result[6],
                    'DestinationName': result[7],
                    'Location': result[8],
                    'Rating': result[9],
                    'Viewers': result[10],
                    'Price': result[11]
                }
                return jsonify(booking)
            else:
                return jsonify({"message": "Booking not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
