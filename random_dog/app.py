from flask import Flask, render_template
import requests

# Import database file
from database import db

app = Flask(__name__)

# app.secret_key = os.environ['flask_secret_key']

# app.config['SESSION_COOKIE_SAMESITE'] = 'None'
# app.config['SESSION_COOKIE_SECURE'] = True


@app.route('/')
def home():
  return render_template('test.html')


@app.route('/get_dog')
def get_dog():
  response = requests.get('https://dog.ceo/api/breeds/image/random')

  data = response.json() 

  dog_image = data['message']

  db['total_dogs_generated'] += 1
  
  return render_template('test.html',
   dog=dog_image,
   dogs_generated=db['total_dogs_generated'])


'''
Create route for logout
'''
@app.route('/logout')
def logout():
  return 'LOGOUT PAGE'

if __name__ == "__main__":
    # Replit server config
    # app.run(debug=True,host='0.0.0.0', port=81)

    # Local server config
    app.run(debug=True)