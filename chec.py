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
        with open(file_path,'rb') as f:
            text = extract_text(f)
        if "full_text" in selected_options:
            text_con = text
        if "dates" in selected_options:
            dates = list(datefinder.find_dates(text))
            if len(dates) > 0:
                print("Dates found:")
                for date in dates:
                    print(date)
        if "addresses" in selected_options:
            addresses = pyap.parse(text, country='US')
            if addresses:
                print("Addresses found:")
                for address in addresses:
                    print(address.full_address)
            else:
                print("No addresses found.")
        if "names" in selected_options:
            def extract_names_from_pdf(file_path):
                names = []
                stop_words = set(stopwords.words('english'))
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        tokens = word_tokenize(page_text)
                        filtered_tokens = [token for token in tokens if token.isalpha() and token.lower() not in stop_words]
                        text = ' '.join(filtered_tokens)
                        doc = nlp(text)
                        for ent in doc.ents:
                            if ent.label_ == 'PERSON':
                                names.append(ent.text)
                return names
            extracted_names = extract_names_from_pdf(file_path)
            print("Extracted names:")
            for name in extracted_names:
                pass
                #print(name)
            human_names = []
            for name in extracted_names:
                if re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+$', name):
                    human_names.append(name)
                elif re.match(r"\b[A-Z][a-zA-Z]+\b",name):
                    human_names.append(name)
            print("Extracted human names:")
            for name in human_names:
                print(name)
        os.remove(file_path)

    return render_template("che.html", **locals())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
