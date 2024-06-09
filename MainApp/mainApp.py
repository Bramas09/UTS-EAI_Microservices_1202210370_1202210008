from flask import Flask, jsonify, render_template, redirect, url_for, request
import requests
from requests.exceptions import HTTPError, JSONDecodeError

app = Flask(__name__)

def post_customer(data):
    url = 'http://localhost:5000/create-customer'
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except JSONDecodeError as json_err:
        print(f'JSON decoding error occurred: {json_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return None

# Service functions for bookings
def post_booking(result):
    url = 'http://localhost:5000/create-booking/'
    try:
        response = requests.post(url, json=result)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except JSONDecodeError as json_err:
        print(f'JSON decoding error occurred: {json_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return None

def get_booking(BookingID=None):
    url = 'http://localhost:5000/show-booking/'
    if BookingID is not None:
        url += str(BookingID)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except JSONDecodeError as json_err:
        print(f'JSON decoding error occurred: {json_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return []

def update_booking(BookingID, result):
    url = f'http://localhost:5000/update-booking/{BookingID}'
    try:
        response = requests.put(url, json=result)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except JSONDecodeError as json_err:
        print(f'JSON decoding error occurred: {json_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return None

def delete_booking(BookingID):
    url = f'http://localhost:5000/delete-booking/{BookingID}'
    try:
        response = requests.delete(url)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except JSONDecodeError as json_err:
        print(f'JSON decoding error occurred: {json_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return None

# Service functions for destinations
def post_destination(result):
    url = 'http://localhost:5001/destinations/'
    try:
        response = requests.post(url, json=result)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except JSONDecodeError as json_err:
        print(f'JSON decoding error occurred: {json_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return None

def get_destination(DestinationID=None):
    url = 'http://localhost:5001/destinations/'
    if DestinationID is not None:
        url += str(DestinationID)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except JSONDecodeError as json_err:
        print(f'JSON decoding error occurred: {json_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return []

def update_destination(DestinationID, result):
    url = f'http://localhost:5001/destinations/{DestinationID}'
    try:
        response = requests.put(url, json=result)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except JSONDecodeError as json_err:
        print(f'JSON decoding error occurred: {json_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return None

def delete_destination(DestinationID):
    url = f'http://localhost:5001/destinations/{DestinationID}'
    try:
        response = requests.delete(url)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except JSONDecodeError as json_err:
        print(f'JSON decoding error occurred: {json_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return None

# Routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-booking', methods=['GET', 'POST'])
def create_booking():
    if request.method == 'POST':
        customer_data = {
            "CustomerID": request.form['CustomerID'],
            "CustomerName": request.form['CustomerName'],
            "NIK": request.form['NIK'],
            "Email": request.form['Email'],
            "Address": request.form['Address']
        }
        destination_id = request.form['DestinationID']
        booking_id = request.form['BookingID']
        
        create_customer_result = post_customer(customer_data)
        if create_customer_result:
            booking_data = {
                "BookingID": booking_id,
                "CustomerID": customer_data['CustomerID'],
                "DestinationID": destination_id
            }
            create_booking_result = post_booking(booking_data)
            if create_booking_result:
                return redirect(url_for('get_booking_info', BookingID=create_booking_result['BookingID']))
        return "Failed to create booking"
    
    destination_id = request.args.get('DestinationID')
    destination = get_destination(destination_id)
    return render_template('CreateBooking.html', destination=destination)

@app.route('/show-booking')
def get_booking_list():
    booking_list = get_booking()
    return render_template('BookingList.html', detail=booking_list)

@app.route('/show-booking/<int:BookingID>')
def get_booking_info(BookingID):
    detail_booking = get_booking(BookingID)
    return render_template('DetailBooking.html', detail=detail_booking)

@app.route('/update-booking/<int:BookingID>', methods=['GET', 'POST'])
def update_booking_info(BookingID):
    if request.method == 'POST':
        result = request.form.to_dict()
        update_booking_result = update_booking(BookingID, result)
        if update_booking_result:
            return redirect(url_for('get_booking_info', BookingID=update_booking_result['BookingID']))
        else:
            return "Failed to update booking"
    detail_booking = get_booking(BookingID)
    return render_template('UpdateBooking.html', detail=detail_booking)

@app.route('/delete-booking/<int:BookingID>')
def delete_booking_info(BookingID):
    delete_booking_result = delete_booking(BookingID)
    if delete_booking_result and 'BookingID' in delete_booking_result:
        return redirect(url_for('get_booking_list'))
    else:
        return "Error: Failed to delete booking"

@app.route('/create-destination', methods=['GET', 'POST'])
def create_destination():
    if request.method == 'POST':
        result = request.form.to_dict()
        create_destination_result = post_destination(result)
        if create_destination_result:
            return redirect(url_for('get_destination_info', DestinationID=create_destination_result['DestinationID']))
        else:
            return "Failed to create destination"
    return render_template('CreateDestination.html')

@app.route('/show-destination')
def get_destination_list():
    destination_list = get_destination()
    return render_template('DestinationList.html', result=destination_list)

@app.route('/show-destination/<int:DestinationID>')
def get_destination_info(DestinationID):
    destination_detail = get_destination(DestinationID)
    return render_template('DetailDestination.html', result=destination_detail)

@app.route('/update-destination/<int:DestinationID>', methods=['GET', 'POST'])
def update_destination_info(DestinationID):
    if request.method == 'POST':
        result = request.form.to_dict()
        update_destination_result = update_destination(DestinationID, result)
        if update_destination_result:
            return redirect(url_for('get_destination_info', DestinationID=DestinationID))
        else:
            return "Failed to update destination"
    destination_detail = get_destination(DestinationID)
    return render_template('UpdateDestination.html', result=destination_detail)

@app.route('/delete-destination/<int:DestinationID>')
def delete_destination_info(DestinationID):
    delete_destination_result = delete_destination(DestinationID)
    if delete_destination_result and 'DestinationID' in delete_destination_result:
        return redirect(url_for('get_destination_list'))
    else:
        return "Error: Failed to delete destination"

if __name__ == "__main__":
    app.run(debug=True, port=5003)
