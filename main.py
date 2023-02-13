from flask_socketio import SocketIO

from website import create_app
from website.views import handle_message, reply

app = create_app()
socketio = SocketIO(app, logger=True, engineio_logger=True, ping_timeout=5, ping_interval=5)

# Deborah's Part =====================================================
# socket.io for chatbot feature

@socketio.on('message')
def chatbot_diagnosis(msg):
    handle_message(msg)

@socketio.on('chat')
def chat(msg):
    reply(msg)

if __name__ == '__main__':
    # app.run(debug=True,host='0.0.0.0',port=8888)
    socketio.run(app, debug=True, host='0.0.0.0', port=8888)
