import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import spacy
import re
import requests
from bs4 import BeautifulSoup
import urllib3

# Disable SSL certificate verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Download NLTK resources
nltk.data.path.append('C:/USER/AppData/Roaming/nltk_data')
nltk.download('punkt_tab')  # Correct tokenizer resource
nltk.download('stopwords')  # If you want to use stopwords

# Initialize SpaCy for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

# Sample job-related intents (to be expanded)
intents = [
    {"intent": "job_search", "patterns": ["I am looking for a job", "Find me a job", "Help me find work"]},
    {"intent": "location", "patterns": ["Where is the job", "In which location", "Location of the job"]},
    {"intent": "skills", "patterns": ["What skills are needed", "What skills for this job", "Skills required for the job"]},
]

# Preprocessing function to clean and tokenize input
def preprocess_input(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = word_tokenize(text)
    stop_words = set(nltk.corpus.stopwords.words("english"))
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

def scrape_infopark_jobs():
    url = "https://infopark.in/companies/job-search"  # Updated URL for job listings
    response = requests.get(url,verify=False)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
       
        jobs = []
         # Loop through each job listing container
        for job_card in soup.find_all('div', class_='row company-list joblist'):  # Adjusted the class based on the provided HTML
            title = job_card.find('a').text.strip() if job_card.find('a') else "No title"
            company = job_card.find('div', class_='col-xs-6 col-md-4 mt5 jobs-comp-name text-center').find('a').text.strip() if job_card.find('div', class_='col-xs-6 col-md-4 mt5 jobs-comp-name text-center') else "No company"
            date = job_card.find('div', class_='col-xs-12 col-md-4 text-right job-date').text.strip() if job_card.find('div', class_='col-xs-12 col-md-4 text-right job-date') else "No date"

            jobs.append({
                "title": title,
                "company": company,
                "date": date
            })

        return jobs
    else:
        print(f"Failed to retrieve jobs. Status code: {response.status_code}")
        return []

# Intent classification using Naive Bayes
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

# Entity Recognition using SpaCy
def extract_entities(text):
    doc = nlp(text)
    entities = {"skills": [], "location": []}
    
    for ent in doc.ents:
        if ent.label_ == "GPE":
            entities["location"].append(ent.text)
        elif ent.label_ == "ORG":
            entities["skills"].append(ent.text)
    
    return entities

# Match the intent and respond with job data
def get_job_response(user_input):
    preprocessed_input = preprocess_input(user_input)
    vectorized_input = vectorizer.transform([preprocessed_input])
    
    intent = classifier.predict(vectorized_input)[0]
    
    if intent == "job_search":
        jobs = scrape_infopark_jobs()  # Fetch job listings
        
        if not jobs:
            return "Sorry, I couldn't find any job listings right now."
        
        keyword = user_input.lower() if user_input else "" # Get the filter keyword from user input
        
        if keyword:
            jobs = [job for job in jobs if keyword in job["title"].lower()]  # Filter jobs by keyword
        
        if jobs:
            response = "Here are some job listings:\n\n"
            for job in jobs:
                response += f"🔹 **Title:** {job['title']}\n"
                response += f"🏢 **Company:** {job['company']}\n"
                response += f"📅 **Date:** {job['date']}\n"
                response += "----------------------\n"
            return response
        else:
            return f"Sorry, I couldn't find any job listings matching '{keyword}'."

    if intent == "location":
        location = extract_entities(user_input)["location"]
        if location:
            jobs = scrape_infopark_jobs()
            jobs_in_location = [job for job in jobs if location[0].lower() in job["location"].lower()]
            return f"Here are jobs in {location[0]}: " + "\n".join([f"{job['title']}" for job in jobs_in_location])
        else:
            return "Which location are you interested in?"

    if intent == "skills":
        skills = extract_entities(user_input)["skills"]
        if skills:
            jobs = scrape_infopark_jobs()
            jobs_with_skills = [job for job in jobs if any(skill.lower() in job["title"].lower() for skill in skills)]
            return f"Jobs requiring {', '.join(skills)}: " + "\n".join([f"{job['title']} in {job['location']}" for job in jobs_with_skills])
        else:
            return "What skills do you have? Please specify."
    
    return "Sorry, I could not understand your query."

# Train the model
vectorizer, classifier = train_intent_classifier()

# Example interaction
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    response = get_job_response(user_input)
    print(f"Bot: {response}")
