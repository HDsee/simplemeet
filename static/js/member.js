const userName = document.querySelector('#user-name')
const userEmail = document.querySelector('#user-email')

let nowEmail


//會員資料查詢
function memberGet(){
    fetch(userApi)
        .then(res => res.json())
        .then(data => {
            if(data.data != null ){
                userName.innerText = `Member Name：${data.data.user}`
                userEmail.innerText = `Member Email：${data.data.email}`
                nowEmail = data.data.email
            }
            else{
                window.location.href='/'
            }
        })
}

memberGet()


const memberForm = document.querySelector('#member-data')
const memberApi = '/api/member'
const friendApi = '/api/friend'


//會員資料修改
function memberupdate(e){
    e.preventDefault()

    const data = {
        email : nowEmail,
        name : this.querySelector('input[name="name"]').value,
        password : this.querySelector('input[name="password"]').value,
    }
    fetch(memberApi, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: new Headers({
        'Content-Type': 'application/json'
        })
    })
    .then(res => res.json())
    .then(data => {
        const message = this.querySelector('.message')
        if(data.ok){
            alert('修改成功')
            message.innerText = '修改成功'
            history.go(0)
        }else{
            message.innerText = data.message
        }
    })
}


memberForm.addEventListener('submit', memberupdate)


const friendSearchForm = document.querySelector('#firend-search')
const friendNameText = document.querySelector('#friend-name')

let friendName 
let friendEmail
//好友資料查詢
function friendSearch(e){
    e.preventDefault()

    const data = {
        email : this.querySelector('input[name="search"]').value,
    }
    fetch(memberApi, {
        method: 'PATCH',
        body: JSON.stringify(data),
        headers: new Headers({
        'Content-Type': 'application/json'
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data)
        if(data.user ){
            friendNameText.innerText = data.user
            friendName = data.user
            friendEmail = data.email
        }
        else{
            console.log(data)
            friendNameText.innerText = data.message
        }
    })
}

friendSearchForm.addEventListener('submit', friendSearch)

const joinFriendBtn = document.querySelector('#join-friend-button')
const joinFriendMes = document.querySelector('#join-friend-message')
//好友資料增加
function joinfriend(e){
    e.preventDefault()
    const data = {
        email : friendEmail,
        name : friendName
    }
    console.log(data)
    fetch(friendApi, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: new Headers({
        'Content-Type': 'application/json'
        })
    })
    .then(res => res.json())
    .then(data => {
        const message = this.querySelector('.message')
        if(data.ok){
            joinFriendMes.innerText = '好友添加成功'
        }else{
            joinFriendMes.innerText = data.message
        }
    })
}


joinFriendBtn.addEventListener('click', joinfriend)