const url = 'http://'+window.location.host + '/chat/';
const chatroomUrl = null;
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

const friendListDiv = document.querySelector('.friendListDiv');
const chatroomDiv = document.querySelector('.chatroomDiv');
const friendsRef = document.querySelectorAll('.friendA');
const chatroomFrameRef = document.querySelector('.chatroomFrame');
const placeholderSpanRef = document.querySelector('.placeholder');

var isProcessing = false;

window.addEventListener('resize', (e)=>{
    chatroomFrameRef.width = window.innerWidth*0.8;
    chatroomFrameRef.height = window.innerHeight;
});

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
    console.log(e.target);
    let toUserId = e.target.id;
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
        }else{
            console.log("Got error: ", roomName.error);
        }
        isProcessing = false;
    }
};

friendsRef.forEach((friendRef)=>{
    friendRef.addEventListener('click', renderChatroom);
});


