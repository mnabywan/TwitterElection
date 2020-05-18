import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('punkt')
import morfeusz2
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from ttp import ttp
from collections import Counter
import numpy as np
from pandas.core.common import flatten
import re

DUDA = "Duda"
KIDAWA = "Kidawa"
KOSINIAK = "Kosiniak"
BIEDRON = "Biedron"
BOSAK = "Bosak"
HOLOWNIA = "Holownia"

CANDIDATES = [DUDA, KIDAWA, KOSINIAK, BIEDRON, BOSAK, HOLOWNIA]

DUDA_ACCOUNTS = ['AndrzejDuda', 'AndrzejDuda2020', 'mecenasJTK', 'jbrudzinski', 'AdamBielan', 'pisorgpl']
KIDAWA_ACCOUNTS = ['M_K_Blonska', 'adamSzlapka', 'Arlukowicz', 'Platforma_org']
BIEDRON_ACCOUNTS = ['RobertBiedron', 'poselTTrela', 'B_Maciejewska', '__Lewica']
KOSINIAK_ACCOUNTS = ['KosiniakKamysz', 'magdasobkowiak', 'DariuszKlimczak', 'nowePSL']
BOSAK_ACCOUNTS = ['krzysztofbosak', 'Bosak2020', 'PUsiadek', 'annabrylka', 'Konfederacja_']
HOLOWNIA_ACCOUNTS = ['szymon_holownia', 'michalkobosko']

def add_candidate(name):
    if name in DUDA_ACCOUNTS:
        return DUDA
    if name in KIDAWA_ACCOUNTS:
        return KIDAWA
    if name in BIEDRON_ACCOUNTS:
        return BIEDRON
    if name in KOSINIAK_ACCOUNTS:
        return KOSINIAK
    if name in BOSAK_ACCOUNTS:
        return BOSAK
    if name in HOLOWNIA_ACCOUNTS:
        return HOLOWNIA
    else: 
        return "undefined"
		

def validate(string):
    txt = "The rain in Spain"
    x = re.search("[a-zA-Z]", txt)

    if (x):
      return True
    else:
      return False
	  
def lemm(f):
    try:
        morf = morfeusz2.Morfeusz()
        analysis=morf.analyse(f)
        return analysis[0][2][1]
    except:
        return ''

def create_word_cloud(data,column):
    bigstring = data[column].apply(lambda x: ' '.join(x)).str.cat(sep=' ')
    plt.figure(figsize=(12,12))
    wordcloud = WordCloud(stopwords=STOPWORDS,
                              background_color='white',
                              collocations=False,
                              width=1200,
                              height=1000
                             ).generate(bigstring)
    plt.axis('off')
    plt.imshow(wordcloud)
	#return wordcloud


def plot_chart(data,column):
    p=[]
    bigstring = data[column].apply(lambda x: p.append(x))
    p=list(flatten(p))

    labels, values = zip(*Counter(p).most_common(10))

    plt.figure(figsize=(20,12))
    indexes = np.arange(len(labels))
    width = 1

    plt.bar(indexes, values, width)
    plt.xticks(indexes + width*0.1, labels)
    plt.show()

    items, counts = zip(*Counter(p).most_common(10))
    df= pd.Series(counts, index=items)
	

def most_common_words(data):
    sp=[]
    k=data['processed_text'].apply(lambda x: sp.append(x))
    sp=list(flatten(sp))
    return Counter(sp).most_common(6)
	

def tags_list(data):
    sp=[]
    k=data['tags'].apply(lambda x: sp.append(x))
    sp=list(flatten(sp))
    return sp
	
#chart of user reply tweets
def reply(data):
    sp=[]
    k=duda_data['in_reply_to_screen_name'].apply(lambda x: sp.append(x))
    sp=list(flatten(sp))
    res=[]
    sp=Counter(sp).most_common(6)
    for val in sp: 
        if val[0] is not  None : 
            res.append(val)
            
    labels, values = zip(*res)

    plt.figure(figsize=(20,12))
    indexes = np.arange(len(labels))
    width = 1

    plt.bar(indexes, values, width)
    plt.xticks(indexes + width*0.1, labels)
    plt.show()

    items, counts = zip(*res)
    df= pd.Series(counts, index=items)
    print(df)
	
#cosine similarity between two vectors
def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(data):
    sp=[]
    k=data['processed_text'].apply(lambda x: sp.append(x))
    sp=list(flatten(sp))
    return Counter(sp)

	
'''loads tweets to dataframe and add columns: processed_text (polish basic words only, hashtags,user- screen user name of the tweet creator, candidate - name of the candidate, the user "belongs to" '''

def prepare_data():
    data = pd.read_json('candidatedb.json') 
    print(data) 
    additional  = ['rt','rts','retweet']
    swords = set(nltk.corpus.stopwords.words('polish'))
    data.drop_duplicates(subset='full_text',inplace=True)
    data['processed_text'] = data['full_text'].str.lower()\
            .str.replace('@\w+','')\
            .str.replace('#\w+','')\
            .str.replace('(http|https):\/\/\w+.+[^ alt]', '')\
            .str.replace('[,-:()-]',' ')\
            .apply(lambda x: [i for i in x.split() if i.isalpha() and len(i)>1])\
            .apply(lambda x: [i for i in x if not i in swords])
    p = ttp.Parser()
    data['tags']=data['full_text'].apply(lambda x: p.parse(x).tags)
    data['candidate']=data['user'].apply(lambda x: add_candidate(x.get('screen_name')))
    data['user_name']=data['user'].apply(lambda x: x.get('screen_name'))
    candidate_dataframes=[]
    duda_data=data.loc[data['candidate'] == DUDA]
    candidate_dataframes.append((duda_data,DUDA))
    kidawa_data=data.loc[data['candidate'] == KIDAWA]
    candidate_dataframes.append((kidawa_data,KIDAWA))
    bosak_data=data.loc[data['candidate'] == BOSAK]
    candidate_dataframes.append((bosak_data,BOSAK))
    kosiniak_data=data.loc[data['candidate'] == KOSINIAK]
    candidate_dataframes.append((kosiniak_data,KOSINIAK))
    biedron_data=data.loc[data['candidate'] == BIEDRON]
    candidate_dataframes.append((biedron_data,BIEDRON))
    holownia_data=data.loc[data['candidate'] == HOLOWNIA]		
    candidate_dataframes.append((holownia_data,HOLOWNIA))
    return data,candidate_dataframes
	
data,cf=prepare_data()
print(data)

'''
examples of uses:

-show similarities of tweet texts between all candidates
c[0]- concatenated tweets as a list of words
c[1]- candidate name

for c in candidate_dataframes:
    for ca in candidate_dataframes:
        if(c[1]==ca[1]):
            continue
        print(str(c[1])+"-"+str(ca[1]))
        print(get_cosine(text_to_vector(c[0]), text_to_vector(ca[0])))

-create word cloud of hashtags of duda candidate
create_word_cloud(duda_data,'tags')
-create chart of most used words from tweets of duda president
plot_chart(duda_data,'processed_text')		
	