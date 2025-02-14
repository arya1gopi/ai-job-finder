# Job Search Chatbot API

This Flask-based API enables users to search for job listings based on their queries and provides a chatbot-like interface for job-related intents (job search, location, skills). It utilizes Natural Language Processing (NLP) to identify the user's intent and scrape job listings from the Infopark website.

## Features

- **Intent Recognition**: Classifies user inputs into job-related intents (e.g., job search, location, skills).
- **Job Scraping**: Scrapes job listings from the Infopark website.
- **Named Entity Recognition (NER)**: Extracts entities like location and skills from user input.
- **CORS Support**: Allows cross-origin requests for easier integration with front-end applications.

## API Endpoints

### `POST /get_job_response`

This endpoint receives user input, processes it, and returns job-related information based on the recognized intent.

#### Request

- **Method**: `POST`
- **Content-Type**: `application/json`
- **Body**:

```json
{
  "user_input": "I am looking for a job in New York with Python skills"
}
```

#### Response

The API will return job information based on the recognized intent (job search, location, or skills) and the entities extracted from the user input.

##### For Job Search Intent

```json
{
  "jobs": [
    {
      "title": "Software Developer",
      "company": "Tech Co.",
      "date": "2025-01-25",
      "location": "New York",
      "skills": ["Python", "Django"],
      "link": "https://example.com/job/1"
    },
    {
      "title": "Python Developer",
      "company": "Dev Corp",
      "date": "2025-01-20",
      "location": "New York",
      "skills": ["Python", "Flask"],
      "link": "https://example.com/job/2"
    }
  ]
}
```

##### For Location Intent

```json
{
  "jobs": [
    {
      "title": "Python Developer",
      "company": "Tech Co.",
      "date": "2025-01-25",
      "location": "New York",
      "skills": ["Python", "Flask"],
      "link": "https://example.com/job/1"
    }
  ]
}
```

##### For Skills Intent

```json
{
  "jobs": [
    {
      "title": "Software Developer",
      "company": "Dev Corp",
      "date": "2025-01-15",
      "location": "San Francisco",
      "skills": ["JavaScript", "React"],
      "link": "https://example.com/job/3"
    }
  ]
}
```

##### For Unrecognized Intents

```json
{
  "response": "Sorry, I could not understand your query."
}
```

## Functions and Description

### `preprocess_input(text)`
- **Description**: Preprocesses the input text by converting it to lowercase, removing non-alphabetic characters, and filtering out stopwords using NLTK.
- **Parameters**: `text` (string) - User's input text.
- **Returns**: Preprocessed text (string).

### `scrape_infopark_jobs()`
- **Description**: Scrapes job listings from the Infopark website.
- **Returns**: A list of job objects containing the title, company, date, and link.

### `train_intent_classifier()`
- **Description**: Trains a classifier to recognize user intents (e.g., job search, location, skills) based on predefined patterns.
- **Returns**: A tuple containing the vectorizer and classifier objects.

### `extract_entities(text)`
- **Description**: Uses SpaCy's Named Entity Recognition (NER) to extract entities (e.g., location, skills) from the user's input.
- **Parameters**: `text` (string) - User's input text.
- **Returns**: A dictionary with the extracted location and skills entities.

### `get_job_response()`
- **Description**: This is the main API endpoint function that processes the user's input, classifies the intent, scrapes job listings, and returns a response.
- **Parameters**: `user_input` (string) - The user's query received in the POST request body.
- **Returns**: A JSON response containing job listings or a message based on the intent.

## Libraries and Tools Used

### Flask
- **Description**: A micro web framework used to create the API.
- **Usage**: Used to define routes, handle incoming requests, and return responses.

### NLTK (Natural Language Toolkit)
- **Description**: A library for text processing and natural language processing tasks.
- **Usage**: Used for tokenizing the text and removing stopwords.

### SpaCy
- **Description**: A powerful NLP library for Named Entity Recognition (NER) and other NLP tasks.
- **Usage**: Used to extract entities such as location and skills from user input.

### Scikit-learn
- **Description**: A machine learning library used for building and training the intent classification model.
- **Usage**: Used for vectorizing the text input with `TfidfVectorizer` and classifying the intent using `MultinomialNB`.

### BeautifulSoup and Requests
- **Description**: Libraries used for web scraping.
- **Usage**: Used to scrape job listings from the Infopark website.

### Flask-CORS
- **Description**: A library to enable Cross-Origin Resource Sharing (CORS) for Flask apps.
- **Usage**: Used to allow the front-end to make requests to this back-end API hosted on different origins.

## Deployment and Running the Application

### Environment Setup
Make sure the following dependencies are installed:

```bash
pip install Flask Flask-CORS nltk spacy scikit-learn beautifulsoup4 requests
```

### Running the App
Run the app using the following command:

```bash
python aichatbot.py
```

The app will start a local server by default at `http://127.0.0.1:5000/`.

### Loading SpaCy Model
Make sure to download the SpaCy model before running the application:

```bash
python -m spacy download en_core_web_sm
```

---

This documentation provides a complete guide on how to set up, use, and deploy the Job Search Chatbot API. 🚀

