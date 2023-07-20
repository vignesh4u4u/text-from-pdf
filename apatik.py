from flask import Flask, request, render_template, json, jsonify
from pdfminer.high_level import extract_text
from nameparser import HumanName
import datefinder
from dateutil import parser
import dateutil.parser as dp
import pyap
import spacy
nlp = spacy.load("en_core_web_sm")
text = extract_text('Lease6.pdf')
import re


#file_path = 'path/to/your/file.txt'

#with open(file_path, 'r') as file:
    #text = file.read()

# Define a regex pattern to match date patterns
date_pattern = r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|' \
               r'\d{1,2}(?:st|nd|rd|th)? \w+ \d{2,4}|' \
               r'\d{1,2} \w+ \d{2,4}|' \
               r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{2,4})\b'

# Find all matches of the date pattern in the text
matches = re.findall(date_pattern, text)

# Parse the matched dates using dateutil
dates = [dp.parse(match, fuzzy=True) for match in matches]

# Print the extracted dates
for date in dates:
    pass
    #print(date)

print("------name prediction------------")


# The extracted_names dictionary from the provided output
extracted_names = {
"Name_1": "TENANTherebyagreestopaythesum Dollars",
    "Name_10": "MAINTENANCE TENANTagreesthatnorepresentationastoconditionorrepairofpremisesandnopromisetodecorate",
    "Name_11": "Landlord",
    "Name_12": "Eric Lewis Responsibilties",
    "Name_13": "Landlord",
    "Name_14": "Pull",
    "Name_15": "Closet Rod Keys Returned Light Fixtures",
    "Name_16": "Sills Baseboards Shower",
    "Name_17": "Holder Blinds",
    "Name_18": "Windows Must",
    "Name_19": "Garages",
    "Name_2": "Schuyler Avenue",
    "Name_20": "Resident",
    "Name_21": "Eric Lewis Emergencies",
    "Name_22": "Resident",
    "Name_23": "Fire Call",
    "Name_24": "Eric Lewis Miscellaneous",
    "Name_25": "Clogged Backed Toilet ThismaybeconsideredanemergencyONLYifthereisonlyonetoiletintheunitANDyouhavemadeeveryeffort",
    "Name_26": "Locked",
    "Name_27": "Eric Lewis",
    "Name_28": "Dave Crandall",
    "Name_29": "Eric Lewis Lessee",
    "Name_3": "Eric Lewis",
    "Name_4": "LANDLORD Eric",
    "Name_5": "Ifthepremisesofthebuildingaresubstantiallydamagedby",
    "Name_6": "Landlord",
    "Name_7": "Tenant",
    "Name_8": "Lease Term Tenant",
    "Name_9": "LANDLORD"
}

"""def is_valid_human_name(name):
    if not re.search(r'[a-zA-Z]', name) or name.isupper():
        return False

    parsed_name = HumanName(name)
    return bool(parsed_name.first and parsed_name.last)

valid_human_names = {}

for key, name in extracted_names.items():
    if is_valid_human_name(name):
        valid_human_names[key] = name

print(valid_human_names)"""

print("-------signature detect------")
import cv2
import pytesseract
import pdfplumber

# Provide the path to the PDF file
pdf_path = 'Lease6.pdf'


# Function to extract text from an image using pytesseract
def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text


# Function to process each page of the PDF and extract signatures
def extract_signatures_from_pdf(pdf_path):
    signatures = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            images = page.images
            for idx, img in enumerate(images):
                image_path = f"page_{page_num}_image_{idx}.png"
                with open(image_path, 'wb') as f:
                    f.write(img['stream'].get_object().get_data())

                # Extract text from the image
                signature_text = extract_text_from_image(image_path)
                signatures.append(signature_text)

                # Remove the temporary image file
                os.remove(image_path)

    return signatures


if __name__ == "__main__":
    signatures = extract_signatures_from_pdf(pdf_path)
    for idx, signature_text in enumerate(signatures, start=1):
        print(f"Signature {idx}: {signature_text}")
