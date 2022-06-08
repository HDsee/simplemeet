const userName = document.querySelector('#user-name')
const userEmail = document.querySelector('#user-email')

let nowEmail


//檢查有沒有登入
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






