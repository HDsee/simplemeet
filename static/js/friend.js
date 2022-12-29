
const memberApi = '/api/member'
const friendApi = '/api/friend'

const friendSearchForm = document.querySelector('#firend_search')
const friendNameText = document.querySelector('#friend_name')
const joinImg = document.querySelector('#join_img')
let friendName 
let friendEmail
let friendImg
//好友資料查詢
function friendSearch(e){
    e.preventDefault()
    joinFriendMes.innerText = ''
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
            friendImg = data.img
            joinFriendBtn.classList.add('show')
        }
        else{
            console.log(data)
            friendNameText.innerText = data.message
        }
    })
}

friendSearchForm.addEventListener('submit', friendSearch)

const joinFriendBtn = document.querySelector('#join_friend_button')
const joinFriendMes = document.querySelector('#join_friend_message')

//好友資料增加
function joinfriend(e){
    e.preventDefault()
    const data = {
        email : friendEmail,
        name : friendName,
        img : friendImg
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

const SectionOptionUser = document.querySelector('.section_option_user')
const SectionOptionChat = document.querySelector('.section_option_chat')
const SectionOptionJoin = document.querySelector('.section_option_join')
const Background = document.querySelector('.background')


const sectionContentFriendSearch = document.querySelector('.section_content_friend_search')
const sectionContentFriendListContainer = document.querySelector('.section_content_friend_list_container')

const SectionMessage = document.querySelector('.section_message')
const FormMemberdata = document.querySelector('.form_memberdata')

const FriendListUser = document.querySelector('.friend_list_user')
const FriendListFriendname = document.querySelector('.friend_list_friendname')
const UserName = document.querySelector('.user_name')
const UserImg = document.querySelector('.user_img')
let targetFriend
let targetFriendImg

//好友資料取得
function getfriend(){
    sectionContentFriendSearch.classList.remove('show')
    sectionContentFriendListContainer.classList.add('show')
    fetch(friendApi) 
        .then(res => res.json())
        .then(data => {
            UserImg.src=userimg
            UserName.innerText = username
            console.log(data)
            if (data) {
                FriendListFriendname.innerHTML = ''
                const friends = data.data.frined
                for (const friend of friends) {
                    const FriendnameContent = document.createElement('div')
                    FriendnameContent.classList.add('friendname_content')
                    const FriendImage = document.createElement('img');
                    FriendImage.src=friend[1]
                    FriendImage.classList.add('friend_img')
                    const FriendName = document.createElement('p')
                    FriendName.innerText = friend[0]
                    FriendName.classList.add('friend_name')

                    FriendnameContent.append(FriendImage, FriendName)
                    FriendListFriendname.append(FriendnameContent)
                }
                
            }
        })
        .then(() => {
            const FriendNameAll = document.querySelectorAll('.friend_name')

            //歷史訊息取得
            function getfriendname(){
                targetFriend = this.innerText
                SectionMessage.classList.add('show')
                Background.classList.remove('show')
                FormMemberdata.classList.remove('show')
                messageContent.innerHTML = ''
                const historyData = {
                    sender : username,
                    receiver : targetFriend
                }
                fetch(messageApi, {
                    method: 'PATCH',
                    body: JSON.stringify(historyData),
                    headers: new Headers({
                    'Content-Type': 'application/json'
                    })
                })
                .then(res => res.json())
                .then(data => {
                    targetFriendImg = data.img
                    if(data.data){
                        data.data.forEach( data => meshistory(data[0],data[1],data[2], data[3]) )
                    }
                    else{
                        console.log('None message')
                    }
                })
            }

            FriendNameAll.forEach(get => {
                get.addEventListener('click',getfriendname)
            })

        })
}

//歷史訊息顯示
function meshistory(historySneder, historyReceiver,historyMessage,historyTime){ 
    const time = historyTime.slice(-6,-4) + ':' +  historyTime.slice(-4,-2) + ':' + historyTime.slice(-2);
    if(historySneder == username){
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
        senderName.innerHTML = `${historySneder}`;

        const senderMes = document.createElement('div');
        senderMes.classList.add('mes_text');
        const senderTime = document.createElement('div');
        senderTime.classList.add('mes_time');
        senderTime.classList.add('sender');
        senderMes.innerHTML = `${historyMessage}`;
        senderTime.innerHTML = `${time}`;

        senderImgContent.appendChild(senderImg);
        senderContent.appendChild(senderImgContent);
        senderContent.appendChild(senderName);
        sendContainer.appendChild(senderContent);
        sendContainer.appendChild(senderMes);
        sendContainer.appendChild(senderTime);
        messageContent.appendChild(sendContainer);

    }
    else{
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
        receiverName.innerHTML = `${historyReceiver}`;

        const receiverMes = document.createElement('div');
        receiverMes.classList.add('mes_text');
        const receiverTime = document.createElement('div');
        receiverTime.classList.add('mes_time');
        receiverMes.innerHTML = `${historyMessage}`;
        receiverTime.innerHTML = `${time}`;

        receiverImgContent.appendChild(receiverImg);
        receiverContent.appendChild(receiverImgContent);
        receiverContent.appendChild(receiverName);
        receiveContainer.appendChild(receiverContent);
        receiveContainer.appendChild(receiverMes);
        receiveContainer.appendChild(receiverTime);
        messageContent.appendChild(receiveContainer);
    }
}
SectionOptionChat.addEventListener('click', getfriend)
getfriend()

function showMemberData(){
    SectionMessage.classList.remove('show')
    Background.classList.remove('show')
    FormMemberdata.classList.add('show')
}

SectionOptionUser.addEventListener('click', showMemberData)
/*顯示好友搜尋*/
function optionJoinFriend(){
    sectionContentFriendSearch.classList.add('show')
    sectionContentFriendListContainer.classList.remove('show')
}

SectionOptionJoin.addEventListener('click', optionJoinFriend)

/*顯示好友名單*/
function optionFriendList(){
    sectionContentFriendSearch.classList.remove('show')
    sectionContentFriendListContainer.classList.add('show')
}

SectionOptionChat.addEventListener('click', optionFriendList)



