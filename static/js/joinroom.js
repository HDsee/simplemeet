
const joinRoomForm = document.querySelector('#joinroom')
const joinroomApi = '/api/joinroom'

//進入房間
function joinroom(e){
    e.preventDefault()
    fetch(userApi)
        .then(res => res.json())
        .then(data => {
            // 有登入
            if(data.data !== null){
                window.location.href='/chat';
            }else{  // 沒登入
                window.location.href='/';
            }
        })
}

joinRoomForm.addEventListener('submit', joinroom)



