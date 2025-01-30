from flask import Flask, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import spacy
import re
import requests
from bs4 import BeautifulSoup
import urllib3
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Disable SSL certificate verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Ensure required NLTK resources are available
nltk.data.path.append('C:/USER/AppData/Roaming/nltk_data')
nltk.download('punkt')
nltk.download('stopwords')

# Initialize SpaCy for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

# Sample job-related intents
intents = [
    {"intent": "job_search", "patterns": ["I am looking for a job", "Find me a job", "Help me find work"]},
    {"intent": "location", "patterns": ["Where is the job", "In which location", "Location of the job"]},
    {"intent": "skills", "patterns": ["What skills are needed", "What skills for this job", "Skills required for the job"]},
]

# Preprocessing function
def preprocess_input(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = word_tokenize(text)
    stop_words = set(nltk.corpus.stopwords.words("english"))
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

# Scrape job listings with links
def scrape_infopark_jobs():
    url = "https://infopark.in/companies/job-search"
    response = requests.get(url, verify=False)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = []

        for job_card in soup.find_all('div', class_='row company-list joblist'):
            title_tag = job_card.find('a')
            title = title_tag.text.strip() if title_tag else "No title"
            link = title_tag['href'] if title_tag and 'href' in title_tag.attrs else "No link"
            company_tag = job_card.find('div', class_='col-xs-6 col-md-4 mt5 jobs-comp-name text-center')
            company = company_tag.find('a').text.strip() if company_tag and company_tag.find('a') else "No company"
            date_tag = job_card.find('div', class_='col-xs-12 col-md-4 text-right job-date')
            date = date_tag.text.strip() if date_tag else "No date"

            jobs.append({
                "title": title,
                "company": company,
                "date": date,
                "link": link
            })
        
        return jobs
    else:
        return []

# Train intent classifier
def train_intent_classifier():
    training_sentences = []
    labels = []
    for intent in intents:
        for pattern in intent['patterns']:
            training_sentences.append(preprocess_input(pattern))
            labels.append(intent['intent'])
    
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(training_sentences)
    y = labels
    
    classifier = MultinomialNB()
    classifier.fit(X, y)
    
    return vectorizer, classifier

# Extract entities (location & skills)
def extract_entities(text):
    doc = nlp(text)
    entities = {"skills": [], "location": []}
    
    for ent in doc.ents:
        if ent.label_ == "GPE":
            entities["location"].append(ent.text)
        elif ent.label_ in ["ORG", "PRODUCT"]:
            entities["skills"].append(ent.text)
    
    return entities

# API endpoint for job search
@app.route('/get_job_response', methods=['POST'])
def get_job_response():
    data = request.json
    user_input = data.get("user_input", "")
    preprocessed_input = preprocess_input(user_input)
    vectorized_input = vectorizer.transform([preprocessed_input])
    
    intent = classifier.predict(vectorized_input)[0]
    jobs = scrape_infopark_jobs()
    
    if intent == "job_search":
        if not jobs:
            return jsonify({"response": "Sorry, I couldn't find any job listings right now."})
        
        keyword = user_input.lower()
        filtered_jobs = [job for job in jobs if keyword in job["title"].lower()]
        
        if filtered_jobs:
            return jsonify({"jobs": filtered_jobs})
        else:
            return jsonify({"response": f"Sorry, no jobs found matching '{keyword}'."})

    if intent == "location":
        location = extract_entities(user_input)["location"]
        if location:
            jobs_in_location = [job for job in jobs if location[0].lower() in job["title"].lower()]
            return jsonify({"jobs": jobs_in_location})
        else:
            return jsonify({"response": "Which location are you interested in?"})

    if intent == "skills":
        skills = extract_entities(user_input)["skills"]
        if skills:
            jobs_with_skills = [job for job in jobs if any(skill.lower() in job["title"].lower() for skill in skills)]
            return jsonify({"jobs": jobs_with_skills})
        else:
            return jsonify({"response": "What skills do you have? Please specify."})
    
    return jsonify({"response": "Sorry, I could not understand your query."})

# Train the model
vectorizer, classifier = train_intent_classifier()

if __name__ == "__main__":
    app.run(debug=True)
