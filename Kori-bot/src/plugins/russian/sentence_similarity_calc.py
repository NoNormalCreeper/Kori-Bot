from string import punctuation
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

#import nltk
#nltk.download('punkt')
#nltk.download('stopwords')

# X = input('S1 > ')
# Y = input('S2 > ')

def calculate_similarity(X, Y):
    X, Y = X.lower().strip(), Y.lower().strip()

    X = X.replace("won't", "will not")
    X = X.replace("'ll", " will")
    X = X.replace("n't", " not")
    X = X.replace("'ve", " have")
    X = X.replace("'re", " are")
    X = X.replace("'d", " would")
    X = X.replace("'m", " am")
    Y = Y.replace("won't", "will not")
    Y = Y.replace("'ll", " will")
    Y = Y.replace("n't", " not")
    Y = Y.replace("'ve", " have")
    Y = Y.replace("'re", " are")
    Y = Y.replace("'d", " would")
    Y = Y.replace("'m", " am")

    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for x in X:
        if x in punctuations:
            X = X.replace(x, "")
    for y in Y:
        if y in punctuations:
            Y = Y.replace(y, "")

    X_list = word_tokenize(X)  
    Y_list = word_tokenize(Y) 

    sw = stopwords.words('english')  
    l1 =[];l2 =[] 

    X_set = {w for w in X_list if not w in sw}  
    Y_set = {w for w in Y_list if not w in sw} 

    rvector = X_set.union(Y_set)  
    for w in rvector: 
        if w in X_set: l1.append(1)
        else: l1.append(0) 
        if w in Y_set: l2.append(1) 
        else: l2.append(0) 
    c = 0
        
    for i in range(len(rvector)): 
            c+= l1[i]*l2[i] 
    cosine = c / float((sum(l1)*sum(l2))**0.5) 
    # print("similarity: ", cosine)
    return cosine
