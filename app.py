from flask import Flask, render_template

app = Flask(__name__)

# ----- general routes -----

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about-us')
def about_us():
    return render_template('about-us.html')

@app.route('/apps')
def apps():
    return render_template('apps.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/pages')
def pages():
    return render_template('pages.html')

# ----- authentication routes -----

@app.route('/sign-in')
def sign_in():
    return render_template('auth/sign-in.html')

@app.route('/sign-up')
def sign_up():
    return render_template('auth/sign-up.html')

@app.route('/reset-password')
def reset_password():
    return render_template('auth/reset-password.html')


if __name__ == "__main__":
    app.run(debug=True)

# change 2 lol

# Hi im Gerald

# First branch 

# second branch ahahahhahahahf
