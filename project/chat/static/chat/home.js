//Constants for sending and receiving latest messages and rendering chatroom view
const url = 'http://'+window.location.host + '/chat/';
const chatroomUrl = null;
const wsUrl = 'ws://'+window.location.host+'/ws/chat/';
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const myUsername = document.getElementById('my-username').value;

//References of DOM objects
const friendListDiv = document.querySelector('.friendListDiv');
const chatroomDiv = document.querySelector('.chatroomDiv');
const friendsRef = document.querySelectorAll('.friendA');
const chatroomFrameRef = document.querySelector('.chatroomFrame');
const placeholderSpanRef = document.querySelector('.placeholder');
const userProfileImageRef = document.getElementById('user-profile-image');
const slideMenuBtn = document.querySelector('.fixed-slide-menu-btn');
const overlayDiv = document.querySelector('.overlay');

//Flags
var isProcessing = false;
var isMenuOpened = false;

//WebSocket for receiving latest message broadcasts
const notificationSocket = new WebSocket(wsUrl);

//Helper function for escaping any special characters
function escapeSpecialChar(str){
    var tmp = str.replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/'/g, "&apos;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/{/g, "&#123;").replace(/}/g, "&#125;");
    return tmp;
}

//WebSocket event listener for receiving latest messages and updating friend list side menu
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

//Websocket Event listener for closing connection
notificationSocket.onclose = async (e) =>{
    console.error('ERROR: notification socket closed.');
};

//Helper function for getting the chatroom between the current user and the target user
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

//Helper function for rendering the chatroom view in the iframe of the chatroom window
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

//Helper function for toggling the friend list side menu. Small screen devices only.
const toggleSlideMenu = ()=>{
    if (window.innerWidth<=576){
        overlayDiv.style.backgroundColor = (isMenuOpened?"rgba(0, 0, 0, 0)":"rgba(0, 0, 0, 0.4)");
        overlayDiv.style.zIndex = (isMenuOpened?"-1":"1");
        friendListDiv.style.width = (isMenuOpened?"0px":"260px");
        isMenuOpened = !isMenuOpened;
    }
};

//Event listeners for clicking the friend profiles in the friend list side menu
friendsRef.forEach((friendRef)=>{
    friendRef.addEventListener('click', renderChatroom);
});

//Event listener for clicking the user avatar image at the top left of friend list side menu
userProfileImageRef.addEventListener('click', (e)=>{
    window.location.href = 'http://'+window.location.host+'/account/profile/';
});

//Event listener for clicking the friend list side menu toggle button. Small screen devices only.
slideMenuBtn.addEventListener('click', toggleSlideMenu);