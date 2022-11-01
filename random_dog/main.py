from flask import Flask, render_template

app = Flask(__name__)

# app.secret_key = os.environ['flask_secret_key']

app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

@app.route('/')
def home():
  return render_template('index.html')

if __name__ == "__main__":
    # Replit server config
    # app.run(debug=True,host='0.0.0.0', port=81)

    # Local server config
    app.run(debug=True)