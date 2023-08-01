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
            filtered_addresses = [address.full_address for address in addresses if
                                  "1 RESIDENT IS RESPONSIBLE FOR CHAR" not in address.full_address
                                  and "invitees.11. THERE IS NO WARRANTY OF A SMOK" not in address.full_address]
            if filtered_addresses:
                unique_addresses = list(set(filtered_addresses))
                formatted_addresses = [{"value": address} for address in unique_addresses]
                data['addresses'] = formatted_addresses
                data['address_count'] = len(formatted_addresses)
            else:
                data["address_response"] = "No addresses found"

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

        if "monetary_amounts" in selected_options:
            doc = nlp(text)
            us_amounts = [ent.text for ent in doc.ents if ent.label_ == "MONEY"]
            formatted_amounts = [{"value": amount} for amount in us_amounts]
            data['monetary_amounts'] = formatted_amounts
            data['monetary_amount_count'] = len(formatted_amounts)

        """if "emails" in selected_options:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            formatted_emails = [{"value": email} for email in emails]
            data['emails'] = formatted_emails
            data['email_count'] = len(formatted_emails)"""

        os.remove(file_path)
        return jsonify(data)
    #return render_template("che.html", **locals())
    #host="10.244.0.7",port=8080
    #http://localhost:8080/ml-service/text-extraction
    #https://india.yoroflow.com/ml-service/text-extraction
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)