import React, { useEffect, useState } from 'react'
import './styles/Shared.css'
import './styles/ChatList.css'
import Divider from '@mui/material/Divider'
import { FaPlus } from "react-icons/fa";
import axios from 'axios'
import './styles/ModalAnims.css'
import Chat from './Chat';
import Skeleton from '@mui/material/Skeleton';

const ChatList = () => {
    const [modalActive, setModalActive] = useState(false);
    const [modalClass, setModalClass] = useState('');
    const [selId, setSelId] = useState()

    const handleButtonClick = async (buttonId, id) => {
        await setSelId(id)
        setModalClass(buttonId);  // Set modal class based on the button clicked
        setModalActive(true);  // Activate modal
    };

    const handleModalClick = () => {
        setModalClass('out');  // Add 'out' class for closing animation
        setModalActive(false);  // Deactivate modal
    };

    const [chatList, setChatList] = useState([])
    const loadChatList = async () => {
        try {
            const res = await axios.get('https://pychat-re.onrender.com/api/chats/')
            setChatList(res.data)
        } catch (e) {
            console.log(e)
        }
    }

    const openChat = async(id) => {
        try {
            setModalActive(false)
            await setSelId(id)
            setModalClass('seven')
            setModalActive(true)
        } catch(e) {
            console.log(e)
        }
    }

    const handleNewChat = async () => {
        try {
            const formData = { "title": "PyChat Message", "description": "Testing Messaging." }
            const res = await axios.post(`https://pychat-re.onrender.com/api/chats/`, formData)
            console.log(res.data)
            await setSelId(res.data.id)
            const formDataLogs = { chat: res.data.id, message_content: "Hello, I am PyChat. To start our conversation, please click on the mic button below.", sender: "PyChat" };
            const resLogs = await axios.post(
                `https://pychat-re.onrender.com/api/chat_logs/`,
                formDataLogs,
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );
            console.log(resLogs)
            setModalClass('seven')
            setModalActive(true)
        } catch (e) {
            console.log(e)
        }
    }

    const handleDelete = async (id) => {
        try {
            const res = await axios.delete(`https://pychat-re.onrender.com/api/chats/${id}/`)
            loadChatList()
        } catch(e) {
            console.log(e)
        }
    }

    useEffect(() => {
        loadChatList()
    }, [])

    useEffect(() => {
        loadChatList()
    }, [modalActive])

    return (
        <div className='dashboard-content__container'>
            {modalActive && (
                <div className={modalClass} id="modal-container" onClick={handleModalClick}>
                    <div className="modal-background">
                        <div className="modal" onClick={(e) => e.stopPropagation()}>
                            <Chat id={selId} setModalActive={setModalActive}/>
                        </div>
                    </div>
                </div>
            )}
            <div className="dashboard-title__common">
                Select a Chat Log
            </div>
            <Divider />
            <div className="sm-spacer"></div>
            <div className="bars-container">
                <div className="bar-item create-bar__item" tabIndex="0" onClick={() => { handleNewChat() }}>
                    <FaPlus /> &nbsp;
                    Create New Chat
                </div>
                {
                    chatList.length > 0 ? (
                        chatList.map((chat, index) => {
                            // Ensure chat.logs is not empty
                            const lastLog = chat.logs && chat.logs.length > 0 ? chat.logs[chat.logs.length - 1] : null;
                            const firstLog = chat.logs && chat.logs.length > 1 ? chat.logs[1] : null;

                            // Format the date if timestamp exists
                            const formattedDate = lastLog?.timestamp
                                ? new Date(lastLog.timestamp).toLocaleString("en-US", {
                                    month: "long",
                                    day: "numeric",
                                    year: "numeric",
                                    hour: "numeric",
                                    minute: "numeric",
                                    hour12: true,
                                    timeZone: "UTC",
                                })
                                : "No timestamp available";

                            // Provide fallback values
                            const chatId = chat.id || "No ID available";
                            const startingMessage = firstLog?.message_content || "No starting message available";

                            return (
                                <div key={index} className="bar-item chat-item">
                                    <div className="chat-id">ID: {chatId}</div>
                                    <div className="chat-title" onClick={() => {openChat(chat.id)}}>Starting Message: {startingMessage}</div>
                                    <div className="chat-timestamps">Last Message: {formattedDate}</div>
                                    <button onClick={() => {handleDelete(chat.id)}}>Delete</button>
                                </div>
                            );
                        })
                    ) : (
                        <Skeleton variant="rounded" width="100%" height={140} />
                    )
                }
            </div>
        </div>
    )
}

export default ChatList