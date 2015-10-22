__author__ = 'Manu'

import simplejson as json
from collections import Counter

''' Changing filenames to variables"'''

business = "yelp_academic_dataset_business.json"
checkin ="yelp_academic_dataset_checkin.json"
review = "yelp_academic_dataset_review.json"
tip  = "yelp_academic_dataset_tip.json"
user  = "yelp_academic_dataset_user.json"

''' categoryCount keeps track of number of businesses in each category '''
categoryCount = Counter()


with open(business,"r") as bizFile,open("categories","w") as output:
    for line in bizFile:
        string = json.loads(line)
        categories = string['categories']
        output.write(str(categories)+"\n")
        for category in categories:
            categoryCount.update((category,))
#        break

#Sort the counter, it is a list now instead of a counter
categoryCount = categoryCount.most_common()
print (type(categoryCount))

with open("categoryCountFile","w") as output:
    for item in categoryCount:
        val =  item[0] + "\t" + str(item[1]) + "\n"
        output.write (val)


#