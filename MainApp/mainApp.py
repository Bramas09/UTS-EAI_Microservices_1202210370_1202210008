from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

# layanan destination
def get_destination(DestinationID=None):
    url = f'http://localhost:5000/destination/'
    if DestinationID is not None:
        url += str(DestinationID)
    response = requests.get(url)
    return response.json()

# layanan bookings
def get_booking(BookingID=None):
    url = f'http://localhost:5001/booking/destination/'
    if BookingID is not None:
        url += str(BookingID)
    response = requests.get(url)
    return response.json()

def get_detail_booking(BookingID=None):
    url = f'http://localhost:5001/detailbooking/destination/'
    if BookingID is not None:
        url += str(BookingID)
    response = requests.get(url)
    return response.json()


#Routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/destination')
def get_destination_list():
    destination_list = get_destination(DestinationID=None)
    return render_template('DestinationList.html', detail=destination_list)

@app.route('/destination/<int:DestinationID>')
def get_destination_info(DestinationID):
    destination = get_destination(DestinationID)
    return render_template('DetailDestination.html', detail=destination)

@app.route('/booking')
def get_booking_list():
    booking_list = get_booking(BookingID=None)
    return render_template('Booking.html', result=booking_list) 

@app.route('/detailbooking/<int:BookingID>')
def get_booking_info(BookingID):
    booking_detail = get_detail_booking(BookingID)
    return render_template('DetailBooking.html', result=booking_detail)



if __name__ == "__main__" :
    app.run (debug=True, port=5003)