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
import joblib
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
app = Flask(__name__, template_folder="template")
nltk.download('punkt')
nltk.download('stopwords')
nlp = spacy.load('en_core_web_sm')

def extract_address_custom(text):
    address_line_pattern = r"\d+ [\w\s.,]+"
    suite_pattern = r"Suite [\w\d]+"
    city_state_zip_pattern = r"[A-Z][A-Za-z\s]+, [A-Z]{2} \d{5}"
    address_line_match = re.search(address_line_pattern, text)
    suite_match = re.search(suite_pattern, text)
    city_state_zip_match = re.search(city_state_zip_pattern, text)

    if address_line_match and city_state_zip_match:
        address_line = address_line_match.group()
        suite = suite_match.group().replace("Suite ", "") if suite_match else None
        city_state_zip = city_state_zip_match.group()

        address = f"{address_line}{', ' + suite if suite else ''} • {city_state_zip}"
        return address
    else:
        return None
def format_addresses(addresses):
    formatted_addresses = {}
    for key, address in addresses.items():
        formatted_address = address.replace('\u2022', '').strip()
        formatted_addresses[key] = formatted_address
    return formatted_addresses

@app.route("/ml-service/text-extraction", methods=["POST"])
def text_from_pdf():
    if request.method == 'POST':
        file = request.files['files']
        selected_options = request.form["extractOptions"]
        file_path = "temp.pdf"
        file.save(file_path)
        with open(file_path, 'rb') as f:
            text = extract_text(f)

        data = {}

        if "full_text" in selected_options:
            data['full_text'] = text

        if "addresses" in selected_options:
            addresse1 = pyap.parse(text, country="US")
            addresse2 = pyap.parse(text, country="GB")  # UK
            addresse3 = pyap.parse(text, country="CA")  # Canada
            addresses = addresse1
            address = extract_address_custom(text)
            all_addresses = {}
            if address:
                all_addresses['Custom Address'] = address
            if addresses:
                unique_addresses = list(set(address.full_address for address in addresses))
                unique_addresses.sort()  # Sort the addresses for consistency
                all_addresses.update({f"Address_{idx}": address for idx, address in enumerate(unique_addresses, start=1)})
            data['addresses'] = {
                "address_count": len(all_addresses),
                "addresses": [{"value": address} for address in all_addresses.values()]
            }

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
            unique_dates.sort()  # Sort the dates for consistency
            ordered_dates_list = [{"value": date} for date in unique_dates]
            data['dates'] = {
                "date_count": len(ordered_dates_list),
                "dates": ordered_dates_list
            }

        if "names" in selected_options:
            def extract_names_from_pdf(file_path):
                names = set()  # Use a set to store names and remove duplicates
                stop_words = set(stopwords.words('english'))
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        tokens = word_tokenize(page_text)
                        filtered_tokens = [token for token in tokens if
                                           token.isalpha() and token.lower() not in stop_words]
                        text = ' '.join(filtered_tokens)
                        doc = nlp(text)
                        unique_names = set(ent.text for ent in doc.ents if ent.label_ == 'PERSON')
                        names.update(unique_names)
                return names

            extracted_names = extract_names_from_pdf(file_path)
            name_length_threshold = 25
            filtered_names = [name for name in extracted_names if len(name) <= name_length_threshold]
            formatted_names = [{"value": name} for name in filtered_names]
            formatted_names.sort(key=lambda x: x["value"])  # Sort the names for consistency
            data['names'] = {
                "name_count": len(filtered_names),
                "names": formatted_names
            }

        return jsonify(data)

    #return render_template("che.html", **locals())
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)