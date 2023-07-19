from flask import Flask,request,render_template
import json
import pyap
import PyPDF2
from pdfminer.high_level import extract_text,extract_pages,extract_text_to_fp
from dateutil import parser
import datefinder
import dateparser
import joblib
import nltk
import tika
nltk.download('punkt')
from dateparser.search import search_dates
from nameparser import HumanName
from nltk.corpus import wordnet
app=Flask(__name__,template_folder="template")
@app.route("/")
def home():
    return render_template("pdf_to_text.html")
@app.route("/pre" ,methods=["POST","GET"])
def text_from_pdf():
    if request.method == 'POST':
        file = request.files['pdf_file']
        text = extract_text(file)
        #print(text)
        dates = list(datefinder.find_dates(text))
        if len(dates) > 0:
            print("Dates found:")
            for date in dates:
                print(date)
        addresses = pyap.parse(text, country='US')
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
            print("No names found.")

    return render_template("pdf_to_text.html",**locals())
if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)

