from website import create_app
from flask_socketio import SocketIO, send
from website.ml_models import chatbot
import time
import requests

app = create_app()
socketio = SocketIO(app, logger=True, engineio_logger=True, ping_timeout=5, ping_interval=5)

@socketio.on('message')
def handle_message(msg):
    print("Received message: " + msg)
    # try:
    if msg != "User connected!" and msg != "Healthcare Chatbot: Hello, what symptoms are you experiencing today?":
        result = requests.post("http://127.0.0.1:8000/chatbot-diagnosis-model", json={"data":msg})
        docker_result = result.json()['response']
        print(docker_result)

        diagnosis = docker_result.replace("_", " ").capitalize()
        result = "I have detected that you are experiencing: " + diagnosis
        description = chatbot.map_to_diagnosis(diagnosis)[0]
        causes = chatbot.map_to_diagnosis(diagnosis)[1]
        treatment = chatbot.map_to_diagnosis(diagnosis)[2]
        follow_up = "Any other symptoms?"

        send("You: " + msg, broadcast=True)
        time.sleep(3)
        send("Healthcare Chatbot: " + result, broadcast=True)
        send(description, broadcast=True)
        send(causes, broadcast=True)
        send(treatment, broadcast=True)
        send(follow_up, broadcast=True)
    else:
        send(msg, broadcast=True)
    # except:
    #     print("error")
    #     result = "Healthcare Chatbot: Sorry, I didn't get that. Please try again."
    #     send(result, broadcast=True)

if __name__ == '__main__':
    #app.run(debug=True,host='0.0.0.0',port=8888)
    socketio.run(app, debug=True, host='0.0.0.0', port=8888)