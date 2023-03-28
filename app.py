import re
import pandas as pd
import numpy as np
import sqlite3
from terbilang import Terbilang


from flask import Flask, jsonify
from Database import Database as db

app = Flask(__name__)

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
    'version': LazyString(lambda: '1.0.0'),
    'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,             
                  config=swagger_config)


@swag_from("docs/text_sensor.yml", methods=['POST'])
@app.route('/text_sensor', methods=['POST'])
def text_sensor():
  
    #upload file
    text = request.form.get('text')
    #read file
    abusive = pd.read_csv('abusive.csv', encoding = 'ISO-8859-1')
    
    #cleansing data
    listo=[]
    for ind in abusive.index:
        b=abusive['ABUSIVE'][ind]
        listo.append(b)
    #abusive = ['Bau', 'alay']
    
    split_text = re.split(' ', text)
    
    for i in split_text:
        for j in listo:
            if i == j:
                index=split_text.index(i)
                split_text[index] = '**sensor**'
                
    list_text = ' '.join(map(str, split_text))
    
    json_response = {
        'status_code': 200,
        'description': "Teks sudah diproses",
        'data': re.sub(r'[^a-zA-Z0-9*]',' ', list_text),
    }
    
    response_data = jsonify(json_response)
    return response_data


### POST input text and cleaning
@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():

    #input text
    text = request.form.get('text')
    
    #read kamusalay
    kamusalay = pd.read_csv('new_kamusalay.csv', encoding = 'ISO-8859-1', names=['old', 'new'])
    
    #cleasing data
    def cleaning_data(text):
        text=text.lower()
        text=re.sub('url', ' ', text)
        text=re.sub('url\S+', ' ', text) #change Url+other word/special character
        text=re.sub(r'#\S+',' ' , text)
        text=re.sub(r'@', ' ', text)
        text=re.sub(r'&amp;', 'dan', text)
        text=re.sub(r'http:\S+', ' ', text)
        text=re.sub(r'\\n', ' ', text)
        text=re.sub(r'(\\x(.){2})', ' ', text) #remove emoticon
        text=re.sub(r'[^a-zA-Z0-9]', ' ', text)
        text=re.sub(r'\s+', ' ', text)
        
        return text
    
    #Split data
    text=cleaning_data(text)
    text=text.split()
    #asd=np.where(kamusalay['anakjakartaasikasik']==text)
    
    #change number to word
    t = Terbilang()
    
    titip=[]
    for ch in text:
        if ch.isdigit()==True:
            ch = t.parse(ch).getresult()
        else:
            ch = ch
        titip.append(ch)


    #check with 
    temporary=[]
    result = ""
    for tweets in titip:
        temp =[]
        if type(tweets) is list:
            for tweet in tweets:
                try:
                    trying = np.where(kamusalay['old']==tweet)[0][0]
                    tweet = kamusalay['new'].iloc[trying]
                except:
                    tweet = tweet
                temp.append(tweet)
                result = result + " " + tweet
            temporary.append(temp)
        else:
            try:
                trying = np.where(kamusalay['old']==tweets)[0][0]
                tweets = kamusalay['new'].iloc[trying]
            except:
                tweets = tweets
            temporary.append(tweets)
            result = result + " " + tweets
    db.insert_database(result)

    
    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': temporary, #re.sub(r'[^a-zA-Z0-9]', ' ', text),
        
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text_processing_file.yml", methods=['POST'])
@app.route('/text-processing-file', methods=['POST'])
def text_processing_file():

    # Upladed file
    file = request.files.getlist('file')[0]
    
    #read kamusalay
    kamusalay = pd.read_csv('new_kamusalay.csv', encoding = 'ISO-8859-1', names=['old', 'new'])
    
    # Import file csv ke Pandas
    df = pd.read_csv(file, names=['text'], encoding='ISO-8859-1')

    # Ambil teks yang akan diproses dalam format list
    texts=df.text.to_list()
    #texts = df.values.tolist()

    t = Terbilang()
    
    # Lakukan cleansing pada teks
    def cleaning_data(text):
        text=text.lower()
        text=re.sub('URL', ' ', text)
        text=re.sub('URL\S+',' ', text) #change URL to space
        text=re.sub('Url\S+', ' ', text) #change Url+other word/special character
        text=re.sub(r'#\S+',' ' , text)
        text=re.sub(r'@', ' ', text)
        text=re.sub(r'&amp;', 'dan', text)
        text=re.sub(r'http:\S+', ' ', text)
        text=re.sub(r'\\n', ' ', text)
        text=re.sub(r'(\\x(.){2})', ' ', text) #remove emoticon
        text=re.sub(r'[^a-zA-Z0-9]', ' ', text)
        text=re.sub(r'\s+', ' ', text)
        
        return text
    
    def convert(lst):
        return ''.join(lst).split()

    #text=convert(cleaned_text)
    
    def filter_data(text):
        result = ""
        tweets = text
        #print(tweets)
        temp=[]
        for tweet in tweets:
            try:
                trying = np.where(kamusalay['old']==tweet)[0][0]
                tweet = kamusalay['new'].iloc[trying]
            except:
                tweet = tweet
            #print(tweet)
            temp.append(tweet)
            result = result + " " + tweet
        return result
    
    #change number to word
    def tersebut(text):
        titip=[]
        for ab in convert(text):
            if ab.isdigit()==True:
                ab = t.parse(ab).getresult()
            else:
                ab = ab
            titip.append(ab)
        return titip
            
    cleaned_text =[]
    for text in texts:
        #cleaned_text.append(cleaning_data(text))
        text=cleaning_data(text)
        text=tersebut(text)
        text=filter_data(text)
        cleaned_text.append(text)
        db.insert_database(text)

    
    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': cleaned_text,
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
    db.create_database()
    app.run()

