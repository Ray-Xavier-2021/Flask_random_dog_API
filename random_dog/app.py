from flask import Flask, render_template, request, session
import requests

from database import db

from secret import sk

app = Flask(__name__)

# app.secret_key = os.environ['flask_secret_key']
app.secret_key = sk['secret_key']

# app.config['SESSION_COOKIE_SAMESITE'] = 'None'
# app.config['SESSION_COOKIE_SECURE'] = True


@app.route('/', methods=['POST', 'GET'])
def home():
  if request.method == 'POST':
    print("You clicked the Login Button!")
    user_name = request.form['user_name']
    session['user'] = user_name
    user = create_or_update_user(user_name)

  else:
    user = None

  return render_template('index.html',
  dogs_generated=db['total_dogs_generated'],
  dog_image=db['last_dog'],
  user=user)


@app.route('/get_dog')
def get_dog():
  response = requests.get('https://dog.ceo/api/breeds/image/random')
  data = response.json() 
  dog_image = data['message']
  db['last_dog'] = dog_image

  if session['user']:
    user = get_user_from_database(session['user'])
    db['total_dogs_generated'] += 1
    user['dogs_generated'] += 1

  return render_template('index.html',
   dog_image=dog_image,
   dogs_generated=db['total_dogs_generated'],
   user=user)


@app.route('/logout')
def logout():
  session['user'] = None

  return render_template('index.html',
  dogs_generated=db['total_dogs_generated'])


def create_or_update_user(user_name):
  user = get_user_from_database(user_name)
  user = user[0] if user else None

  if user:
    print('USER ALREADY EXIST!')
    user['logins'] += 1
    print(user)

  else:
    print('NEW USER!')
    db['users'].append({
      'user_name': user_name,
      'logins': 1,
      'dogs_generated': 0
    })
    user = get_user_from_database(user_name)

  return user
  
  
def get_user_from_database(user_name):
  user = [user for user in db['users'] if user['user_name'] == user_name]
  return user[0] if user else None


if __name__ == "__main__":
  app.run(debug=True)