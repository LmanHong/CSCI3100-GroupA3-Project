const roomName = document.querySelector("h1").innerHTML;
const chatLog = document.querySelector(".chat-log");
const chatInput = document.getElementById("chat-input");
const chatSubmitBtn = document.getElementById("chat-submit-btn");
const chatReceiveBtn = document.getElementById("chat-receive-btn");

const url = 'http://'+window.location.host+'/chat/'+roomName+'/';
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const msgIdPrefix = 'msg-';

const sendMessage = async (e) =>{
    let message = chatInput.value;
    if (message != ''){
        let message_json = {
            'message_string':message,
            'message_status':'msg',
            'sent_time':Date.now()
        }
        console.log(message_json);
        try{
            let res = await fetch(url, {
                body: JSON.stringify(message_json),
                cache: 'no-cache',
                credentials: 'same-origin',
                headers:{
                    'content-type': 'application/json',
                    'X-CSRFToken':csrfToken
                },
                method: 'POST'
            })
            let res_json = await res.json();
            console.log(res_json);
        }catch(err){
            console.error("ERROR: ", err);
        }
        chatInput.value = '';
    }else console.error("ERROR: Chat message cannot be empty!");
}

const receiveMessage = async (e)=>{
    let getMsgCount = 10;
    let request_json = {
        'message_status':'spc',
        'special_request':'getMessages-'+getMsgCount,
        'sent_time':Date.now()
    }
    try{
        let res = await fetch(url, {
            body: JSON.stringify(request_json),
            cache: 'no-cache',
            credentials: 'same-origin',
            headers:{
                'content-type': 'application/json',
                'X-CSRFToken':csrfToken
            },
            method: 'POST'
        });
        let res_json = await res.json();
        if (res_json.status){
            messageList = res_json.message_list;
            for (var i=0; i<res_json.message_count; i++){
                console.log(messageList[i]);
                if (messageList[i].message_status == 'msg' && document.getElementById(msgIdPrefix+messageList[i].message_id) == null){
                    let msgPara = document.createElement('p');
                    let content = `${messageList[i].sent_by}: ${messageList[i].message_string} ---> ${messageList[i].sent_time}`;
                    msgPara.innerHTML = content;
                    msgPara.id = msgIdPrefix+messageList[i].message_id;
                    chatLog.appendChild(msgPara);
                }
            }
        }else throw TypeError("Response Status is false!");
    }catch(err){
        console.error('ERROR: ', err);
    }
}

chatSubmitBtn.addEventListener('click', sendMessage);
chatReceiveBtn.addEventListener('click', receiveMessage);
document.addEventListener('keyup', (e)=>{
    if (e.key == 'Enter') sendMessage();
});

