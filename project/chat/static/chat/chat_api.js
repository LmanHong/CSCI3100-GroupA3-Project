const roomName = document.querySelector("h1").innerHTML;
const chatLog = document.querySelector(".chat-log");
const chatInput = document.getElementById("chat-input");
const chatSubmitBtn = document.getElementById("chat-submit-btn");

const url = 'http://'+window.location.host+'/chat/'+roomName+'/';
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

chatSubmitBtn.addEventListener('click', (e)=>{
    let message = chatInput.value;
    message_json = {
        'message_string':message,
        'message_status':'chat_msg',
        'sent_time':Date.now()
    }
    console.log(message_json);
    fetch(url, {
        body: JSON.stringify(message_json),
        cache: 'no-cache',
        credentials: 'same-origin',
        headers:{
            'content-type': 'application/json',
            'X-CSRFToken':csrfToken
        },
        method: 'POST'
    }).then(async res => {
        let res_json = await res.json();
        console.log(res_json);
    }).catch(err =>{
        console.error('ERROR: ', err);
    });
    chatInput.value = '';
});