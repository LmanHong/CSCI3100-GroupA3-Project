# CUHK Tinder Chat
This folder contains all files for the LiveChat module of the CUHK Tinder project.

#### Pages
1. `chat/` **Chat Homepage**
2. `chat/<CHATROOM NAME>/` **Chatroom view**  

Please reference `views.py` for the actual implementations of the HTTP requests.

#### WebSocket paths
WebSockets are used for the real-time update of chat messages and the broadcasting of latest message created.  
1. `ws/chat/` **Latest message notification broadcast**
2. `ws/chat/<CHATROOM NAME>/` **Chatroom Chat messages send/receive**  

Please reference `consumers.py` and `static/chat/*.js` for the actual implementations the WebSocket consumers and front-end WebSocket respectively.

#### Models
1. `ChatMessage` **Single chat message record in a designated live chat.**
2. `ChatRoom` **Single chat room record between two users.**  

Please reference `models.py` for the functions for making queries.

