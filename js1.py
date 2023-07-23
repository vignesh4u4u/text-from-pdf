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
from names_dataset import NameDataset
text=extract_text("Lease6.pdf")
nd=NameDataset()
a1=nd.get_top_names(country_alpha2='AE')
a2=nd.get_top_names(country_alpha2="AF")
a3=nd.get_top_names(country_alpha2="AL")
a4=nd.get_top_names(country_alpha2="AO")
a5=nd.get_top_names(country_alpha2="AR")
a6=nd.get_top_names(country_alpha2="AT")
a7=nd.get_top_names(country_alpha2="BD")
a8=nd.get_top_names(country_alpha2="BE")
a9=nd.get_top_names(country_alpha2="BF")
a10=nd.get_top_names(country_alpha2="BG")
A=(a1["AE"]["M"]+a1["AE"]["F"])+(a2["AF"]["M"]+a2["AF"]["F"])+(a3["AL"]["M"]+a3["AL"]["F"])+(a4["AO"]["M"]+a4["AO"]["F"])+(a5["AR"]["M"]+a5["AR"]["F"])+\
  (a6["AT"]["M"]+a6["AT"]["F"])+(a7["BD"]["M"]+a7["BD"]["F"])+(a8["BE"]["M"]+a8["BE"]["F"])+(a9["BF"]["M"]+a9["BF"]["F"])+(a10["BG"]["M"]+a10["BG"]["F"])

b1=nd.get_top_names(country_alpha2="BH")
b2=nd.get_top_names(country_alpha2="BI")
b3=nd.get_top_names(country_alpha2="BN")
b4=nd.get_top_names(country_alpha2="BO")
b5=nd.get_top_names(country_alpha2="BW")
b6=nd.get_top_names(country_alpha2="CH")
b7=nd.get_top_names(country_alpha2="CL")
b8=nd.get_top_names(country_alpha2="CM")
b9=nd.get_top_names(country_alpha2="CO")
b10=nd.get_top_names(country_alpha2="CR")
B=(b1["BH"]["M"]+b1["BH"]["F"])+(b2["BI"]["M"]+b2["BI"]["F"])+(b3["BN"]["M"]+b3["BN"]["F"])+(b4["BO"]["M"]+b4["BO"]["F"])+(b5["BW"]["M"]+b5["BW"]["F"])+(b6["CH"]["M"]+b6["CH"]["F"])+\
  (b7["CL"]["M"]+b7["CL"]["F"])+(b8["CM"]["M"]+b8["CM"]["F"])+(b9["CO"]["M"]+b9["CO"]["F"])+(b10["CR"]["M"]+b10["CR"]["F"])

c1=nd.get_top_names(country_alpha2="CY")
c2=nd.get_top_names(country_alpha2="CZ")
c3=nd.get_top_names(country_alpha2="DE")
c4=nd.get_top_names(country_alpha2="US")
c5=nd.get_top_names(country_alpha2="DJ")
c6=nd.get_top_names(country_alpha2="DK")
c7=nd.get_top_names(country_alpha2="DZ")
c8=nd.get_top_names(country_alpha2="EC")
c9=nd.get_top_names(country_alpha2="EE")
c10=nd.get_top_names(country_alpha2="ES")
C=(c1["CY"]["M"]+c1["CY"]["F"])+(c2["CZ"]["M"]+c2["CZ"]["F"])+(c3["DE"]["M"]+c3["DE"]["F"])+(c4["US"]["M"]+c4["US"]["F"])+(c5["DJ"]["M"]+c5["DJ"]["F"])+(c6["DK"]["M"]+c6["DK"]["F"])+\
  (c7["DZ"]["M"]+c7["DZ"]["F"])+(c8["EC"]["M"]+c8["EC"]["F"])+(c9["EE"]["M"]+c9["EE"]["F"])+(c10["ES"]["M"]+c10["ES"]["F"])

d1=nd.get_top_names(country_alpha2="EG")
d2=nd.get_top_names(country_alpha2="ET")
d3=nd.get_top_names(country_alpha2="FI")
d4=nd.get_top_names(country_alpha2="FJ")
d5=nd.get_top_names(country_alpha2="FR")
d6=nd.get_top_names(country_alpha2="GB")
d7=nd.get_top_names(country_alpha2="GE")
d8=nd.get_top_names(country_alpha2="GH")
d9=nd.get_top_names(country_alpha2="GR")
d10=nd.get_top_names(country_alpha2="GT")
D=(d1["EG"]["M"]+d1["EG"]["F"])+(d2["ET"]["M"]+d2["ET"]["F"])+(d3["FI"]["M"]+d3["FI"]["F"])+(d4["FJ"]["M"]+d4["FJ"]["F"])+(d5["FR"]["M"]+d5["FR"]["F"])+(d6["GB"]["M"]+d6["GB"]["F"])+\
  (d7["GE"]["M"]+d7["GE"]["F"])+(d8["GH"]["M"]+d8["GH"]["F"])+(d9["GR"]["M"]+d9["GR"]["F"])+(d10["GT"]["M"]+d10["GT"]["F"])

e1=nd.get_top_names(country_alpha2="HK")
e2=nd.get_top_names(country_alpha2="HN")
e3=nd.get_top_names(country_alpha2="HR")
e4=nd.get_top_names(country_alpha2="HT")
e5=nd.get_top_names(country_alpha2="HU")
e6=nd.get_top_names(country_alpha2="ID")
e7=nd.get_top_names(country_alpha2="IE")
e8=nd.get_top_names(country_alpha2="IL")
e9=nd.get_top_names(country_alpha2="IN")
e10=nd.get_top_names(country_alpha2="IQ")
E=(e1["HK"]["M"]+e1["HK"]["F"])+(e2["HN"]["M"]+e2["HN"]["F"])+(e3["HR"]["M"]+e3["HR"]["F"])+(e4["HT"]["M"]+e4["HT"]["F"])+(e5["HU"]["M"]+e5["HU"]["F"])+(e6["ID"]["M"]+e6["ID"]["F"])+\
  (e7["IE"]["M"]+e7["IE"]["F"])+(e8["IL"]["M"]+e8["IL"]["F"])+(e9["IN"]["M"]+e9["IN"]["F"])+(e10["IQ"]["M"]+e10["IQ"]["F"])
f1=nd.get_top_names(country_alpha2="IR")
f2=nd.get_top_names(country_alpha2="IS")
f3=nd.get_top_names(country_alpha2="IT")
f4=nd.get_top_names(country_alpha2="JM")
f5=nd.get_top_names(country_alpha2="JO")
f6=nd.get_top_names(country_alpha2="JP")
f7=nd.get_top_names(country_alpha2="KH")
f8=nd.get_top_names(country_alpha2="KR")
f9=nd.get_top_names(country_alpha2="KW")
f10=nd.get_top_names(country_alpha2="YE")
F=(f1["IR"]["M"]+f1["IR"]["F"])+(f2["IS"]["M"]+f2["IS"]["F"])+(f3["IT"]["M"]+f3["IT"]["F"])+(f4["JM"]["M"]+f4["JM"]["F"])+(f5["JO"]["M"]+f5["JO"]["F"])+(f6["JP"]["M"]+f6["JP"]["F"])+\
  (f7["KH"]["M"]+f7["KH"]["F"])+(f8["KR"]["M"]+f8["KR"]["F"])+(f9["KW"]["M"]+f9["KW"]["F"])+(f10["YE"]["M"]+f10["YE"]["F"])
g1=nd.get_top_names(country_alpha2="KZ")
g2=nd.get_top_names(country_alpha2="LB")
g3=nd.get_top_names(country_alpha2="LT")
g4=nd.get_top_names(country_alpha2="LU")
g5=nd.get_top_names(country_alpha2="LY")
g6=nd.get_top_names(country_alpha2="LT")
g7=nd.get_top_names(country_alpha2="MA")
g8=nd.get_top_names(country_alpha2="MD")
g9=nd.get_top_names(country_alpha2="MO")
g10=nd.get_top_names(country_alpha2="MU")
G=(g1["KZ"]["M"]+g1["KZ"]["F"])+(g2["LB"]["M"]+g2["LB"]["F"])+(g3["LT"]["M"]+g3["LT"]["F"])+(g4["LU"]["M"]+g4["LU"]["F"])+(g5["LY"]["M"]+g5["LY"]["F"])+(g6["LT"]["M"]+g6["LT"]["F"])+\
  (g7["MA"]["M"]+g7["MA"]["F"])+(g8["MD"]["M"]+g8["MD"]["F"])+(g9["MO"]["M"]+g9["MO"]["F"])+(g10["MU"]["M"]+g10["MU"]["F"])
h1=nd.get_top_names(country_alpha2="MV")
h2=nd.get_top_names(country_alpha2="MX")
h3=nd.get_top_names(country_alpha2="MY")
h4=nd.get_top_names(country_alpha2="NA")
h5=nd.get_top_names(country_alpha2="NG")
h6=nd.get_top_names(country_alpha2="NL")
h7=nd.get_top_names(country_alpha2="NO")
h8=nd.get_top_names(country_alpha2="OM")
h9=nd.get_top_names(country_alpha2="PA")
h10=nd.get_top_names(country_alpha2="PE")
H=(h1["MV"]["M"]+h1["MV"]["F"])+(h2["MX"]["M"]+h2["MX"]["F"])+(h3["MY"]["M"]+h3["MY"]["F"])+(h4["NA"]["M"]+h4["NA"]["F"])+(h5["NG"]["M"]+h5["NG"]["F"])+(h6["NL"]["M"]+h6["NL"]["F"])+\
  (h7["NO"]["M"]+h7["NO"]["F"])+(h8["OM"]["M"]+h8["OM"]["F"])+(h9["PA"]["M"]+h9["PA"]["F"])+(h10["PE"]["M"]+h10["PE"]["F"])
i1=nd.get_top_names(country_alpha2="PL")
i2=nd.get_top_names(country_alpha2="PR")
i3=nd.get_top_names(country_alpha2="PS")
i4=nd.get_top_names(country_alpha2="PT")
i5=nd.get_top_names(country_alpha2="QA")
i6=nd.get_top_names(country_alpha2="RS")
i7=nd.get_top_names(country_alpha2="RU")
i8=nd.get_top_names(country_alpha2="SA")
i9=nd.get_top_names(country_alpha2="SD")
i10=nd.get_top_names(country_alpha2="ZA")
I=(i1["PL"]["M"]+i1["PL"]["F"])+(i2["PR"]["M"]+i2["PR"]["F"])+(i3["PS"]["M"]+i3["PS"]["F"])+(i4["PT"]["M"]+i4["PT"]["F"])+(i5["QA"]["M"]+i5["QA"]["F"])+(i6["RS"]["M"]+i6["RS"]["F"])+\
  (i7["RU"]["M"]+i7["RU"]["F"])+(i8["SA"]["M"]+i8["SA"]["F"])+(i9["SD"]["M"]+i9["SD"]["F"])+(i10["ZA"]["M"]+i10["ZA"]["F"])
j1=nd.get_top_names(country_alpha2="SE")
j2=nd.get_top_names(country_alpha2="SG")
j3=nd.get_top_names(country_alpha2="SI")
j4=nd.get_top_names(country_alpha2="SV")
j5=nd.get_top_names(country_alpha2="SY")
j6=nd.get_top_names(country_alpha2="TM")
j7=nd.get_top_names(country_alpha2="TN")
j8=nd.get_top_names(country_alpha2="TR")
j9=nd.get_top_names(country_alpha2="TW")
j10=nd.get_top_names(country_alpha2="UY")
J=(j1["SE"]["M"]+j1["SE"]["F"])+(j2["SG"]["M"]+j2["SG"]["F"])+(j3["SI"]["M"]+j3["SI"]["F"])+(j4["SV"]["M"]+j4["SV"]["F"])+(j5["SY"]["M"]+j5["SY"]["F"])+(j6["TM"]["M"]+j6["TM"]["F"])+\
  (j7["TN"]["M"]+j7["TN"]["F"])+(j8["TR"]["M"]+j8["TR"]["F"])+(j9["TW"]["M"]+j9["TW"]["F"])+(j10["UY"]["M"]+j10["UY"]["F"])
name_list=(A+B+C+D+E+F+G+H+I+J)
# read the names in dataset using pandas
df1=pd.read_csv(r"C:\Users\VigneshSubramani\Desktop\Dataset\NAMES DATASET\name_list9.csv")
df2=pd.read_csv(r"C:\Users\VigneshSubramani\Desktop\Dataset\NAMES DATASET\name_list1.csv")
df3=pd.read_csv(r"C:\Users\VigneshSubramani\Desktop\Dataset\NAMES DATASET\name_list2.csv")
df4=pd.read_csv(r"C:\Users\VigneshSubramani\Desktop\Dataset\NAMES DATASET\name_list3.csv")
df6=pd.read_csv(r"C:\Users\VigneshSubramani\Desktop\Dataset\NAMES DATASET\name_list5.csv")
df7=pd.read_csv(r"C:\Users\VigneshSubramani\Desktop\Dataset\NAMES DATASET\name_list6.csv")
df8=pd.read_csv(r"C:\Users\VigneshSubramani\Desktop\Dataset\NAMES DATASET\name_list11.csv")#state name
df9=pd.read_csv(r"C:\Users\VigneshSubramani\Desktop\Dataset\NAMES DATASET\name_list13.csv")
df10=pd.read_csv(r"C:\Users\VigneshSubramani\Desktop\Dataset\NAMES DATASET\name_list14.csv")
df11=pd.read_csv(r"C:\Users\VigneshSubramani\Desktop\Dataset\NAMES DATASET\name_list17.csv")#state name
df12=pd.read_csv(r"C:\Users\VigneshSubramani\Desktop\Dataset\NAMES DATASET\name_list18.csv")
df13=pd.read_csv(r"C:\Users\VigneshSubramani\Desktop\Dataset\NAMES DATASET\name_list15.csv")
df14=pd.read_csv(r"C:\Users\VigneshSubramani\Desktop\Dataset\NAMES DATASET\name_list12.csv")
# convert the all dataset into list
l1=df1['AARON'].tolist()
l2=df3['FirstName'].tolist()
l3=df4["name"].tolist()
l4=df6["John"].tolist()
l5=df7["name"].tolist()
l6=df9['name'].tolist()
#l7=df10['name'].tolist()
l8=df12['name'].tolist()
l9=df13['name_clean'].tolist()
l10=df14['Name'].tolist()
l11=df2["FirstName"].tolist()
l12=df2["Surname"].tolist()
l13=df2["cleanName"].tolist()
total_name_list=name_list+(l1+l2+l3+l4+l5+l6+l8+l9+l10+l11+l12+l13)
list_lowercase = [str(element).lower() for element in total_name_list]
list_lowercase = [element for element in list_lowercase if element]
#print(len(list_lowercase))
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
            addresse1 = pyap.parse(text,country="US")
            addresse2 = pyap.parse(text, country="GB")
            addresse3 = pyap.parse(text, country="CA")
            addresses= addresse1
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