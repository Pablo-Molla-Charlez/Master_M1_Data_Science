#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
reducer.py
Files associated to 1º Loop - Miniwords.txt / words.txt

"""
"""
import sys

language_list = []
current_language_list = []
word = None
counter = 0
for line in sys.stdin:

    try: #extraction
        current_word, current_language = line.split("\t") # patate, french
        #sys.stderr.write("\nReducer Input: {0}, {1}".format(current_word, current_language))
        current_language_list.append(current_language[:-1]) # [french]
        #sys.stderr.write("Reducer Variables: {0}, {1}, {2}\n".format(current_word, current_language[:-1], current_language_list))
    except ValueError:
        continue
    
    if (current_word == word): # old and new the same
        #print("\n{0} = {1}".format(current_word, word))
        #print("{0} not in {1}".format(current_language[:-1], language_list))
        if (current_language[:-1] not in language_list) and (current_language[:-1] == "fran\xc3\xa7ais" or current_language[:-1] == "english"): # new language is english or french and not included in old language list
            #sys.stderr.write("\nSame word: {0} - New language: {1}\n".format(current_word, current_language))
            language_list.append(current_language[:-1])
            #sys.stderr.write("Language_list: {0}\n".format(language_list))
            current_language_list = []
        else:
            word = current_word
            current_language_list = []
    
    else: # if not current_word == word
        
        if not word: # new word
            word = current_word # patate
            #sys.stderr.write("\nCreation word: {0}".format(word))
            language_list = current_language_list # [french]
            current_language_list = []
            #sys.stderr.write("\nCreation Variables: (word: {0}, language_list: {1}, current_language_list: {2})".format(word, language_list, current_language_list))
        
        else:
            if len(language_list) == 2:
                print("\nOutput Reducer ({0}, {1})".format(word, language_list))
            # reset
            word = current_word
            language_list = []
            if (current_language[:-1] == "fran\xc3\xa7ais" or current_language[:-1] == "english"):
                language_list.append(current_language[:-1])
            current_language_list = []
            #sys.stderr.write("\nReducer Variables: {0}, {1}, {2}".format(word, language_list, current_language_list))
    
# Loop for finished - last word       
if len(language_list) == 2:
    print("\nOutput Reducer ({0}, {1})".format(word, language_list))

"""


"""reducer.py

import sys
total_price_cash = 0
total_price_online = 0
total_price_card = 0
old_date = None

for line in sys.stdin:
    current_date, current_price, current_method = line.split("\t")[0], int(line.split("\t")[1]), line.split("\t")[2][:-1]
    if current_date == old_date: # Consecutive same year
        if current_method == "online":
            total_price_online = total_price_online + current_price
        if current_method == "credit card":
            total_price_card = total_price_card + current_price
        if current_method == "cash":
            total_price_cash = total_price_cash + current_price
    else: # Creation
        
        if old_date != None:
            print("\nOutput Reducer: {0} cash {1}".format(old_date, total_price_cash))
            print("Output Reducer: {0} online {1}".format(old_date, total_price_online))
            print("Output Reducer: {0} credit card {1}".format(old_date, total_price_card))
        
        old_date = current_date
        total_price_cash = 0
        total_price_online = 0
        total_price_card = 0
        if current_method == "online":
            total_price_online = current_price
        if current_method == "credit card":
            total_price_card = current_price
        if current_method == "cash":
            total_price_cash = current_price
"""

"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
best_product = None
old_city = None

for line in sys.stdin:
    current_city, current_item, current_price = line.split("\t")[0], line.split("\t")[1], int(line.split("\t")[2])

    if current_city == old_city:
        if current_item == "ballon":
            total_price_b = total_price_b + current_price
        if current_item == "t-shirt":
            total_price_t = total_price_t + current_price
        if current_item == "soulier":
            total_price_s = total_price_s + current_price
        if current_item == "cap":
            total_price_c = total_price_c + current_price
        if current_item == "jersey":
            total_price_j = total_price_j +current_price

    else:
        if old_city != None:
            best_product = max(total_price_b, total_price_c, total_price_t, total_price_j, total_price_s)
            if total_price_b == best_product:
                print("\n In {0}, the best product is the ballon with a revenue of {1}€".format(old_city, total_price_b))
            if total_price_c == best_product:
                print("\n In {0}, the best product is the cap with a revenue of {1}€".format(old_city, total_price_c))
            if total_price_t == best_product:
                print("\n In {0}, the best product is the t-shirt with a revenue of {1}€".format(old_city, total_price_t))
            if total_price_j == best_product:
                print("\n In {0}, the best product is the jersey with a revenue of {1}€".format(old_city, total_price_j))
            if total_price_s == best_product:
                print("\n In {0}, the best product is the soulier with a revenue of {1}€".format(old_city, total_price_s))

        old_city = current_city
        total_price_b = 0
        total_price_t = 0
        total_price_s = 0
        total_price_c = 0
        total_price_j = 0
        if current_item == "ballon":
            total_price_b = current_price
        if current_item == "t-shirt":
            total_price_t = current_price
        if current_item == "soulier":
            total_price_s = current_price
        if current_item == "cap":
            total_price_c = current_price
        if current_item == "jersey":
            total_price_j = current_price
"""                

import sys

counter_b = 0
counter_t = 0
counter_s = 0
counter_c = 0
counter_j = 0
old_city = None
old_date = None

for line in sys.stdin:
    line = line.strip()
    key, current_item = line.split('\t', 1)
    current_city, current_date = key.split('-', 1)

    # current_city, current_date, current_item
    if current_city == old_city:
        if current_date == old_date:
            if current_item == "ballon":
                counter_b = counter_b + 1
            if current_item == "t-shirt":
                counter_t = counter_t + 1
            if current_item == "soulier":
                counter_s = counter_s + 1
            if current_item == "cap":
                counter_c = counter_c + 1
            if current_item == "jersey":
                counter_j = counter_j + 1

        else: # not same date within same city
            best_value = max(counter_b, counter_t, counter_s, counter_c, counter_j)
            if best_value == counter_b:
                best_product = "ballon"
            if best_value == counter_t:
                best_product = "t-shirt"
            if best_value == counter_s:
                best_product = "soulier"
            if best_value == counter_c:
                best_product = "cap"
            if best_value == counter_j:
                best_product = "jersey"
            
            print("\nIn {0}, during {1} the best product was:{2}".format(old_city, old_date, best_product))
            sys.stderr.write("New date = {0}, Old date = {1}".format(current_date, old_date))
            sys.stderr.write("\nballon = {0}, t-shirt = {1}, soulier = {2}, cap = {3}, jersey = {4}\n".format(counter_b, counter_t, counter_s, counter_c, counter_j))
            counter_b, counter_t, counter_s, counter_c, counter_j = 0, 0, 0, 0, 0
            old_date = current_date
            
            if current_item == "ballon":
                counter_b = counter_b + 1
            if current_item == "t-shirt":
                counter_t = counter_t + 1
            if current_item == "soulier":
                counter_s = counter_s + 1
            if current_item == "cap":
                counter_c = counter_c + 1
            if current_item == "jersey":
                counter_j = counter_j + 1

    else: #current_city != old_city

        if old_city != None: # different city, we need to print and reset
            
            best_value = max(counter_b, counter_t, counter_s, counter_c, counter_j)
            if best_value == counter_b:
                best_product = "ballon"
            if best_value == counter_t:
                best_product = "t-shirt"
            if best_value == counter_s:
                best_product = "soulier"
            if best_value == counter_c:
                best_product = "cap"
            if best_value == counter_j:
                best_product = "jersey"
            
            print("\nIn {0}, during {1} the best product was:{2}".format(old_city, old_date, best_product))
            sys.stderr.write("\nNew City = {0}, Old City = {1}".format(current_city, old_city))
            sys.stderr.write("\nballon = {0}, t-shirt = {1}, soulier = {2}, cap = {3}, jersey = {4}\n".format(counter_b, counter_t, counter_s, counter_c, counter_j))
            
            counter_b, counter_t, counter_s, counter_c, counter_j = 0, 0, 0, 0, 0
            old_date = current_date
            old_city = current_city

            if current_item == "ballon":
                counter_b = counter_b + 1
            if current_item == "t-shirt":
                counter_t = counter_t + 1
            if current_item == "soulier":
                counter_s = counter_s + 1
            if current_item == "cap":
                counter_c = counter_c + 1
            if current_item == "jersey":
                counter_j = counter_j + 1

        if old_city == None: # Creation
            old_city = current_city
            old_date = current_date
        
            if current_item == "ballon":
                counter_b = counter_b + 1
            if current_item == "t-shirt":
                counter_t = counter_t + 1
            if current_item == "soulier":
                counter_s = counter_s + 1
            if current_item == "cap":
                counter_c = counter_c + 1
            if current_item == "jersey":
                counter_j = counter_j + 1


        
        
    





