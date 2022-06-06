import streamlit as st
import requests
import datetime

'''
# Taxi fare prediction - demo app
'''
url_location = "https://nominatim.openstreetmap.org/search"
url_predict = "https://taxifare.lewagon.ai/predict"

# function to
@st.cache()
def get_location(location_input):
    # return a list of an empty dict if no text is provided
    if location_input == '':
        return [{}]

    response_pickup = requests.get(url_location,
                                   params = {'q':location_input,
                                             'format':'jsonv2'})
    if response_pickup.status_code == 200:
        pickup_output = response_pickup.json()
        return pickup_output
    # return list of an empty dict if GET request fails
    else:
        return [{}]

############# Get inputs #################

# get pickup location
pickup_inp = st.text_input("Pickup Location:", "")
pickup_out = get_location(pickup_inp)
st.write(pickup_out[0].get('display_name', ''))

# get dropoff location
dropoff_inp = st.text_input("Dropoff Location:", "")
dropoff_out = get_location(dropoff_inp)
st.write(dropoff_out[0].get('display_name', ''))

# pickup date, time and number of passengers
columns_dt = st.columns([1, 1, 2])
# pickup date
pickup_d = columns_dt[0].date_input("Pickup Date:",
                            datetime.date.today())
# pickup time
pickup_t = columns_dt[1].time_input("Pickup Time:",
                            datetime.datetime.now())
# slider for number of passengers
pax = columns_dt[2].slider('Number of passengers', 1, 8, 1)
st.write(f'### Picking up {pax} passengers on {pickup_d} {pickup_t}')

########### Obtain parameters for prediction ##################

# store pickup coordinates
pickup_lat = pickup_out[0].get('lat', 0)
pickup_lon = pickup_out[0].get('lon', 0)
# store pickup coordinates
dropoff_lat = dropoff_out[0].get('lat', 0)
dropoff_lon = dropoff_out[0].get('lon', 0)

# input params
params = {
    "pickup_latitude": pickup_lat,
    "pickup_longitude": pickup_lon,
    "dropoff_latitude": dropoff_lat,
    "dropoff_longitude": dropoff_lon,
    "passenger_count": pax,
    "pickup_datetime": f"{pickup_d} {pickup_t}"
}

############# Obtain prediction #######################

# call prediction API and retrieve the JSON from the response
if st.button('Get fare estimate'):
    response_fare = requests.get(url_predict, params=params)

    # extract the predicted fare
    if response_fare.status_code == 200:
        result_fare = response_fare.json()['fare']
        st.markdown(f"### Your estimated fare is: **${result_fare:.2f}**")
    else:
        st.warning("Something went wrong, please check your inputs and try again.")
