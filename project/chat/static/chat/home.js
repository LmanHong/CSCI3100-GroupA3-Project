const url = 'http://'+window.location.host + '/chat/';
const chatroomUrl = null;
const wsUrl = 'ws://'+window.location.host+'/ws/chat/';
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const myUsername = document.getElementById('my-username').value;

const friendListDiv = document.querySelector('.friendListDiv');
const chatroomDiv = document.querySelector('.chatroomDiv');
const friendsRef = document.querySelectorAll('.friendA');
const chatroomFrameRef = document.querySelector('.chatroomFrame');
const placeholderSpanRef = document.querySelector('.placeholder');
const userProfileImageRef = document.getElementById('user-profile-image');
const slideMenuBtn = document.querySelector('.fixed-slide-menu-btn');
const overlayDiv = document.querySelector('.overlay');

var isProcessing = false;
var isMenuOpened = false;

const notificationSocket = new WebSocket(wsUrl);

//Helper function for escaping any special characters
function escapeSpecialChar(str){
    var tmp = str.replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/'/g, "&apos;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/{/g, "&#123;").replace(/}/g, "&#125;");
    return tmp;
}

notificationSocket.onmessage = async (e) =>{
    const data = await JSON.parse(e.data);
    console.log(data);
    let targetUsername = (data.sent_by == myUsername?data.sent_to:data.sent_by)
    console.log(targetUsername)
    const friendNameSpan = document.querySelectorAll('.friend-name');
    friendNameSpan.forEach((ref)=>{
        if (ref.innerHTML == targetUsername){
            console.log(ref.nextElementSibling);
            ref.nextElementSibling.innerHTML = escapeSpecialChar(data.message_string);
        }
    });
};

notificationSocket.onclose = async (e) =>{
    console.error('ERROR: notification socket closed.');
};

const getChatroom = async (toUserId) =>{
    try{
        let res = await fetch(url, {
            body: JSON.stringify({
                'to_user_id': toUserId
            }),
            cache: 'no-cache',
            credential: 'same-origin',
            headers: {
                'X-CSRFToken': csrfToken,
                'content-type': 'application/json'
            },
            method: 'POST'
        });
        let res_json = await res.json();
        if (res_json.status && res_json.room_name){
            return {
                'status': true,
                'room_name': res_json.room_name
            };
        }else if (res_json.error){
            throw TypeError("Server Error: ", res_json.error);
        }else{
            throw TypeError("Server Error unknown!");
        }
    }catch(err){
        console.error('ERROR: ', err);
        return {
            'status': false,
            'error': err
        };
    }

};

const renderChatroom = async (e)=>{
    let toUserId = (e.target.nodeName == "A"?e.target.id:(e.target.parentElement.nodeName == "A"?e.target.parentNode.id:e.target.parentNode.parentNode.id));
    console.log("friend id: ", toUserId);
    if (isProcessing){
        console.error("ERROR: Another chatroom is requesting.");
    }else{
        isProcessing = true;
        let roomName = await getChatroom(toUserId);
        if (roomName.status){
            console.log("Got room name: ", roomName.room_name);
            chatroomFrameRef.src = url + roomName.room_name + "/";
            placeholderSpanRef.style.display = "none";
            chatroomFrameRef.style.display = "block";
            if (window.innerWidth<=576) toggleSlideMenu(); 
        }else{
            console.log("Got error: ", roomName.error);
        }
        isProcessing = false;

    }
};

const toggleSlideMenu = ()=>{
    if (window.innerWidth<=576){
        overlayDiv.style.backgroundColor = (isMenuOpened?"rgba(0, 0, 0, 0)":"rgba(0, 0, 0, 0.4)");
        overlayDiv.style.zIndex = (isMenuOpened?"-1":"1");
        friendListDiv.style.width = (isMenuOpened?"0px":"260px");
        isMenuOpened = !isMenuOpened;
    }
};

friendsRef.forEach((friendRef)=>{
    friendRef.addEventListener('click', renderChatroom);
});

userProfileImageRef.addEventListener('click', (e)=>{
    window.location.href = 'http://'+window.location.host+'/account/profile/';
});

slideMenuBtn.addEventListener('click', toggleSlideMenu);