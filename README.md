## Trade API with FastAPI
This project is a REST API built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python. The API serves trade data from a mocked database and provides various endpoints for retrieving, searching, and filtering trades.

## Features

* ***Listing Trade*** : Fetch a list of trades with support for pagination and sorting.
* ***Single Trade*** : Retrieve a single trade by its ID.
* ***Searching Trades*** : Search for trades using query parameters to filter by counterparty, instrument ID, instrument name, and trader.
* ***Advanced Filtering*** : Filter trades by asset class, trade date-time range, trade type (buy or sell), and price range.
* ***Pagination and Sorting*** : Supports pagination with customizable page size and sorting based on various trade attributes.
* ***Mocked Database*** : Implements a mocked database interaction layer to generate random trade data for testing and demonstration purposes.

## Technologies Used
* ***FastAPI*** : A modern, fast (high-performance), web framework for building APIs with Python.
* ***Pydantic*** : A library for data validation and parsing using Python type annotations.
* ***Uvicorn*** : An ASGI server for running FastAPI applications.
* ***Git*** : Version control system for managing the project's source code.

## Getting Started
To get started with the project:

* Clone the repository: git clone <repository-url>
* Install the project dependencies: pip install -r requirements.txt
* Run the API server: python main.py
* Access the API endpoints locally: http://localhost:8000/
* For detailed documentation on the API endpoints, usage examples, and query parameters, refer to the API Documentation file.
  
## Contributions
Contributions are welcome! If you find any issues, have suggestions for improvements, or want to add new features, feel free to open an issue or submit a pull request.
