from flask import Flask,render_template,request
import pandas as pd
import numpy as np

import pickle

popular_books=pickle.load(open('popular.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
sim_score=pickle.load(open('sim_score.pkl','rb'))
final_data=pickle.load(open('final_data.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))

app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_books['Book-Title'].values),
                           image=list(popular_books['Image-URL-M'].values),
                           book_author=list(popular_books['Book-Author'].values),
                           year=list(popular_books['Year-Of-Publication'].values),
                           votes=list(popular_books['num-rating'].values),
                           rating=list(popular_books['avg-rating'].values),
                           )


@app.route('/recommend')
def index1():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['POST'])
def index2():
    user_input=request.form.get('user_input')
    b=list(books['Book-Title'])
    if user_input in b:
        idx = np.where(pt.index == user_input)[0][0]
        similar = sorted(list(enumerate(sim_score[idx])), key=lambda x: x[1], reverse=True)[1:5]
        data = []
        for i in similar:
            item = []
            temp = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp.drop_duplicates('Book-Title')['Publisher'].values))
            item.extend(list(temp.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
            item.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)
        print(data)
        return render_template('recommend.html',data=data)
    else:
        return render_template('recommend.html', data=None)
if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)
