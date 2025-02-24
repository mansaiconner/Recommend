import pandas as pd
import numpy as np

# Read the Dataset
movies = pd.read_csv('IMDB-Movie-Data.csv', usecols=['Title', 'Genre', 'Description'], nrows=500)

movies['Description'] = movies['Description'].str.lower()

# Get input from the user
input_query = input('Enter movie description: ')
input_query = input_query.lower()

# List of characters to remove
char_to_remove = ['.', '/', '!', '@', '$', '%', '&', '*', '#', '?', ',', '(', ')']

# List of words to remove
words_to_remove = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 
'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 
'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 
'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 
'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 
'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 
'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 
'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 
's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 
'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
 "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 
'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 'watch', 'like', 'movies', 'best', 'movie']

# Removes unwanted characters
for c in char_to_remove:
    input_query = input_query.replace(c, '')

# Creates a list of words from the input query and cleans the list
char_array = input_query.split()
char_array = remove_dups(char_array)
for w in words_to_remove:
    while w in char_array:
        char_array.remove(w)
for e in char_array:
    if '-' in e:
        term = e.split('-')
        for ll in term:
            char_array.append(ll)
        char_array.remove(e)
user_prompt = char_array

G = []
D =[]
check = []
#### iterate through the movie dataset

for p in range(len(movies)):
    genre = movies['Genre'][p]
    description = movies['Description'][p]
    for y in char_to_remove:
        description = description.replace(y, '')
    #### clean the data
    if ',' in genre:
        genre = genre.split(',')
    else: 
        genre = [genre]
    for l, e in enumerate(genre):
        if '-' in e:
            g = e.split('-')
            for j in range(len(g)):
                #print(len(g))
                genre.append(g[j])
            genre.remove(e)
    description = description.split()
    for w in words_to_remove:
        while w in description:
            description.remove(w)
    temp = []
    for num, des in enumerate(description):
        #temp = []
        for cha in char_to_remove:
            if cha in des:
                if cha in temp:
                    pass
                else:
                    temp.append(cha)
    for te in temp:
        while te in description:
            description.remove(te)
            
    G.append(genre)
    D.append(description)


### Stores the similarity values in a list 
values = []
doc_counts = 0
for p in range(len(G)):
    wordcount = 0
    doccount = 0
    for word in char_array:
        for s in range(len(G)):
            if word in G[s]:
                doccount += 1
            elif word in D[s]:
                doccount += 1
        for gen in G[p]:
            if gen == word:
                wordcount += 1
        for desc in D[p]:
            if desc == word:
                wordcount += 1
    num = wordcount/ (len(G[p]) + len(D[p]))
    values.append((wordcount/(len(G[p]) + len(D[p]))) *  (float(np.log(len(G)/doccount))))



### Prints out the top five movies that match the users input
for i in range(5):
    maxval = max(values)
    index = values.index(maxval)
    values[index] = 0
    print(movies['Title'][index])
