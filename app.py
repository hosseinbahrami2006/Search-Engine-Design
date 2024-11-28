from flask import Flask , render_template , request
from flask.globals import request
from project_tfidf2 import tfidf2


app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html' )

@app.route('/result', methods=['GET'])
def result():
    text = request.args.get('search')
    quote,author,link=tfidf2(text)

    return render_template('result.html',text=text , quote=quote , author=author, link=link)

@app.template_filter('subContent')
def subContent(content):
    return content[0:140] + '...'

app.jinja_env.filters['subContent'] = subContent 

if __name__=='__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()