__author__ = 'Manu'

from collections import Counter
from itertools import combinations
import operator

import simplejson as json

from math import log

''' Changing filenames to variables"'''

business = "yelp_academic_dataset_business.json"
checkin ="yelp_academic_dataset_checkin.json"
review = "yelp_academic_dataset_review.json"
tip  = "yelp_academic_dataset_tip.json"
user  = "yelp_academic_dataset_user.json"


''' categoryCount keeps track of number of businesses in each category '''
categoryCount = Counter()
categoryRelationships = Counter()


with open(business,"r") as bizFile,open("categories","w") as output:
    for line in bizFile:
        string = json.loads(line)
        categories = string['categories']
        output.write(str(categories)+"\n")
        x = combinations(categories, 2)
        for i in x:
            categoryRelationships.update((i,))
        for category in categories:
            categoryCount.update((category,))


# #Sort the counter, it is a list now instead of a counter
# categoryCount = categoryCount.most_common()

#
# with open("categoryCountFile","w") as output:
#     for key,value in categoryCount.items():
#         val =  key + "\t" + str(value) + "\n"
#         output.write (val)
#
# # Relationships between two categories
# categoryRelationships = categoryRelationships.most_common()
# with open("categoryRelationships", "w") as output:
#     for item in categoryRelationships:
#         val = str(item[0]) + "\t" + str(item[1]) + "\n"
#         output.write(val)


pmi = {}
for key,value in categoryRelationships.items():
    mult = float(categoryCount[key[0]]) * float(categoryCount[key[1]])
    pmi[key] = log(value/mult)


sorted_pmi = sorted(pmi.items(),key = operator.itemgetter(0,1))

print (sorted_pmi)
# for key,value in pmi.items():
#     print (key,value)



# Finding out the number of businesses in every cities
# city = Counter()
# with open(business,"r") as file,open("city","w") as output:
#     for line in file:
#         string = json.loads(line)
#         string = string['city'].strip()
#         city.update((string,))
#
#
# city = city.most_common()
#
# with open("city","w") as output:
#     for item in city:
#         val =  item[0] + "\t" + str(item[1]) + "\n"
#         output.write (val)
#


