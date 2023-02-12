from datetime import datetime

import keras.utils as image
from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model
from transformers import (AutoModelForTokenClassification, AutoTokenizer,
                          pipeline)


from . import db
from .models import NutritionAnalyserHistory, SkinConditionHistory, BurnGradeHistory, ChatbotDiagnosisHistory


def process_image(img_path):
    i = image.load_img(img_path, target_size=(128,128))
    i = image.img_to_array(i)
    i = i.reshape(1, 128,128,3)
    i = preprocess_input(i)
    return i

class skin:
    def Check_Highest_Prediction(prediction_array):
        print("Put into dic")
        predictecdic = skin.put_into_dic(prediction_array[0])

        top1 = list(dict(predictecdic).keys())[0]
        top2 = list(dict(predictecdic).keys())[1]
        top3 = list(dict(predictecdic).keys())[2]

        return top1,top2,top3
        
    def predict_label(img_path):
        classlist = ['Actinic Keratosis','basal cell carcinoma','dermatofibroma','melanoma','nevus','vascular lesion']
        model = load_model('website/model/Erika_Model.h5')

        print("Call make_prediction_function()")
        #model.make_predict_function()

        print("Image Path part 2: ", img_path)

        p = model.predict(process_image(img_path))
        print("Original Array: ", p)
        top1,top2,top3 = skin.Check_Highest_Prediction(p)
        print("top1: ", classlist[top1])
        print("top2: ", classlist[top2])
        print("top3: ", classlist[top3])
        return classlist[top1],classlist[top2],classlist[top3]

    def put_into_dic(prediction_array):
        mydict={}
        for index, i in enumerate(prediction_array):
            print(i)
            mydict[index]=f"{i}"
		
        sorteddic = sorted(mydict.items(), key=lambda x:x[1])
        ##print("DICT", mydict)
        print("DICTSORT", sorteddic)

        return sorteddic

    def create_history(img_path, top1, top2, top3,passuser):
        new_skinhistory = SkinConditionHistory(username=passuser, topone = top1, toptwo = top2, topthree = top3, imguploadpath = img_path, dateprediction = str(datetime.now()))
        db.session.add(new_skinhistory)
        db.session.commit()

class burn:
    def predict_label(img_path):
        model = load_model('website/model/BurnModel.h5')
        model.make_predict_function()

        pr = model.predict(process_image(img_path))
        predResult = burn.Return_Prediction(pr)

        print(pr)
        print("result", predResult)
        return predResult

    def Return_Prediction(pred_array):
        HighestValue = -100
        burnclass = ""
        index = 0
        
        for arrayValue in pred_array[0]: 
            print("THis is index ", index)
            print("THis is Value ", arrayValue)
            if arrayValue > HighestValue:
                HighestValue = arrayValue
                if index == 0:
                    burnclass = "This is First degree burn"
                elif index == 1:
                    burnclass = "This is Second degree burn"  
                else:
                    burnclass = "This is Third degree burn"
            index+=1
        return burnclass

    def create_burn_history(img_path,PredResult,passuser):
        new_burnhistory = BurnGradeHistory(username=passuser, burnGradePred = PredResult, imguploadpath = img_path, dateprediction = str(datetime.now()))
        db.session.add(new_burnhistory)
        db.session.commit()

class chatbot:
    def load_classifier():
        label_names = ['B-COUGH', 'I-COUGH', 'B-BREATHLESSNESS', 'I-BREATHLESSNESS', 'B-DIZZINESS', 'I-DIZZINESS', 'B-HEADACHE', 'I-HEADACHE', 'B-CHILLS', 'I-CHILLS', 'B-CHEST_PAIN', 'I-CHEST_PAIN', 'B-BACK_PAIN', 'I-BACK_PAIN', 'B-MUSCLE_PAIN', 'I-MUSCLE_PAIN', 'B-JOINT_PAIN', 'I-JOINT_PAIN', 'B-NECK_PAIN', 'I-NECK_PAIN', 'B-STOMACH_PAIN', 'I-STOMACH_PAIN', 'O']
        id2label = { i: label for i, label in enumerate(label_names) }
        label2id = {v: k for k, v in id2label.items()}

        model = AutoModelForTokenClassification.from_pretrained(
            "website/chatbot",
            num_labels=23,
            id2label=id2label,
            label2id=label2id,
            ignore_mismatched_sizes=True
        )
        tokenizer = AutoTokenizer.from_pretrained("samrawal/bert-base-uncased_clinical-ner")

        # instantiates a pipeline, which uses the model for inference

        token_classifier = pipeline(
            "token-classification", model=model, 
            tokenizer=tokenizer,
            aggregation_strategy="first",
            device=-1
        )
        
        return token_classifier
    
    def predict_diagnosis(text):
        token_classifier = chatbot.load_classifier()
        return token_classifier(text)
    
    def map_to_diagnosis(diagnosis):
        diagnosis_dict = {
            "Cough": ["While an occasional cough is normal, a cough that persists may be a sign of a medical problem.",
                      "Common causes of coughs include: Common cold, Influenza, Inhaling an irritant (such as smoke, dust, chemicals or a foreign body)",
                      "To treat a cough, you can drink lots of fluids, swallow some honey, or consider over the counter options."],
            "Breathlessness": ["Breathlessness — known medically as dyspnea — is often described as an intense tightening in the chest, air hunger, difficulty breathing, breathlessness or a feeling of suffocation.",
                               "Possible causes of breathlessness include: Asthma, carbon monoxide poisoning, heart attack, low blood pressure, or an allergic reaction.",
                               "To relieve shortness of breath, practicing pursed lip breathing, sitting forward, or pointing a small handheld fan toward your face may help."],
            "Dizziness": ["Dizziness is a term used to describe a range of sensations, such as feeling faint, woozy, weak or unsteady. Dizziness that creates the false sense that you or your surroundings are spinning or moving is called vertigo.",
                          "Dizziness has many possible causes, including inner ear disturbance, motion sickness and medication effects. Sometimes it's caused by an underlying health condition, such as poor circulation, infection or injury.",
                          "When you feel dizzy, sit or lie down immediately. Drink enough fluids, eat a healthy diet, get enough sleep and avoid stress."],
            "Headache": ["A headache is a pain that occurs in the temples, scalp or neck.",
                         "Headaches can manifest as a symptom of another health disorder, such as an infection, medication overuse, high blood pressure, and stroke.",
                         "Most headaches are easily treated with over-the-counter medications, including: Aspirin, Ibuprofen, and Acetaminophen. You can also rest in a quiet, dark room and try hot or cold compresses to your head and neck."],
            "Chills": ["Chills are a sign that your body is trying to regulate its core temperature. You may shiver, shake, have chattering teeth or goosebumps.",
                       "Health conditions such as bacterial infections, cancers, low blood sugar, panic attacks may cause chills."
                       "Layering clothes or getting to a warm place can make cold chills go away. You can also drink hot beverages to raise your internal body temperature."],
            "Chest pain": ["Chest pain appears in many forms, ranging from a sharp stab to a dull ache. Sometimes chest pain feels crushing or burning. In certain cases, the pain travels up the neck, into the jaw, and then spreads to the back or down one or both arms.",
                           "Chest pain can stem from a heart problem, but other possible causes include a lung infection, muscle strain, a rib injury, or a panic attack. Some of these are serious conditions and need medical attention.",
                           "Drugs used to treat some of the most common causes of chest pain include: Artery relaxers, Aspirin, and blood thinners."],
            "Back pain": ["Back pain can range from a muscle aching to a shooting, burning or stabbing sensation. Also, the pain can radiate down a leg. Bending, twisting, lifting, standing or walking can make it worse.", 
                          "Conditions commonly linked to back pain include: Muscle or ligament strain, Bulging or ruptured disks, arthritis, and osteoporosis.",
                          "Continue your activities as much as you can with back pain. Try light activity, such as walking. Stop activity that increases pain, but don't avoid activity out of fear of pain. If home treatments aren't working after several weeks, your health care provider might recommend stronger medications or other therapies."
                          ],
            "Muscle pain": ["Muscle aches, also known as myalgia, can be felt in any area of the body that has muscles. Depending on the cause, the discomfort may be mild or extremely severe.",
                            "Common causes of muscle pain include: muscle tension in one or more areas of the body, overusing the muscle during physical activity. Medical conditions such as fibromyalgia, infections and autoimmune disorders can also cause muscle pain.",
                            "Some measures you can take to relieve muscle discomfort from injuries and overuse include: resting the area of the body where you're experiencing aches and pains, taking an over-the-counter pain reliever such as ibuprofen, and applying ice to the affected area."],
            "Joint pain": ["Joint discomfort is common and usually felt in the hands, feet, hips, knees, or spine. Pain may be constant or it can come and go. Sometimes the joint can feel stiff, achy, or sore.",
                           "The most common causes of chronic pain in joints are: osteoarthritis, gout, viral infections and tendinitis.",
                           "To ease joint pain, you can try simple at-home treatments such as applying a heating pad or ice on the affected area, or light exercise such as walking and swimming."],
            "Neck pain": ["Neck pain, sometimes called cervicalgia, is pain in or around your spine beneath your head. Your neck is also known as your cervical spine. Neck pain is a common symptom of many different injuries and medical conditions.",
                          "Neck pain has many potential causes, including: Injury, like whiplash, physical strain, aging, and mental stress.",
                          "Neck pain can be managed by taking pain medications and muscle relaxers, taking a hot shower or placing a hot towel on the site of the pain."],
            "Stomach pain": ["Stomach pain is discomfort or other uncomfortable sensations that you feel in your belly area.",
                             "Causes of stomach pain include: irritable bowel syndrome (IBS), food poisoning, food allergies, or gas.",
                             "You can treat your stomach pain by resting your bowel, only eating easy-to-digest foods like crackers or bananas. In addition, drink plenty of water to stay hydrated."],
        }
        return diagnosis_dict[diagnosis]
    
    def create_history(username, symptoms):
        chatbot_history = ChatbotDiagnosisHistory(username=username, symptoms=symptoms)
        db.session.add(chatbot_history)
        db.session.commit()

class food:
    def predict_label(img_path):
        classlist = ['Chicken Wings','Fish and Chips','French Fries','French Toast','Garlic Bread','Macaroni and Cheese','Pizza','Pork Chop','Spaghetti Carbonara','Steak']

        model = load_model('website/model/Food_Model.h5')
        print("Call make_prediction_function()")
        #model.make_predict_function()

        p = model.predict(process_image(img_path))
        print("Original Array: ", p)
        return classlist[p]

    def create_history(img_path, food_name, passuser):
        new_foodhistory = NutritionAnalyserHistory(username=passuser, food_name = food_name, imguploadpath = img_path, dateprediction = str(datetime.now()))
        db.session.add(new_foodhistory)
        db.session.commit()