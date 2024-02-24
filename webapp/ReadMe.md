# Address Book Web Application

Deployed here: 

## Overview

This project is a web-based application designed to normalize and sort by name address data input by users. 
Utilizing Flask for the backend, JavaScript for asynchronous web interactions, and the PositionStack API for address normalization and geolocation, it shows modern web application development practices. 

## Features

- **Address Normalization**: Converts input addresses into a standardized geolocation in JSON format using PositionStack API.
- **Data Sorting**: Organizes names associated with identical addresses in alphabetical order.
- **File Upload**: Supports CSV file uploads for bulk and multyline address processing.
- **Interactive Web Interface**: Offers a dynamic user experience without page reloads for data submission and downloads + data storage reset option.

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Data Processing**: Pandas (Python)
- **API**: PositionStack for geolocation services
- **Deployment**: Heroku CLI

## Getting Started

### Installation

1. Clone the repository:

```
git clone https://github.com/filipfilchev/address-book
```
2. Navigate to the project directory and install Python dependencies:

```
cd webapp
pip install flask pandas requests unidecode
python3 app.py

```

## Usage

After starting the server, the web application will be accessible at http://localhost:5000. Users can enter addresses directly or upload a CSV file, then preview on the UI or download the processed data.

## Deployment to Heroku

1. Create a Procfile with the content: web: python app.py, which tells Heroku to run the app.py Flask server.
2. Install the Heroku CLI and log in using ```heroku login```
3. Create a new Heroku app with ```heroku create```
4. Initialize a git repo

```
cd webapp
git init 
heroku git:remote -a address-book-webapp
git add .
git commit -m "source code commited"
```
5. To link the git repo to the Heroku app -> ```heroku git:remote -a address-book-webapp```
6. Deploy with ```git push heroku master```
7. Test Locally: ```heroku local web```


## Contributing

You are welcome to contribute! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your features or fixes.
3. Submit a pull request with a description of changes.


## License

Distributed under the MIT License. See LICENSE for more information.


### For more info about this app read the requirements -> ReadRequirements.txt