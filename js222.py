from flask import Flask, request, jsonify
from pdfminer.high_level import extract_text
import json
import pyap
import re
from dateutil import parser
import nltk
import pdfplumber
import spacy
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import OrderedDict

app = Flask(__name__)
nltk.download('punkt')
nltk.download('stopwords')
nlp = spacy.load('en_core_web_sm')
@app.route("/")
def home():
    return render_template("che.html")
@app.route("/pre", methods=["POST"])
def text_from_pdf():
    if request.method == 'POST':
        file = request.files["files"]
        selected_options = request.form["extractOptions"]
        file_path = "temp.pdf"
        file.save(file_path)
        with open(file_path, 'rb') as f:
            text = extract_text(f)
        data = {}
        if "addresses" in selected_options:
            addresse1 = pyap.parse(text, country="US")
            addresse2 = pyap.parse(text, country="GB")  # UK
            addresse3 = pyap.parse(text, country="CA")  # Canada
            addresses = addresse1
            if addresses:
                unique_addresses = list(set(address.full_address for address in addresses))
                data['address_count'] = len(unique_addresses)
                data['addresses'] = [{"value": address} for address in unique_addresses]
            else:
                data['address_count'] = 0
                data['addresses'] = []

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
            data['date_count'] = len(unique_dates)
            data['dates'] = [{"value": date} for date in unique_dates]

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
            data['name_count'] = len(filtered_names)
            data['names'] = [{"value": name} for name in filtered_names]

        if "full_text" in selected_options:
            data['full_text'] = text
        os.remove(file_path)
        # Convert data to JSON and return
        return jsonify(data)
    return render_template("che.html", **locals())

if __name__ == "__main__":
    app.run()
