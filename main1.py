#%pip install pyap
#%pip install datefinder
#%pip install dateparser
#%pip install nameparser
#%pip install nltk

import pyap
import datefinder
import nltk
from dateparser.search import search_dates
from nameparser import HumanName
from nltk.corpus import wordnet

nltk.download('punkt')

text = """
 1. Landlord: Giant Oaks, LLC
 2. Landlord's Representative:Larry Savage (Property Manager)
 3. Landlord's Address: 1312 West 8th Street, Anderson, IN 46016 
 4. Landlord's E-Mail Address: Larry@giantoaksanderson.com 
 5. Residents:Daynesha D. Glover 
 6. Resident's Address: 1312 W 8th St, Anderson, IN 46016 
 7. Community:Giant Oaks Apartments 
 8. Lease Start Date: 02/02/2023 
 9. Lease End Date: 02/01/2024 
 10. Deposit:$879.00
 11. Fees & Rent:
"""

addresses = pyap.parse(text, country='US')
for address in addresses:
    # shows found address
    print(address)
    # shows address parts
    #print(address.as_dict())

print ('----------------------------------------------------------------------')
matches = search_dates(text)
for date in matches:
    print(date)

print ('----------------------------------------------------------------------')

tokens = nltk.tokenize.word_tokenize(text)
pos = nltk.pos_tag(tokens)
sentt = nltk.ne_chunk(pos, binary = False)

person_list = []
person_names=person_list
person = []
name = ""
for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
    for leaf in subtree.leaves():
        person.append(leaf[0])
    if len(person) > 1:
        for part in person:
            name += part + ' '
        if name[:-1] not in person_list:
            person_list.append(name[:-1])
        name = ''
    person = []

print (person_list)