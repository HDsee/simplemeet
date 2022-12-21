const socket = io.connect("http://127.0.0.1:3020");
// const socket = io.connect("https://52.68.132.15:3020");
// const socket = io.connect("https://hd.simplemeet.website");
const privateSocket = io.connect("http://127.0.0.1:3020/private");

const userApi = '/api/user'
const joinroomApi = '/api/joinroom'
const messageApi = '/api/message'
let username
let useremail
let userimg 
let room


function userGet(){
    fetch(userApi)
        .then(res => res.json())
        .then(data => {
            if(data.data != null ){
                username = data.data.user,
                useremail = data.data.email,
                userimg = data.data.img
            }
            else{
                window.location.href='/'
            }
        })
}
userGet()

socket.on('connect', function() {
    privateSocket.emit('username',username)
});

//發送訊息
const messageInput = document.querySelector('#message_input');
const messageForm = document.querySelector('#message_input_form');
const messageContent = document.querySelector('#messages');
const today = new Date();
const month =  today.getMonth() + 1
const day =  ('0' + today.getDate()).slice(-2);
const hour =  ('0' + today.getHours()).slice(-2);
const minute = ('0' + today.getMinutes()).slice(-2);
const second = ('0' + today.getSeconds()).slice(-2);
const time =  today.getHours() + ':' +  minute + ':' + second;

function message_send (e){
    e.preventDefault()
    const mes=messageInput.value.trim()
    const message = ({username,mes,time});
    if (message) {
        //發送即時訊息
        privateSocket.emit('private_message',{'username': targetFriend,'message':message});
        //視窗加入即時訊息
        const sendContainer = document.createElement('div');
        sendContainer.classList.add('mes_user');
        sendContainer.classList.add('sender');

        const senderContent = document.createElement('div');
        senderContent.classList.add('mes_content');
        const senderImgContent = document.createElement('div');
        senderImgContent.classList.add('mes_img_content');
        const senderImg = document.createElement('img');
        senderImg.src=userimg
        const senderName = document.createElement('div');
        senderName.classList.add('mes_name');
        senderName.innerHTML = `${username}`;

        const senderMes = document.createElement('div');
        senderMes.classList.add('mes_text');
        const senderTime = document.createElement('div');
        senderTime.classList.add('mes_time');
        senderTime.classList.add('sender');
        senderMes.innerHTML = `${mes}`;
        senderTime.innerHTML = `${time}`;

        senderImgContent.appendChild(senderImg);
        senderContent.appendChild(senderImgContent);
        senderContent.appendChild(senderName);
        sendContainer.appendChild(senderContent);
        sendContainer.appendChild(senderMes);
        sendContainer.appendChild(senderTime);
        messageContent.appendChild(sendContainer);
    }
}
messageForm.addEventListener('submit', message_send)

//儲存訊息
function message_store (e){
    e.preventDefault()
    const data = {
        sender : username,
        receiver : targetFriend,
        message : messageInput.value.trim(),
    }
    fetch(messageApi, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: new Headers({
        'Content-Type': 'application/json'
        })
    })
    messageInput.value = '';
}
messageForm.addEventListener('submit', message_store)

//接收即時訊息
privateSocket.on('new_private_message', function(msg){
    const receiveContainer = document.createElement('div');
    receiveContainer.classList.add('mes_user');
    receiveContainer.classList.add('receiver');

    const receiverContent = document.createElement('div');
    receiverContent.classList.add('mes_content');
    const receiverImgContent = document.createElement('div');
    receiverImgContent.classList.add('mes_img_content');
    const receiverImg = document.createElement('img');
    receiverImg.src=targetFriendImg
    const receiverName = document.createElement('div');
    receiverName.classList.add('mes_name');
    receiverName.innerHTML = `${msg.username}`;

    const receiverMes = document.createElement('div');
    receiverMes.classList.add('mes_text');
    const receiverTime = document.createElement('div');
    receiverTime.classList.add('mes_time');
    receiverMes.innerHTML = `${msg.mes}`;
    receiverTime.innerHTML = `${time}`;

    receiverImgContent.appendChild(receiverImg);
    receiverContent.appendChild(receiverImgContent);
    receiverContent.appendChild(receiverName);
    receiveContainer.appendChild(receiverContent);
    receiveContainer.appendChild(receiverMes);
    receiveContainer.appendChild(receiverTime);
    messageContent.appendChild(receiveContainer);
})

//emoji
const emoji = document.querySelector('.emoji');
const picker = new EmojiButton({
    position: 'bottom-end'
});

picker.on('emoji', selection => {
    messageInput.value += selection;
});
emoji.addEventListener('click', () => picker.togglePicker(emoji));


// socket.on('connect', function() {
//     socket.emit('join_room', {
//         username: username,
//         room: room
//     })

//     let message_input = document.getElementById('message_input');
//     document.getElementById('message_input_form').onsubmit = function (e) {
//     e.preventDefault();
//     let message = message_input.value.trim();
//     if (message.length) {
//         socket.emit('send_message', {
//             username: username,
//             room: room,
//             message: message
//         })
//     }
//     message_input.value = '';
//     message_input.focus();
//     }
// });

