"""from flask import Flask, request, render_template, json, jsonify
from pdfminer.high_level import extract_text
from nameparser import HumanName
import datefinder
import pyap
text = extract_text('Lease10.pdf')
print(text)
from pdfminer.high_level import extract_text
import datefinder
import pyap
# Extract text from the PDF
text = extract_text('Lease10.pdf')"""
#print(text)
# Find dates within the extracted text
"""dates = list(datefinder.find_dates(text))
# Check if dates are present
if len(dates) > 0:
    print("Dates found:")
    for date in dates:
        print(date)
else:
    print("No dates found.")
# Find addresses within the extracted text
addresses = pyap.parse(text, country='US')  # Adjust the country code based on your requirements

# Check if addresses are present
if addresses:
    print("Addresses found:")
    for address in addresses:
        print(address.full_address)
else:
    print("No addresses found.")
names = []
for line in text.split('\n'):
    name = HumanName(line)
    if name.first or name.last:
        names.append(name)
if names:
    print("Names found:")
    for name in names:
        print(name)
else:
    print("No names found.")"""

print("--------------------name detect--------------")

"""import nltk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pdfplumber

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')

def extract_names_from_pdf(file_path):
    names = []
    stop_words = set(stopwords.words('english'))

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            tokens = word_tokenize(text)
            filtered_tokens = [token for token in tokens if token.isalpha() and token.lower() not in stop_words]
            tagged_tokens = pos_tag(filtered_tokens)

            current_name = ""
            for word, pos in tagged_tokens:
                if pos == 'NNP':  # Proper noun tags in NLTK
                    if current_name:
                        current_name += " "
                    current_name += word
                else:
                    if current_name:
                        names.append(current_name)
                        current_name = ""
            if current_name:
                names.append(current_name)

    return names
file_path = "Lease10.pdf"
extracted_names = extract_names_from_pdf(file_path)
print("Extracted names:")
for name in extracted_names:
    print(name)"""

print("--------------------only human name-----------")
"""import nltk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pdfplumber
import spacy
import re
from collections import OrderedDict
nltk.download('punkt')
nltk.download('stopwords')

# Load the pre-trained spaCy model for English
nlp = spacy.load('en_core_web_sm')
def extract_names_from_pdf(file_path):
    names = []
    stop_words = set(stopwords.words('english'))

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            tokens = word_tokenize(text)
            filtered_tokens = [token for token in tokens if token.isalpha() and token.lower() not in stop_words]

            # Join the tokens into a single string
            text = ' '.join(filtered_tokens)

            # Apply named entity recognition using spaCy
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ == 'PERSON':
                    names.append(ent.text)
    return names
file_path = "Lease10.pdf"
extracted_names = extract_names_from_pdf(file_path)
print("Extracted names:")
for name in extracted_names:
    pass
    #print(name)


human_names = []
for name in extracted_names:
    if re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+$', name):
        human_names.append(name)
print("Extracted human names:")
for name in human_names:
    print(name)"""

"""print("------------------spacy-----------")
import spacy

# Load the pre-trained English model
nlp = spacy.load('en_core_web_sm')

# Text to be analyzed
#text = "John Smith and Sarah Johnson went to the park."

# Process the text with the NER model
doc = nlp(text)

# Extract person names
person_names = []
for ent in doc.ents:
    if ent.label_ == 'PERSON':
        person_names.append(ent.text)

# Display the predicted names
for name in person_names:
    print(name)"""
print("-----------------date------------------")
"""import PyPDF2
import dateparser
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfFileReader(f)
        num_pages = pdf_reader.numPages
        text = ""
        for page_number in range(num_pages):
            page = pdf_reader.getPage(page_number)
            text += page.extract_text()
    return text
def extract_dates_from_text(text):
    extracted_dates = dateparser.search.search_dates(text)
    dates = [date for date, _ in extracted_dates]
    return dates
file_path = 'Lease6.pdf'
text = extract_text_from_pdf(file_path)
dates = extract_dates_from_text(text)

for date in dates:
    print(date)"""
print("_________________________________________________________")
"""import nltk

# Download the NER trained model (Note: This is a large download)
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Function to find human names using NER
def find_human_names(text):
    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    named_entities = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    person_names = []
    for tree in named_entities:
        for subtree in tree:
            if isinstance(subtree, nltk.Tree) and subtree.label() == 'NE':
                person_name = ' '.join([token for token, pos in subtree.leaves()])
                person_names.append(person_name)

    return person_names

# Example text
text = "John Smith is a software engineer at XYZ Corp. Jane Doe works in the marketing department."

# Find human names
names = find_human_names(text)
print(names)"""

from flask import Flask, request, render_template, jsonify
from pdfminer.high_level import extract_text, extract_pages, extract_text_to_fp
import json
import pyap
import PyPDF2
import pandas as pd
import numpy as np
from dateutil import parser
import datefinder
import dateparser
import nltk
import tika
import re
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pdfplumber
import spacy
from dateparser.search import search_dates
from nameparser import HumanName
import os
import addressparser
from collections import OrderedDict
app = Flask(__name__)
nltk.download('punkt')
nltk.download('stopwords')
nlp = spacy.load('en_core_web_sm')
@app.route("/ml-service/health/v1/ping",methods=["GET"])
def home():
    if request.method == 'GET':
        return "pong"
@app.route("/ml-service/text-extraction", methods=["POST"])
def text_from_pdf():
    if request.method == 'POST':
        #print(request.files)
        file = request.files["files"]
        selected_options = request.form["extractOptions"]
        file_path = "temp.pdf"
        file.save(file_path)
        with open(file_path, 'rb') as f:
            text = extract_text(f)
        data = {}
        if "addresses" in selected_options:
            addresse1 = pyap.parse(text, country="US")
            addresse2 = pyap.parse(text, country="GB")  # uk
            addresse3 = pyap.parse(text, country="CA")  # canada
            addresses = addresse1
            if addresses:
                unique_addresses = list(set(address.full_address for address in addresses))
                formatted_addresses = [{"value": address} for address in unique_addresses]
                data['addresses'] = formatted_addresses
                data['address_count'] = len(formatted_addresses)
            else:
                data["address_response"]="No addresses found"

        if "dates" in selected_options:
            date_pattern = r'(?i)\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|' \
                           r'\d{1,2}(?:st|nd|rd|th)? \w+ \d{2,4}|' \
                           r'\d{1,2} \w+ \d{2,4}|' \
                           r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{2,4}|' \
                           r'(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?) \d{1,2}, \d{4}|' \
                           r'[a-zA-Z]{3} \d{1,2}, \d{4}|' \
                           r'[a-zA-Z]{3} \d{1,2},\d{4})\b'

            matches = re.findall(date_pattern, text, flags=re.IGNORECASE)
            dates = [parser.parse(match, fuzzy=True) for match in matches]
            unique_dates = list(set(date.strftime("%Y-%m-%d") for date in dates))
            # Filter out dates with starting year "0"
            valid_dates = [date for date in unique_dates if not date.startswith("0")]
            formatted_dates = [{"value": date} for date in valid_dates]
            data['dates'] = formatted_dates
            data['date_count'] = len(formatted_dates)

        if "names" in selected_options:
            def extract_names_from_pdf(file_path):
                names = set()
                stop_words = set(stopwords.words('english'))
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        tokens = word_tokenize(page_text)
                        filtered_tokens = [token for token in tokens if token.isalpha() and token.lower() not in stop_words]
                        text = ' '.join(filtered_tokens)
                        doc = nlp(text)
                        unique_names = set(ent.text for ent in doc.ents if ent.label_ == 'PERSON')
                        names.update(unique_names)
                return names
            extracted_names = extract_names_from_pdf(file_path)
            name_length_threshold = 25
            filtered_names = [name for name in extracted_names if (len(name) <= name_length_threshold and len(name) > 2)]
            formatted_names = [{"value": name} for name in filtered_names]
            data['names'] = formatted_names
            data['name_count'] = len(formatted_names)

        if "full_text" in selected_options:
            data['full_text'] = text

        os.remove(file_path)
        return jsonify(data)
    #return render_template("che.html", **locals())
    #host="10.244.0.7",port=8080
    #http://localhost:8080/ml-service/text-extraction
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)





