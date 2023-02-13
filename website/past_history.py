from flask import Blueprint, Flask, flash, render_template, request
from flask_bcrypt import Bcrypt
from flask_login import current_user, login_required

from .ml_models import burn, chatbot, food, retrieve_all_history, skin

past_history = Blueprint("past_history", __name__)

app = Flask(__name__)
Bcrypt = Bcrypt(app)

@past_history.route('/profile')
@login_required
def profile():
    allskinconditionrows, allburngraderows, allchatbotdiagnosisrows, allnutritionanalyserrows = retrieve_all_history(current_user.username)
    return render_template("profile.html", SChistory = allskinconditionrows, NAhistory = allnutritionanalyserrows, BGhistory = allburngraderows, CDhistory = allchatbotdiagnosisrows)

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
    return render_template("models/history-skin-condition.html", passtopone = itemtopone, passtoptwo = itemtoptwo, passtopthree = itemtopthree, passimgpath = itemimgpath, passdate = itemdate)

@past_history.route('/delete-skin-history', methods = ['GET', 'POST'])
def delete_skin_history():
    try:
        if request.method == 'POST':
            id = request.form.get("id")
            skin.delete_history(id)
            flash("Skin Condition identifier History record deleted successfully!", category="info")
            allskinconditionrows, allburngraderows, allchatbotdiagnosisrows, allnutritionanalyserrows = retrieve_all_history(current_user.username)
        return render_template("profile.html", SChistory = allskinconditionrows, NAhistory = allnutritionanalyserrows, BGhistory = allburngraderows, CDhistory = allchatbotdiagnosisrows)
    except Exception as e:
        print("error", e)
        flash("Whoops! There was a problem deleting the skin Condition Identifier history record. Please try again.", category="info")
        allskinconditionrows, allburngraderows, allchatbotdiagnosisrows, allnutritionanalyserrows = retrieve_all_history(current_user.username)
        return render_template("profile.html", SChistory = allskinconditionrows, NAhistory = allnutritionanalyserrows, BGhistory = allburngraderows, CDhistory = allchatbotdiagnosisrows)

@past_history.route('/view-burn-history', methods = ['GET', 'POST'])
@login_required
def viewburngradehistory():
    if request.method == 'POST':
        burnGradePred = request.form.get("burnGradePred")
        itemimgpath = request.form.get("itemimgpath")
        itemdate = request.form.get("itemdate")
        print("Burn image path: ",itemimgpath)
    return render_template("models/history-burn-grade.html",  passgrade = burnGradePred, passimgpath = itemimgpath, passdate = itemdate)

@past_history.route('/delete-grade-history', methods = ['GET', 'POST'])
def delete_burn_history():
    try:
        if request.method == 'POST':
            id = request.form.get("id")
            burn.delete_history(id)
            flash("Burn Grade History record deleted successfully!", category="info")
            allskinconditionrows, allburngraderows, allchatbotdiagnosisrows, allnutritionanalyserrows = retrieve_all_history(current_user.username)
        return render_template("profile.html", SChistory = allskinconditionrows, NAhistory = allnutritionanalyserrows, BGhistory = allburngraderows, CDhistory = allchatbotdiagnosisrows)
    except Exception as e:
        print("error", e)
        flash("Whoops! There was a problem deleting the Burn Grade history record. Please try again.", category="info")
        allskinconditionrows, allburngraderows, allchatbotdiagnosisrows, allnutritionanalyserrows = retrieve_all_history(current_user.username)
        return render_template("profile.html", SChistory = allskinconditionrows, NAhistory = allnutritionanalyserrows, BGhistory = allburngraderows, CDhistory = allchatbotdiagnosisrows)

@past_history.route('/delete-chatbot-history', methods = ['GET', 'POST'])
def delete_chatbot_history():
    try:
        if request.method == 'POST':
            id = request.form.get("id")
            chatbot.delete_history(id)
            flash("Chatbot Diagnosis History record deleted successfully!", category="info")
            allskinconditionrows, allburngraderows, allchatbotdiagnosisrows, allnutritionanalyserrows = retrieve_all_history(current_user.username)
        return render_template("profile.html", SChistory = allskinconditionrows, NAhistory = allnutritionanalyserrows, BGhistory = allburngraderows, CDhistory = allchatbotdiagnosisrows)
    except Exception as e:
        print("error", e)
        flash("Whoops! There was a problem deleting the chatbot diagnosis history record. Please try again.", category="info")
        allskinconditionrows, allburngraderows, allchatbotdiagnosisrows, allnutritionanalyserrows = retrieve_all_history(current_user.username)
        return render_template("profile.html", SChistory = allskinconditionrows, NAhistory = allnutritionanalyserrows, BGhistory = allburngraderows, CDhistory = allchatbotdiagnosisrows)

@past_history.route('/delete-nutrition-history', methods = ['GET', 'POST'])
def delete_nutrition_history():
    try:
        if request.method == 'POST':
            id = request.form.get("id")
            food.delete_history(id)
            flash("Nutrition Analysis History record deleted successfully!", category="info")
            allskinconditionrows, allburngraderows, allchatbotdiagnosisrows, allnutritionanalyserrows = retrieve_all_history(current_user.username)
        return render_template("profile.html", SChistory = allskinconditionrows, NAhistory = allnutritionanalyserrows, BGhistory = allburngraderows, CDhistory = allchatbotdiagnosisrows)
    except Exception as e:
        print("error", e)
        flash("Whoops! There was a problem deleting the nutrition analysis history record. Please try again.", category="info")
        allskinconditionrows, allburngraderows, allchatbotdiagnosisrows, allnutritionanalyserrows = retrieve_all_history(current_user.username)
        return render_template("profile.html", SChistory = allskinconditionrows, NAhistory = allnutritionanalyserrows, BGhistory = allburngraderows, CDhistory = allchatbotdiagnosisrows)