# Movie Collection Manager

A Python application to manage your movie collection with data from OMDb API.

## Features

- Add movies by title (data fetched from OMDb API)
- List, search, and sort your movie collection
- Generate a beautiful website to showcase your movies
- Store data in JSON or CSV format

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

All data files are stored in the `data/` directory, which is automatically created when the application runs.

## Environment Variables

Create a `.env` file with your OMDb API key:

```
API_KEY=your_api_key_here
```

Get your API key from [OMDb API](http://www.omdbapi.com/apikey.aspx)
