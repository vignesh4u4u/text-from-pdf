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
text = extract_text('Lease10.pdf')
#print(text)
# Find dates within the extracted text
dates = list(datefinder.find_dates(text))
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
import nltk
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
    print(name)

