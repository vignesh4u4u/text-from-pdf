from flask import Flask, request, render_template, jsonify
import json
import pyap
import PyPDF2
from pdfminer.high_level import extract_text, extract_pages, extract_text_to_fp
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
from nltk.corpus import wordnet
import os
from collections import OrderedDict

app = Flask(__name__, template_folder="template")
nltk.download('punkt')
nltk.download('stopwords')
nlp = spacy.load('en_core_web_sm')

@app.route("/")
def home():
    return render_template("che.html")

@app.route("/pre", methods=["POST", "GET"])
def text_from_pdf():
    if request.method == 'POST':
        file = request.files['pdf_file']
        selected_options = request.form.getlist('myselect')
        file_path = "temp.pdf"
        file.save(file_path)
        with open(file_path, 'rb') as f:
            text = extract_text(f)
        data = {}  # Dictionary to store the extracted data

        if "addresses" in selected_options:
            addresses = pyap.parse(text, country='US')
            if addresses:
                unique_addresses = list(set(address.full_address for address in addresses))
                data['addresses'] = {f"address_{idx}": address for idx, address in enumerate(unique_addresses, start=1)}
                data['address_count'] = len(unique_addresses)
            else:
                data['addresses'] = "No addresses found."

        if "full_text" in selected_options:
            data['full_text'] = text

        if "dates" in selected_options:
            date_pattern = r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|' \
                           r'\d{1,2}(?:st|nd|rd|th)? \w+ \d{2,4}|' \
                           r'\d{1,2} \w+ \d{2,4}|' \
                           r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{2,4}|' \
                           r'(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?) \d{1,2}, \d{4})\b'

            matches = re.findall(date_pattern, text, flags=re.IGNORECASE)
            dates = [parser.parse(match, fuzzy=True) for match in matches if not match.startswith(('0', '00'))]

            if dates:
                ordered_dates_dict = OrderedDict()
                for idx, date in enumerate(dates, start=1):
                    formatted_date = date.strftime("%Y-%m-%d")
                    ordered_dates_dict[f"date_{idx}"] = formatted_date
                data['dates'] = ordered_dates_dict
                data['date_count'] = len(ordered_dates_dict)
                adjusted_dates_dict = {f"date_{i}": ordered_dates_dict[key] for i, key in
                                       enumerate(ordered_dates_dict, start=1)}
                data['dates'] = adjusted_dates_dict

        if "names" in selected_options:
            def extract_names_from_pdf(file_path):
                names = []
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
                        names.extend(unique_names)
                return names

            extracted_names = extract_names_from_pdf(file_path)
            formatted_names = {f"Name_{idx}": name for idx, name in enumerate(extracted_names, start=1)}
            ordered_names = dict(sorted(formatted_names.items()))
            data['extracted_names'] = ordered_names
            data['name_count'] = len(extracted_names)

        os.remove(file_path)

        return jsonify(data)

    return render_template("che.html", **locals())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
