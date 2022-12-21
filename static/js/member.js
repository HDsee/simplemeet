const memberName =  document.querySelector('#member_name')
const memberEmail = document.querySelector('#member_email')
const memberImg = document.querySelector('.member_img')
let nowEmail


//會員資料查詢
function memberGet(){
    fetch(userApi)
        .then(res => res.json())
        .then(data => {
            if(data.data != null ){
                memberName.innerText = `Member Name：${data.data.user}`
                memberEmail.innerText = `Member Email：${data.data.email}`
                memberImg.src = `${data.data.img}`
                nowEmail = data.data.email
            }
            else{
                window.location.href='/'
            }
        })
}
 
memberGet()


const memberForm = document.querySelector('#member_data')


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
const imgApi = '/api/img'

//更換大頭貼
const memberImgChangeBtn = document.querySelector('#member_img_change_btn');
const file = document.getElementById('select_file');

let imgData = new FormData();
let image = "";
file.addEventListener('change', (e) => {
    image = e.target.files[0];
});   

function memberImgChange(e){

    if(image !== ""){
        console.log(image);
        imgData.append('file', image);
        
        fetch(imgApi, {
            method: 'POST',
            body: imgData,
        })
        .then(res => res.json())
        .then(data => {
            if(data.ok){
                alert('修改成功')
                history.go(0)
            }else{
                alert('修改失敗')
            }
        })
    }else{
        alert("請選擇圖片");
    }
}

memberImgChangeBtn.addEventListener('click', memberImgChange)