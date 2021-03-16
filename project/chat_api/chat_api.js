/* This is the frontend API for the LiveChat function of the CUHK Tinder Project */ 

/**
 * Status object.
 * @typedef {Object} Status
 * @property {boolean} success - Indicator of the status
 * @property {?string} errMsg - Error message of unsuccessful status. null if successful status.
 */

/**
 * Chat message object.
 * @typedef {Object} ChatMessage
 */

/**
 * Live chat object.
 * @typedef {Object} ChatContent
 */

class ChatMessage{

    /** 
     * Represent a single chat message to be sent.
     * @constructor 
     * @param {!number} chatID - ID of the chat which this chat message belongs to.
     * @param {string} [messageString] - String representation of the chat message body.
     * @param {Object} [file] - File object to be sent in the chat message body.
     * @param {Status} messageStatus- Message status code indicating the type of chat message.
     */
    constructor(chatID, messageString=null, file=null, messageStatus){
    }

    /**
     * Modify the message body of the chat message, and subsequently the message status code.
     * @param {(string|Object)} messageBody - Body of the chat message.
     * @return {Status} Status of the modify operation.
     */
    modify(messageBody){
    }

    /**
     * Send the chat message to the designated chat.
     * @return {Status} Status of the send operation.  
     */
    send(){
    }

    /**
     * Forward the chat message to the designated chat.
     * @param {number} chatID - ID of the chat to be forwarded.
     * @returns {Status} Status of the forward operation.
     * @returns {?ChatMessage} New chat message object in the destination chat, null if unsuccessful.
     */
    forward(chatID){
    }

    /**
     * Delete the chat message.
     * @return {Status} Status of the delete operation.
     */
    delete(){

    }

    /**
     * Copying a chat message to another. 
     * @param {ChatContent} src - Chat message to be copied.
     * @param {ChatContent} dst - Destination of the copying of chat message.
     * @return {Status} Status of the copy operation.
     */
    static copy(src, dst){
    }

}

class ChatContent{
    /**
     * Represent a chat between two users.
     * @constructor
     * @param {string} fromUser - Username of the chat initiating user.
     * @param {string} toUser - Username of the destination user.
     */
    constructor(fromUser, toUser){
    }

    /**
     * Check whether a chat between two users already exist.
     * @param {!string} user1 - Username of user1.
     * @param {!string} user2 - Username of user2.
     * @return {?number} Chat ID of the chat between two users, null if chat does not exist.  
     */
    static isAlreadyExist(user1, user2){
    }
}