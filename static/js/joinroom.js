
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
                const data = {
                    room : this.querySelector('input[name="room"]').value,
                }
                fetch(joinroomApi, {
                    method: 'PATCH',
                    body: JSON.stringify(data),
                    headers: new Headers({
                      'Content-Type': 'application/json'
                    })
                })
                .then(res => res.json())
                .then(data => {
                    if(data.ok){
                        window.location.href='/chat';
                    }else{
                        window.location.href='/';
                    }
                })
            }else{  // 沒登入
                showSignWindow()
            }
        })
}

joinRoomForm.addEventListener('submit', joinroom)


