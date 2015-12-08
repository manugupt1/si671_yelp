import pandas as pd
from collections import Counter
import json
from pandas.io.json import json_normalize
import sys
from gensim import corpora, models, similarities
import re
from nltk.corpus import stopwords

# Changing filenames to variables
business = "yelp_academic_dataset_business.json"
checkin ="yelp_academic_dataset_checkin.json"
review = "yelp_academic_dataset_review.json"
tip  = "yelp_academic_dataset_tip.json"
user  = "yelp_academic_dataset_user.json"



def init():
    #Creates a dataframe for businesses
    with open('yelp_academic_dataset_business.json', 'rb') as f:
        data=map(lambda x: x.rstrip(), f.readlines())
        # Read the files and remove the trailing "\n" from each line

    data_json_str = "[" + ','.join(data) + "]"
    df_biz=pd.read_json(data_json_str)

    #Creates a data frame for reviews of businesses
    with open('yelp_academic_dataset_review.json', 'rb') as f:
        # Read the files and remove the trailing "\n" from each line
        data=map(lambda x: x.rstrip(), f.readlines())

    data_json_str = "[" + ','.join(data) + "]"
    df_review=pd.read_json(data_json_str)

    #Creates pickle files for business and reviews data
    df_biz_subset = df_biz[[1,2,3,13, 8, 11, 12]]
    df_biz_merged= pd.merge(df_biz_subset, df_review, on="business_id", how="inner")
    print df_biz_merged.columns
    df_biz_merged.to_pickle('df_biz_review.pkl')

def lda_cal(category, numtopics):
    reviews=""
    corpus = []
    stoplist = set(stopwords.words("english"))
    df_biz_review = pd.read_pickle('df_biz_review.pkl')
    no_biz_review =  len(df_biz_review)

    print "Calculating for",category
    for i in range(0,no_biz_review):
    #     print df_biz_review["categories"].ix[i]
        if category in df_biz_review["categories"].ix[i]:
            reviews=reviews + df_biz_review["text"].ix[i]

    # Remove punctuations
    reviews = re.sub(r'[^a-zA-Z]', ' ', reviews)
    # To lowercase
    reviews = reviews.lower()
    # Remove stop words
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
    topics =  lda.show_topics(num_topics=numtopics)
    return topics


def lda_cal(category, numtopics,df_biz_review,no_biz_review,stoplist):
    reviews=""
    corpus = []

    print "Calculating for",category
    for i in range(0,no_biz_review):
    #     print df_biz_review["categories"].ix[i]
        if category in df_biz_review["categories"].ix[i]:
            reviews=reviews + df_biz_review["text"].ix[i]

    # Remove punctuations
    reviews = re.sub(r'[^a-zA-Z]', ' ', reviews)
    # To lowercase
    reviews = reviews.lower()
    # Remove stop words
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
    topics =  lda.show_topics(num_topics=numtopics)
    return topics

if __name__ == "__main__":
    print sys.argv
    try:
        if sys.argv[1] == 'init':
            init()
        if sys.argv[1] == 'auto':
            #init()
            stoplist = set(stopwords.words("english"))
            df_biz_review = pd.read_pickle('df_biz_review.pkl')
            no_biz_review =  len(df_biz_review)
            categories = set()
            regex = re.compile('\W')
            with open('category_relations.txt','r') as input:
                for line in input:
                    line = line.rstrip().split('\t')
                    categories.add(line[0])
                    categories.add(line[1])
            print len(categories)
            for category in categories:
                category_file = regex.sub('',category)
                print category
                with open(category_file,'w') as output:
                    topics = lda_cal(category,10,df_biz_review,no_biz_review,stoplist)
                    for topic in topics:
                        output.write(str(topic) + "\n")
        if sys.argv[1] == 'lda' and sys.argv[2]:
            stoplist = set(stopwords.words("english"))
            df_biz_review = pd.read_pickle('df_biz_review.pkl')
            no_biz_review =  len(df_biz_review)
            topics = lda_cal(sys.argv[2],10,df_biz_review,no_biz_review,stoplist)
            for topic in topics:
                print topic
    except Exception as e:
        print e
