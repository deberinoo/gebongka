from website import create_app
from flask_socketio import SocketIO, send
from website.ml_models import chatbot
import time

app = create_app()
socketio = SocketIO(app, logger=True, engineio_logger=True, ping_timeout=5, ping_interval=5)

@socketio.on('message')
def handle_message(msg):
    print("Received message: " + msg)
    try:
        result = chatbot.predict_diagnosis(msg)[0]['entity_group']
        diagnosis = result.replace("_", " ").capitalize()
        result = "I have detected that you are experiencing: " + diagnosis
        description = chatbot.map_to_diagnosis(diagnosis)[0]
        causes = chatbot.map_to_diagnosis(diagnosis)[1]
        treatment = chatbot.map_to_diagnosis(diagnosis)[2]
        follow_up = "Any other symptoms?"

        send("You: " + msg, broadcast=True)
        time.sleep(3)
        send("Healthcare Chatbot: " + result, broadcast=True)
        send("Healthcare Chatbot: " + description, broadcast=True)
        send("Healthcare Chatbot: " + causes, broadcast=True)
        send("Healthcare Chatbot: " + treatment, broadcast=True)
        send("Healthcare Chatbot: " + follow_up, broadcast=True)
    except:
        result = "Healthcare Chatbot: Sorry, I didn't get that. Please try again."
        diagnosis = ""
        send(msg, broadcast=True)

if __name__ == '__main__':
    #app.run(debug=True,host='0.0.0.0',port=8888)
    socketio.run(app, debug=True)