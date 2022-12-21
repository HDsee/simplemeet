const signBtn = document.querySelector('#sign_btn')/*註冊登入按鈕*/
const signWindow = document.querySelector('.sign_window')/*註冊登入視窗*/
const signContainer = document.querySelectorAll('.sign_container')/*註冊登入內容*/
const changeSignBtn = document.querySelectorAll('.change_sign')/*切換註冊登入視窗按鈕*/

//切換註冊登入視窗
function changeSignWindow(){
    signContainer.forEach(container=>{
        container.classList.toggle('show')
    })
}

changeSignBtn.forEach(change => {
    change.addEventListener('click',changeSignWindow)
})

//註冊登入
const signinForm = document.querySelector('#signin')
const signupForm = document.querySelector('#signup')
const userApi = '/api/user'

//註冊功能
function signup(e){
    e.preventDefault()

    const data = {
        name : this.querySelector('input[name="name"]').value,
        email : this.querySelector('input[name="email"]').value,
        password : this.querySelector('input[name="password"]').value,
        img : "https://d2xfotk02kb3rl.cloudfront.net/coffee.jpg" 
    }
    fetch(userApi, {
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
            message.innerText = '註冊成功'
        }else{
            message.innerText = data.message
        }
    })
}


//登入功能
function signin(e){
    e.preventDefault()
    const data = {
        email : this.querySelector('input[name="email"]').value,
        password : this.querySelector('input[name="password"]').value 
    }
    fetch(userApi, {
        method: 'PATCH',
        body: JSON.stringify(data),
        headers: new Headers({
          'Content-Type': 'application/json'
        })
    })
    .then(res => res.json())
    .then(data => {
        //登入成功進入聊天頁面
        if(data.ok === true){
            userCheck()
        }else{
            const message = this.querySelector('.message')
            message.innerText = data.message
        }
    })
}

signupForm.addEventListener('submit', signup)
signinForm.addEventListener('submit', signin)

const testEmail = document.querySelector('#testemail')/*測試帳號*/
const testPassword = document.querySelector('#testpassword')/*測試密碼*/

//檢查有沒有登入
function userCheck(){

    fetch(userApi)
        .then(res => res.json())
        .then(data => {
            if(data.data){
                window.location.href='/chat';
            }
            else{ 
                testEmail.value = '123@outlook.com' /*寫入測試帳號*/
                testPassword.value = '123'
            }
        })
}
userCheck()





