from flask import Flask, Blueprint, render_template, request
from flask_login import login_required, current_user
from flask_bcrypt import Bcrypt

from .models import SkinConditionHistory
from .models import NutritionAnalyserHistory

past_history = Blueprint("past_history", __name__)

app = Flask(__name__)
Bcrypt = Bcrypt(app)

@past_history.route('/profile')
@login_required
def profile():

    # get skin condition history 
    allskinconditionrows = SkinConditionHistory.query.filter_by(username=current_user.username).all()
    
    # get nutrition analyser history 
    allnutritionanalyserrows = NutritionAnalyserHistory.query.filter_by(username=current_user.username).all()

    return render_template("profile.html", SChistory = allskinconditionrows, NAhistory = allnutritionanalyserrows)

@past_history.route('/view-skin-history', methods = ['GET', 'POST'])
@login_required
def viewskinhistory():
    if request.method == 'POST':
        itemtopone = request.form.get("itemtopone")
        itemtoptwo = request.form.get("itemtoptwo")
        itemtopthree = request.form.get("itemtopthree")
        itemimgpath = request.form.get("itemimgpath")
        itemdate = request.form.get("itemdate")
        print(itemimgpath)
    return render_template("history-skin-condition.html", passtopone = itemtopone, passtoptwo = itemtoptwo, passtopthree = itemtopthree, passimgpath = itemimgpath, passdate = itemdate)