const socket = io.connect("http://127.0.0.1:3020");
// const socket = io.connect("https://52.68.132.15:3020");
// const socket = io.connect("https://hd.simplemeet.website");


const userApi = '/api/user'
const joinroomApi = '/api/joinroom'
let username 
let room


function userGet(){
    fetch(userApi)
        .then(res => res.json())
        .then(data => {
            if(data.data != null ){
                username = data.data.user
                console.log(username)
            }
            else{
                window.location.href='/'
            }
        })
}
userGet()

const roomId = document.querySelector('#room_id')

function roomGet(){
    fetch(joinroomApi)
        .then(res => res.json())
        .then(data => {
            if(data.data != null ){
                room = data.data.room
                roomId.innerText = room
                console.log(room)
            }
            else{
                window.location.href='/'
            }
        })
}
roomGet()

socket.on('connect', function() {
    socket.emit('join_room', {
        username: username,
        room: room
    })

    let message_input = document.getElementById('message_input');
    document.getElementById('message_input_form').onsubmit = function (e) {
    e.preventDefault();
    let message = message_input.value.trim();
    if (message.length) {
        socket.emit('send_message', {
            username: username,
            room: room,
            message: message
        })
    }
    message_input.value = '';
    message_input.focus();
    }
});


socket.on('receive_message', function(data){
    console.log(data);
    const newNode = document.createElement('div');
    newNode.innerHTML = `<b>${data.username}:&nbsp;</b>${data.message}`;
    document.getElementById('messages').appendChild(newNode);
})

socket.on('join_room_announcement', function(data){
    console.log(data);
    const newNode = document.createElement('div');
    newNode.innerHTML = `<b>${data.username}</b> has joined the room`;
    document.getElementById('messages').appendChild(newNode);
})

const leaveBtn = document.querySelector('#leave_button')

function leave(e) {
    e.preventDefault()
    socket.emit('leave_room', {
        username: username,
        room: room
    })
    fetch(joinroomApi, {
        method: 'DELETE'
    })
    .then(() => {
        window.location.href='/';
    })
}

socket.on('leave_room_announcement', function(data){
    console.log(data);
    const newNode = document.createElement('div');
    newNode.innerHTML = `<b>${data.username}</b> has left the room`;
    document.getElementById('messages').appendChild(newNode);
})

leaveBtn.addEventListener('click', leave)


window.addEventListener('beforeunload', leave);

// window.onbeforeunload = function () {
//     socket.emit('leave_room', {
//         username: "username",
//         room: "room"
//     })
// };


// const videoBtn = document.getElementById('video');
// function videoPage(e){
//     e.preventDefault()
//     window.location.href='/video';
// }

// videoBtn.addEventListener('click', videoPage)