from flask import Flask, redirect, request, render_template, jsonify, make_response
import pandas as pd
import io
from unidecode import unidecode #ASCII conversion
import requests
import os
import googlemaps  #for Google Maps API integration
import bleach #for sanitizing inputs before rendering or saving them to the db

# Initialize Google Maps client with API key
API_KEY = '__secret'  #restricted only to this url: https://address-book-webapp-fdb2ba8061bc.herokuapp.com/
map_client = googlemaps.Client(key=API_KEY)

# Initialize the Flask application
app = Flask(__name__)

# In-memory DataFrame to store processed data with specified columns
processed_data_storage = pd.DataFrame(columns=['Name', 'Address'])

@app.route('/', methods=['GET'])
def index():
    # Render and return the main page HTML template
    return render_template('index.html')

"""# GET | API
def get_geolocation(address):
    print(f"Getting the address: {address}")
    #Query PositionStack API for geolocation data of the given address.
    # API key (I can use environment variables for storing API keys in production)
    API_KEY = '__secret'
    BASE_URL = 'http://api.positionstack.com/v1/forward'
    params = {
        'access_key': API_KEY,  # Authentication parameter
        'query': address,  # Address query parameter
        'limit': 1,  # Limit results to the top result
    }
    try:
        # Make a GET request to the PositionStack API
        response = requests.get(BASE_URL, params=params) #bg data though..
        # If the request is not successful, this will raise an HTTPError
        response.raise_for_status()
        # Parse the JSON response
        data = response.json()
        if data['data']:
            # Extract the most relevant location data
            location = data['data'][0]  
            ##print(f"Retrieved location: {location}")  # Debugging print statement
            # return f"{location.get('name', '')}, {location.get('region', '')}, {location.get('country', '')}, {location.get('street', '')}, {location.get('latitude', '')}, {location.get('longitude', ''),} "
            return {
                'formatted_address': f"{location.get('name', '')}, {location.get('region', '')}, {location.get('country', '')}, {location.get('street', '')}",
                'latitude': location.get('latitude'),
                'longitude': location.get('longitude')
            }
            
    except requests.RequestException as e:
        # Log any errors encountered during the API request
        print(f"Error querying PositionStack API: {e}")
    return None"""

#GOOGLE API
# GET | API
def get_geolocation(address):
    print(f"Getting the address: {address}")
    """Query Google Maps Geocoding API for geolocation data of the given address."""
    try:
        # Make a request to the Google Maps Geocoding API
        response = map_client.geocode(address)
        if response:
            # Extract the most relevant location data
            location = response[0]  # Take the first result
            #print(f"Retrieved location: {location}")
            formatted_address = location['formatted_address']
            latitude = location['geometry']['location']['lat']
            longitude = location['geometry']['location']['lng']
            return {
                'formatted_address': formatted_address,
                'latitude': latitude,
                'longitude': longitude
            }
    except Exception as e:
        # Log any errors encountered during the API request
        print(f"Error querying Google Maps Geocoding API: {e}")
    return None

#------------------------------------------
# POST (check script.js)
@app.route('/process', methods=['POST'])
def process():
    """Process uploaded data (either from a file or text input) and return processed results."""
    global processed_data_storage  # Reference the global storage variable

    # Check for file upload
    file = request.files.get('csvfile1')
    if file and file.filename != '':
        # Read the uploaded CSV file into a DataFrame
        dataframe = pd.read_csv(file)
        # Sanitize data
        dataframe['Name'] = dataframe['Name'].apply(lambda x: bleach.clean(x))
        dataframe['Address'] = dataframe['Address'].apply(lambda x: bleach.clean(x))
        print("Processing uploaded CSV file...") 
    
    # Process text input    
    else:
        text_data = request.form.get('textinput')
        if text_data:
            try:
                # Differentiate between single line and multiline text input
                if ',' not in text_data or '\n' not in text_data:  # Single line input
                    name, address = text_data.split(',', 1)
                    #Sanitize
                    name = bleach.clean(name.strip())
                    address = bleach.clean(address.strip())
                    dataframe = pd.DataFrame([[name.strip(), address.strip()]], columns=['Name', 'Address'])
                else:  # Multiline (CSV formatted) text input
                    text_io = io.StringIO(text_data)
                    dataframe = pd.read_csv(text_io, lineterminator='\n')
                    #Clean/Sanitize from mal script
                    dataframe['Name'] = dataframe['Name'].apply(lambda x: bleach.clean(x))
                    dataframe['Address'] = dataframe['Address'].apply(lambda x: bleach.clean(x))
                print("Processing text input.") 
                print(f"Data frame {dataframe}")
            except Exception as e:
                # Log any errors encountered during processing
                print(f"Error processing input: {e}")
                return jsonify({'error': str(e)}), 400
        else:
            return jsonify({'error': 'No data provided'}), 400

  
    # Normalize and verify addresses using PositionStack API
    for index, row in dataframe.iterrows():
        #Get loc.
        geolocation_result = get_geolocation(row['Address'])
        if geolocation_result:
            # Combined formatted address with longitude and latitude for testing
            normalized_address = f"{geolocation_result['formatted_address']}, Lat: {geolocation_result['latitude']}, Lng: {geolocation_result['longitude']}"
            dataframe.at[index, 'Address'] = normalized_address
            # print(dataframe)
            print(f"READY & Normalized address for {row['Name']}: {normalized_address}")

    # Combine the new entries with the existing data and sort
    processed_data_storage = pd.concat([processed_data_storage, dataframe])
    # Sort
    processed_data_storage = group_and_sort(processed_data_storage)  
    # Prepare and return the result, excluding the 'Address' column
    result = processed_data_storage.drop(columns=['Address']).to_dict(orient='records')
    return jsonify(result)
#------------------------------------------

@app.route('/download-txt', methods=['GET'])
def download_txt():
    """Allow users to download the processed data as a text file."""
    global processed_data_storage

    if not processed_data_storage.empty:
        buffer = io.StringIO()
        
        # Write the grouped and sorted names to the buffer
        for _, group in processed_data_storage.groupby('Address'):
            buffer.write(', '.join(sorted(group['Name'])) + '\n')
        
        buffer.seek(0)
        response= make_response(buffer.getvalue())
        buffer.close()

        # Set headers for file download
        response.headers['Content-Disposition'] = 'attachment; filename=grouped_names.txt'
        response.headers['Content-Type'] = 'text/plain'
        return response

    return jsonify({'error': 'No data to download'}), 404

def group_and_sort(df):
    """Sort and group data by address, then sort each group's names alphabetically."""
    df.sort_values(by='Address', inplace=True)
    grouped = df.groupby('Address')['Name'].apply(lambda names: ', '.join(sorted(names))).reset_index()
    # Sort groups by the first name in each group for alphabetical ordering
    grouped['First_Name'] = grouped['Name'].apply(lambda x: x.split(', ')[0])
    grouped.sort_values(by='First_Name', inplace=True)
    grouped.drop(columns=['First_Name'], inplace=True)
    print("Data grouped and sorted.")  # Debugging print statement
    return grouped

@app.route('/reset', methods=['GET'])
def reset_data():
    """Reset the stored data to an empty DataFrame and redirect to the home route."""
    global processed_data_storage
    processed_data_storage = pd.DataFrame(columns=['Name', 'Address'])
    print("Data storage reset.")  # Debugging print statement
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)  #Heroku expects to bind to a port number specified by the PORT environment variable. 
