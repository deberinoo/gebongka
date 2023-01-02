from flask import Flask, render_template

app = Flask(__name__)

# ----- routes -----

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about-us')
def about_us():
    return render_template('about-us.html')

@app.route('/apps')
def apps():
    return render_template('apps.html')


if __name__ == "__main__":
    app.run(debug=True)

# change 2 lol

# Hi im Gerald

# First branch 

# second branch ahahahhahahahf
