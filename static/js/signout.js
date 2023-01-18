const signoutBtn = document.querySelector('#signout_btn')/*登出按鈕*/

//登出
function signout(){

    fetch(userApi, {
        method: 'DELETE'
    })
    .then(() => {
        window.location.href='/'
    })

}
signoutBtn.addEventListener('click', signout)



