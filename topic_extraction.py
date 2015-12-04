
# coding: utf-8

# In[1]:

import pandas as pd
from collections import Counter
import json
from pandas.io.json import json_normalize

# Changing filenames to variables

business = "yelp_academic_dataset_business.json"
checkin ="yelp_academic_dataset_checkin.json"
review = "yelp_academic_dataset_review.json"
tip  = "yelp_academic_dataset_tip.json"
user  = "yelp_academic_dataset_user.json"


# In[47]:

#Creates a dataframe for businesses

# with open('yelp_academic_dataset_business.json', 'rb') as f:
# #     data = f.readlines()
#     data=map(lambda x: x.rstrip(), f.readlines())
    
# # remove the trailing "\n" from each line
# # data = map(lambda x: x.rstrip(), data)

# data_json_str = "[" + ','.join(data) + "]"
# df_biz=pd.read_json(data_json_str)


# In[3]:

#Creates a data frame for reviews of businesses
# with open('yelp_academic_dataset_review.json', 'rb') as f:
# #     data = f.readlines(1)
#     data=map(lambda x: x.rstrip(), f.readlines())

# # remove the trailing "\n" from each line
# # data = map(lambda x: x.rstrip(), data)

# data_json_str = "[" + ','.join(data) + "]"
# df_review=pd.read_json(data_json_str)


# In[5]:

#Creates pickle files for business and reviews data

# df_biz.to_pickle('business_dataframe.pkl')
# df_review.to_pickle('reviews_dataframe.pkl')


# In[59]:

#Read data from pickle files

# df_biz= pd.read_pickle('business_dataframe.pkl')
# df_review = pd.read_pickle('reviews_dataframe.pkl')


# In[7]:

print df_biz.columns
df_review.columns


# In[2]:

# df_biz_subset = df_biz[[1,2,3,13, 8, 11, 12]]
# df_biz_review= pd.merge(df_biz_subset, df_review, on="business_id", how="inner")

# df_biz_review.to_pickle('df_biz_review.pkl')

df_biz_review= pd.read_pickle('df_biz_review.pkl')
print len(df_biz_review)

# biz_categories = set(c for cat in df_biz_review["categories"] for c in cat)


# In[19]:

# pd.unique(df_biz_review.categories.ravel())
biz_categories = set(c for cat in df_biz_review["categories"] for c in cat)
biz_categories


# In[3]:

from gensim import corpora, models, similarities
import re
from nltk.corpus import stopwords


# In[35]:

# i=df_biz_review["categories"].index
stoplist = set(stopwords.words("english"))

def lda_cal(category, numtopics):
    reviews=""
    corpus = []
    for i in range(0,1569264):
    #     print df_biz_review["categories"].ix[i]
        if category in df_biz_review["categories"].ix[i]:
            reviews=reviews + df_biz_review["text"].ix[i]
    # Remove punctuations
    reviews = re.sub(r'[^a-zA-Z]', ' ', reviews)

    # # To lowercase
    reviews = reviews.lower()

    # # Remove stop words
    texts = [word for word in reviews.lower().split() if word not in stoplist]

    corpus.append(texts)
    # corpus
    # # Build dictionary
    dictionary = corpora.Dictionary(corpus)
    dictionary.save('restaurant_reviews.dict')

    # # Build vectorized corpus
    corpus_2 = [dictionary.doc2bow(text) for text in corpus]
    # corpus_2
    lda = models.LdaModel(corpus_2, num_topics=numtopics, id2word=dictionary)
    return lda.show_topics(num_topics=numtopics)


# In[36]:

lda_cal("Doctors", 5)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



