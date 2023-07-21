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
        data = {}
        if "addresses" in selected_options:
            addresses = pyap.parse(text, country='US') # us
            if addresses:
                unique_addresses = list(set(address.full_address for address in addresses))
                data['addresses'] = {f"address_{idx}": address for idx, address in enumerate(unique_addresses, start=1)}
                data['address_count'] = len(unique_addresses)
            else:
                data['addresses'] = "No addresses found."
            addresses_in = pyap.parse(text, country='IN')# india
            if addresses_in:
                unique_addresses_in = list(set(address.full_address for address in addresses_in))
                data['addresses_in'] = {f"address_{idx}": address for idx, address in enumerate(unique_addresses_in, start=1)}
                data['address_count_in'] = len(unique_addresses_in)
            else:
                data['addresses_in'] = "No addresses found for India."
            addresses_uk = pyap.parse(text, country='GB') # uk
            if addresses_uk:
                unique_addresses_in = list(set(address.full_address for address in addresses_uk))
                data['addresses_in'] = {f"address_{idx}": address for idx, address in enumerate(unique_addresses_in, start=1)}
                data['address_count_in'] = len(unique_addresses_in)
            else:
                data['addresses_in'] = "No addresses found for India."
            addresses_ca = pyap.parse(text, country='CA') #canada
            if addresses_ca:
                unique_addresses_in = list(set(address.full_address for address in addresses_ca))
                data['addresses_in'] = {f"address_{idx}": address for idx, address in enumerate(unique_addresses_in, start=1)}
                data['address_count_in'] = len(unique_addresses_in)
            else:
                data['addresses_in'] = "No addresses found for India."
            addresses_au = pyap.parse(text, country='AU')#Australia
            if addresses_au:
                unique_addresses_in = list(set(address.full_address for address in addresses_au))
                data['addresses_in'] = {f"address_{idx}": address for idx, address in enumerate(unique_addresses_in, start=1)}
                data['address_count_in'] = len(unique_addresses_in)
            else:
                data['addresses_in'] = "No addresses found for Australia."
            addresses_ge = pyap.parse(text, country='DE')  # germany
            if addresses_ge:
                unique_addresses_in = list(set(address.full_address for address in addresses_ge))
                data['addresses_in'] = {f"address_{idx}": address for idx, address in
                                        enumerate(unique_addresses_in, start=1)}
                data['address_count_in'] = len(unique_addresses_in)
            else:
                data['addresses_in'] = "No addresses found for germany."
            addresses_ch = pyap.parse(text, country='CN')  #china
            if addresses_ch:
                unique_addresses_in = list(set(address.full_address for address in addresses_ch))
                data['addresses_in'] = {f"address_{idx}": address for idx, address in
                                        enumerate(unique_addresses_in, start=1)}
                data['address_count_in'] = len(unique_addresses_in)
            else:
                data['addresses_in'] = "No addresses found for chaina."
            addresses_fr = pyap.parse(text, country='FR')
            if addresses_fr:
                unique_addresses_in = list(set(address.full_address for address in addresses_fr))
                data['addresses_in'] = {f"address_{idx}": address for idx, address in
                                        enumerate(unique_addresses_in, start=1)}
                data['address_count_in'] = len(unique_addresses_in)
            else:
                data['addresses_in'] = "No addresses found for france."

        if "full_text" in selected_options:
            data['full_text'] = text

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
            ordered_dates_dict = OrderedDict()
            for idx, date in enumerate(unique_dates, start=1):
                ordered_dates_dict[f"date_{idx}"] = date
            data['dates'] = ordered_dates_dict
            data['date_count'] = len(ordered_dates_dict)

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
            formatted_names = {f"Name_{idx}": name for idx, name in enumerate(filtered_names, start=1)}
            data['extracted_names'] = {
                'name_count': len(filtered_names),
                'names': formatted_names}
        os.remove(file_path)
        return jsonify(data)
    return render_template("che.html", **locals())
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
