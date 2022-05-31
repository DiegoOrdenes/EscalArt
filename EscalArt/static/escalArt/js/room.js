const chatLog = document.querySelector('#chat-log')
const roomName = JSON.parse(document.getElementById('room-name').textContent);


if (chatLog.hasChildNodes() <= 1) {
    const emptyText = document.createElement('h3')
    emptyText.id = 'emptyText'
    emptyText.innerText = 'Este es el inicio de su conversacion, di algo!'
    emptyText.className = 'emptyText'
    chatLog.appendChild(emptyText)
}

const chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/' +
    roomName +
    '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const divMensaje = document.createElement('div')
    divMensaje.className = 'mensaje'
    const messageElement = document.createElement('div')
        // messageElement.innerText = data.message
    messageElement.className = 'cuerpo'
    const message = document.createElement('div')
    message.className = 'texto'
    message.innerText = data.message
    messageElement.appendChild(message)
    divMensaje.appendChild(messageElement)
    chatLog.appendChild(divMensaje)

    if (document.querySelector('#emptyText')) {
        document.querySelector('#emptyText').remove()
    }
    // document.querySelector('#chat-log').value += (data.message + '\n');
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) { // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};