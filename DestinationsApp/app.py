from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Provide your MySQL password here
    database="tourism"
)

# Function to close database connection
def close_db_connection(cursor):
    cursor.close()

@app.route('/')
def root():
    return 'Selamat Datang di App Booking Destinations'

@app.route('/destinations/', methods=['GET', 'POST'])
def destinations():
    cursor = db.cursor(dictionary=True)
    if request.method == 'GET':
        try: 
            cursor.execute("SELECT * FROM destinations ORDER BY DestinationName ASC")
            result = cursor.fetchall()
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            close_db_connection(cursor)

    elif request.method == 'POST':
        try:
            result = request.json
            sql = "INSERT INTO destinations (DestinationID, DestinationName, Location, Rating, Viewers, Price) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (result['DestinationID'], result['DestinationName'], result['Location'], result['Rating'], result['Viewers'], result['Price'])
            cursor.execute(sql, val)
            db.commit()
            return jsonify({'message': 'Data Berhasil Ditambahkan', 'DestinationID': cursor.lastrowid})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            close_db_connection(cursor)

@app.route('/destinations/<int:DestinationID>', methods=['GET', 'DELETE', 'PUT'])
def detaildestination(DestinationID):
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM destinations WHERE DestinationID = %s", (DestinationID,))
            data = cursor.fetchone()
            if data:
                return jsonify(data)
            else:
                return jsonify({'message': 'produk tidak ditemukan'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            close_db_connection(cursor)

    elif request.method == 'DELETE':
        try:
            cursor.execute("DELETE FROM destinations WHERE DestinationID = %s", (DestinationID,))
            db.commit()
            return jsonify({'DestinationID': DestinationID, 'message': 'Data Berhasil Dihapus'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            close_db_connection(cursor)

    elif request.method == 'PUT':
        try:
            result = request.json
            sql = "UPDATE destinations SET DestinationName=%s, Location=%s, Rating=%s, Viewers=%s, Price=%s WHERE DestinationID = %s"
            val = (result['DestinationName'], result['Location'], result['Rating'], result['Viewers'], result['Price'], DestinationID)
            cursor.execute(sql, val)
            db.commit()
            return jsonify({'message': 'Data Berhasil Diupdate'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            close_db_connection(cursor)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
