from flask import Flask, request
import sys, openai, os
sys.path.insert(1, '../')
from auth import auth
from src.data_extraction import *
os.environ['OPENAI_API_KEY'] = auth.SECRET_KEY
openai.api_key = auth.SECRET_KEY

model_name = 'babbage:ft-hackfest-gpt:babbage-ft-2023-04-10-16-58-48'

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello'

@app.route('/essay')
def evaluate_essay():
    prompt = 'Analyse the following essay:\n\n' + request.args.get('text', default = 1, type = str) + '\n\n###\n\n'
    response = openai.Completion.create(
        model=model_name,
        prompt=prompt,
        temperature=0,
        max_tokens=700
    )
    essay_eval = data_organizer(response['choices'][0].text)
    return essay_eval
    #return response['choices'][0].text

@app.route('/members')
def members():
    return {'members': ['member1', 'member2']}

if __name__ == '__main__':
    app.run(debug=True)
