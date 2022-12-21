const signoutBtn = document.querySelector('#signout_btn')/*登出按鈕*/

//登出
function signout(){

    fetch(userApi, {
        method: 'DELETE'
    })
    .then(() => {
        // history.go(0)
        window.location.href='/'
    })

}
signoutBtn.addEventListener('click', signout)

// function userCheck(){

//     fetch(userApi)
//         .then(res => res.json())
//         .then(data => {
//             if(data.data){
//                 window.location.href='/chat'
//             }else{
//                 window.location.href='/'
//             }
//         })
// }
// userCheck()


