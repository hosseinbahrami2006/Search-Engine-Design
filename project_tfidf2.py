
def tfidf2(text):
    from sklearn.feature_extraction.text import TfidfTransformer,CountVectorizer
    from sklearn.pipeline import Pipeline
    import numpy as np
    import pandas as pd
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "data.xlsx")

    data = pd.read_excel(file_path)

    #------------> document tf-idf
    pipe = Pipeline([('count', CountVectorizer()),
                    ('tfid', TfidfTransformer())]).fit(data['quote text'])

    tf = pipe['count'].transform(data['quote text']).toarray()
    idf = pipe['tfid'].idf_

    tfidf = []
    for i in range(len(tf)):
        tfidf.append(tf[i, :] * idf)

    #------------> input tf-idf
        
    user_input = [text]
    input_tf = pipe['count'].transform(user_input).toarray()
    input_tfidf = input_tf[0] * idf

    #------------> cosine dist between <user input> and <document>
    def cosine_dist(x,y):
        xy = 0
        for i in range(len(x)): 
            xy = xy + (x[i] * y[i])
        return xy

    distances = []
    for i in range(len(data['quote text'])):
        distances.append(cosine_dist(tfidf[i], input_tfidf))
        
    quote = data['quote text']
    
    link = data['quote link']    
    quote = data['quote text']
    author = data['quote author']
    temp = list(distances)
    temp.sort()
    most_sim = temp[-10:]

    author_2=[]
    quote_2=[]
    link_2=[]
    for i in most_sim:
        index = distances.index(i)
        author_2.append(author[index])
        link_2.append(link[index])
        quote_2.append(quote[index])
    
    
    return quote_2 , author_2 , link_2

