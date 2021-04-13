//Constant array of month names
const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

//References of DOM objects
const roomName = document.querySelector("h1").innerHTML;
const chatLog = document.querySelector(".chat-log");
const chatInput = document.getElementById("chat-input");
const chatSubmitBtn = document.getElementById("chat-submit-btn");

//Constants for sending and receiving messages
const wsUrl = 'ws://'+window.location.host+'/ws/chat/'+roomName+'/';
const url = 'http://'+window.location.host+'/chat/'+roomName+'/';
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const msgIdPrefix = 'msg-';

//WebSocket objects
const chatSocket = new WebSocket(wsUrl);
const isWebSocket = true;

//Helper function for converting a datetime string to correct format
const normalizedDateTime = (dateStr, hour24=false) =>{
    let date = new Date(dateStr);
    let month = months[date.getMonth()];
    let time = "";
    if (hour24) time = `${date.getHours()}:${date.getMinutes()}`;
    else time = `${(date.getHours()%12==0?12:date.getHours()%12)}:${date.getMinutes()} ${(date.getHours()/12>0?"p.m.":"a.m.")}`;
    return `${month} ${date.getDate()}, ${date.getFullYear()}, ${time}`;
};

//Websocket Event listener for receiving messages 
chatSocket.onmessage = async (e) =>{
    const data = await JSON.parse(e.data);
    console.log(data);
    if (data.message_status == 'msg' && document.getElementById(msgIdPrefix+data.message_id) == null){
        let msgPara = document.createElement('p');
        let content = `${data.sent_by}: ${data.message_string} ---> ${normalizedDateTime(data.sent_time)}`;
        msgPara.innerHTML = content;
        msgPara.id = msgIdPrefix+data.message_id;
        chatLog.appendChild(msgPara);
    }
};

//Websocket Event listener for closing connection
chatSocket.onclose = async (e) =>{
    isWebSocket = false;
    console.error('ERROR: Chat Socket closed.');
};

//Helper function for sending chat messages
const sendMessage = async (e) =>{
    let message = chatInput.value;
    if (message != ''){
        let message_json = {
            'message_string':message,
            'message_status':'msg',
            'sent_time':Date.now()
        }
        console.log(message_json);
        if (isWebSocket){
            //send chat messages via WebSocket
            try{
                chatSocket.send(JSON.stringify(message_json));
                console.log('message sent.');
            }catch(err){
                console.error("ERROR: ", err);
            }
        }else{
            throw TypeError("WebSocket is not available.");
        }
        chatInput.value = '';
    }else console.error("ERROR: Chat message cannot be empty!");
}

chatSubmitBtn.addEventListener('click', sendMessage);
document.addEventListener('keyup', (e)=>{
    if (e.key == 'Enter') sendMessage();
});

