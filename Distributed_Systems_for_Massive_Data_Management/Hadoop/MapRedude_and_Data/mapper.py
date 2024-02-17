#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
mapper2.py
Files associated with 1º Loop - Miniwords.txt / words.txt

import sys

for line in sys.stdin:
    language, word = line.split()
    
    #sys.stderr.write("Mapper Input: ({0}, {1})\n".format(language, word))
    print ("{0}\t{1}".format(word, language))
    #sys.stderr.write("Mapper Output: ({0}, {1})\n".format(word, language))
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""mapper.py
2. Vente total par ville et produit (Ville, produit, vente total) # Normal
import sys

for line in sys.stdin:
    clean_line_split = [chunk.strip() for chunk in line.split("|")]
    #sys.stderr.write("\nstrip:{0}".format(clean_line_split))
    date = clean_line_split[0][6:]
    price = clean_line_split[4]
    method = clean_line_split[5]
    #sys.stderr.write("\ndate:{0}".format(date))
    #sys.stderr.write("\nmethod:{0}".format(method))
    #sys.stderr.write("Mapper Output: {0} {1} {2}".format(date, price, method))
    print("{0}\t{1}\t{2}".format(date, price, method))

"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"3. Identifier le produit le plus vendu par mois et ville basé sur le nº de produit (unité pas prix) vendu (Ville, Mois, Produit) # A bit more difficult"
" do first a best product in terms of amount of sell"
import sys

for line in sys.stdin:
    clean_line_split = [chunk.strip() for chunk in line.split("|")]
    city = clean_line_split[2]
    date = clean_line_split[0][3:]
    item = clean_line_split[3]
    print("{0}-{1}\t{2}".format(city, date, item))
