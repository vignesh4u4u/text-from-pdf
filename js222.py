import re
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
nltk.download('maxent_ne_chunker')
nltk.download('words')
nlp = spacy.load('en_core_web_sm')
def find_human_names(text):
    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    named_entities = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    person_names = []
    for tree in named_entities:
        for subtree in tree:
            if isinstance(subtree, nltk.Tree) and subtree.label() == 'PERSON':
                person_name = ' '.join([token for token, pos in subtree.leaves()])
                # Use HumanName to check if the name has titles or suffixes
                name_obj = HumanName(person_name)
                if name_obj.title or name_obj.suffix:
                    person_names.append(person_name)

    return person_names

# Rest of the code remains the same...
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
            extracted_names = find_human_names(text)
            name_length_threshold = 25
            filtered_names = [name for name in extracted_names if len(name) <= name_length_threshold]
            formatted_names = {f"Name_{idx}": name for idx, name in enumerate(filtered_names, start=1)}
            data['extracted_names'] = formatted_names

        os.remove(file_path)
        return jsonify(data)

    return render_template("che.html", **locals())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
