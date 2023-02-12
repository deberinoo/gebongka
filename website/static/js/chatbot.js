$(document).ready(function() {
    var socket = io.connect()
    socket.on('connect', function() {
        renderMessage("other", {"text":"Hello, what symptoms are you experiencing today?"})
    });

    socket.on('message', function(type, msg) {
        if ( msg != undefined) {
            renderMessage("my", msg)
        }
    });

    socket.on('chat', function(msg) {
        renderMessage("other", {"text":msg.text})
    });

    function renderMessage(type, msg) {
        let messageContainer = document.querySelector(".container")
        if (type == "other") {
            let el = document.createElement("div");
            el.setAttribute("class", "chat-people");
            el.innerHTML = `
                <div class="chat-item text-small">
                    <div class="chat-date"><span>Healthcare Chatbot</span></div>
                    <div class="chat-text">
                        <p>${msg.text}</p>
                    </div>
                    <div class="triangle angle-left"></div>
                </div>

                <div class="separator-small"></div>
            `;
            messageContainer.appendChild(el);
            console.log('Received message' + msg.text);
        }
        // else
        else if (type == "my") {
            let el = document.createElement("div");
            el.setAttribute("class", "my-chat");
            el.innerHTML = `
                <div class="chat-item text-small bg-my-chat">
                    <div class="chat-date"><span>You</span></div>
                    <div class="chat-text">
                        <p>${msg}</p>
                    </div>
                    <div class="triangle angle-right"></div>
                </div>

                <div class="separator-small"></div>
            `;
            messageContainer.appendChild(el);
            console.log('Received message' + msg);
        }
        messageContainer.scrollTop = messageContainer.scrollHeight - messageContainer.clientHeight;
    }

    $('#sendBtn').on('click', function () {
        socket.send($('#myMessage').val());
        renderMessage("my", $('#myMessage').val());
        $('#myMessage').val('');
        console.log('Sent message' + $('#myMessage').val());
    });
})