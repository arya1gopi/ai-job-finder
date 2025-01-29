# Job Search Chatbot

## Overview
This is a Python-based chatbot that helps users find job listings from Infopark's job search page. It processes user input using Natural Language Processing (NLP) techniques and retrieves relevant job listings based on specified filters such as job title, skills, or location.

## Features
- **Job Search**: Scrapes job listings from Infopark's job portal.
- **Intent Recognition**: Uses a Naive Bayes classifier to determine user intent.
- **Entity Recognition**: Uses SpaCy for Named Entity Recognition (NER) to extract skills and locations from user input.
- **Keyword Filtering**: Allows users to filter job listings based on keywords.
- **Structured Output**: Displays job details in a formatted manner.

## Requirements
Ensure you have the following installed:
- Python 3.x
- Required Python libraries:
  ```sh
  pip install nltk scikit-learn spacy beautifulsoup4 requests urllib3
  ```
- Download the necessary NLP models:
  ```sh
  python -m spacy download en_core_web_sm
  ```

## Installation
1. Clone this repository or copy the script.
2. Install the required dependencies using the command above.
3. Run the script using:
   ```sh
   python chatbot.py
   ```

## Usage
1. Start the chatbot and enter your job search query (e.g., "Find me a Java job").
2. The bot will classify your intent and fetch relevant job listings.
3. You can filter jobs based on title, skills, or location.
4. Type `exit` to quit the chatbot.

## Example Interaction
```
You: Find me a Python Developer job
Bot: Here are some job listings:

🔹 **Title:** Python Developer
🏢 **Company:** ABC Corp
📅 **Date:** 30 Jan 2025
----------------------
...
```

## Future Enhancements
- Improve intent classification with a larger dataset.
- Add support for more job portals.
- Enhance filtering options with more parameters like experience level and salary range.

## License
This project is open-source and available for modification and distribution.

## Author
Arya Gopi
