const chatbox = document.querySelector(".content");
const socket = io();
const room = document.getElementById("room").value;

socket.emit('join', {message:"has joined the chat", room:room})

socket.on('chat', function(msg) {
    var receitor = document.getElementById("receitor"); 
    var li = document.createElement('li');
    li.innerHTML=msg;
    chatbox.scrollTop = chatbox.scrollHeight;
    receitor.appendChild(li);
});

function sendmessage() {
    var msg = document.getElementById("message");
    socket.emit('chat', {message:msg.value, room:room});
    msg.value = "";
}

function pulse(e) {
    if (e.keyCode === 13 && !e.shiftKey) {
        e.preventDefault();
        sendmessage();
    }
}