import React, { useState, useEffect, useRef } from 'react';
import './styles/Chat.css';
import { FaMicrophone } from "react-icons/fa";
import axios from 'axios'
import axiosInstance from '../utils/AxiosInstace';

const Chat = ({ id, setModalActive }) => {
  
  const [chatRecord, setChatRecord] = useState([]);
  const [transcript, setTranscript] = useState('');
  const [isListening, setIsListening] = useState(true);
  const recognitionRef = useRef(null);
  const interimTranscript = useRef('');
  const [isSpeaking, setIsSpeaking] = useState(false);

  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState([]);
  const chatContainerRef = useRef(null);
  const [repeater, setRepeater] = useState(0)

  const retrieveRecords = async () => {
    try {
      const res = await axiosInstance.get(`/chat_logs/messages/${id}`)
      console.log("chats from", id)
      console.log(res)
      setChatRecord(res.data)
    } catch (e) {
      console.log(e)
    }
  }

  const sendNewChat = async (message) => {
    try {
      const formData = { chat: id, message_content: message, sender: "User" };
      const res = await axiosInstance.post(`/chat_logs/`,
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      setMessages((prevMessages) => [
        ...prevMessages,
        { content: res.data.message_content, sender: res.data.sender },
      ]);
  
      if (res.data.message_content.trim()) {
        const speech = new SpeechSynthesisUtterance(res.data.message_content);
        speech.lang = "en-US";
        speech.pitch = 10;
        speech.rate = 1;
  
        // Set the onstart and onend callbacks for speech synthesis
        speech.onstart = () => setIsSpeaking(true);
        speech.onend = () => {
          setIsSpeaking(false);
          setIsListening(false);
  
          // Proceed with the rest of the logic after speech has ended
          setRepeater((prevRepeater) => prevRepeater + 1);
  
          if (res.data.message_content === "exit") {
            setIsListening(false);
          } else {
            setIsListening(true);
          }
        };
  
        // Speak the message
        window.speechSynthesis.speak(speech);
      } else {
        setRepeater((prevRepeater) => prevRepeater + 1);
  
        if (res.data.message_content === "exit") {
          setIsListening(false);
          
        } else {
          setIsListening(true);
        }
      }
    } catch (e) {
      console.log(e);
    }
  };
  

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    retrieveRecords()
  }, [])

  useEffect(() => {
    setMessages([])
    chatRecord.map((chat) => {
      setMessages((prevMessages) => [...prevMessages, { chat: id, content: chat.message_content, sender: chat.sender }])
    })
  }, [chatRecord])

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleKeyDown = (newMessage) => {
    if (!(newMessage == '')) {
      setMessages((prevMessages) => [...prevMessages, { content: newMessage, sender: "User" }]);
      setInputValue('');
    }
  };

  useEffect(() => {
    if (!('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)) {
      console.log("Speech Recognition API is not supported in this browser.");
      return;
    }
  
    recognitionRef.current = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    const recognition = recognitionRef.current;
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';
  
    let inactivityTimeout;  // Variable to hold the timeout ID
  
    recognition.onresult = (event) => {
      clearTimeout(inactivityTimeout); // Reset timeout whenever speech is detected
  
      interimTranscript.current = Array.from(event.results)
        .map((result) => result[0].transcript)
        .join('');
  
      console.log(interimTranscript.current);
  
      // Restart inactivity timer (3 seconds) after speech input
      inactivityTimeout = setTimeout(() => {
        console.log("No input detected for 3 seconds, stopping recognition.");
        recognition.stop()
        setIsListening(false); // Stop listening after 3 seconds of inactivity
         // Stop listening after 3 seconds of inactivity
      }, 1500);  // 3000 ms = 3 seconds
    };
  
    recognition.onerror = (event) => {
      console.log('Speech recognition error:', event);
      setIsListening(false);
    };
  
    recognition.onend = () => {

      if (interimTranscript.current === '') {
        const customMess = "No Input Detected. Please provide a new response.";
        if (customMess.trim()) {
          const speech = new SpeechSynthesisUtterance(customMess);
          speech.lang = "en-US";
          speech.pitch = 1;
          speech.rate = 1;
  
          speech.onstart = () => setIsSpeaking(true);
          speech.onend = () => setIsSpeaking(false);
  
          window.speechSynthesis.speak(speech);
        }
      } else if (interimTranscript.current === "exit") {
        const exitMess = "Closing Program. Thank you for using PyChat";
        if (exitMess.trim()) {
          const speech = new SpeechSynthesisUtterance(exitMess);
          speech.lang = "en-US";
          speech.pitch = 1;
          speech.rate = 1;
  
          speech.onstart = () => setIsSpeaking(true);
          speech.onend = () => {
            setIsSpeaking(false)
            setModalActive(false)
          };
  
          window.speechSynthesis.speak(speech);
        }
      } else {
        recognition.stop();
        setTranscript((prevTranscript) => prevTranscript + ' ' + interimTranscript.current);
        recognition.stop();
        sendNewChat(interimTranscript.current);
      }
    };
  
    // Cleanup the timeout on component unmount
    return () => {
      if (inactivityTimeout) {
        clearTimeout(inactivityTimeout);
      }
      recognition.stop();
    };
  }, []);
  

  useEffect(() => {
    // console.log(repeater)
    const recognition = recognitionRef.current;
    if (isListening) {
      const welcomeMess = "Listening for commands...";
      if (welcomeMess.trim()) {
        const speech = new SpeechSynthesisUtterance(welcomeMess);
        speech.lang = "en-US";
        speech.pitch = 1;
        speech.rate = 1;

        speech.onstart = () => setIsSpeaking(true);
        speech.onend = () => setIsSpeaking(false);

        window.speechSynthesis.speak(speech);
      }
      setTranscript('');
      setTimeout(() => {
        recognition.start();
      }, 1500);
    } else {
      recognition.stop();
    }
  }, [isListening, repeater]);

  useEffect(() => {
    handleKeyDown(transcript)
  }, [transcript])

  useEffect(() => {
    console.log(messages)
  }, [messages])

  const toggleListening = () => {
    setIsListening((prevState) => !prevState);
  };

  return (
    <div className='dashboard-content__container'>
      <div className="chat-main__container">
        <div className="chat-header">
          <div>PyChat {isListening ? 'Stop Listening' : 'Start Listening'}</div>
        </div>
        <div className="chat-log__container" ref={chatContainerRef}>
          {
            messages.map((message, index) => {
              console.log(message)
              return (
                message.sender === 'User' ? (
                  <div key={index} className="user-message">
                    <div className="chat-content">
                      {message.content}
                    </div>
                  </div>
                ) : (
                  <div key={index} className="pychat-message">
                    <div className="chat-content">
                      {message.content}
                    </div>
                  </div>
                )
              );
            })
          }

        </div>
        <div className="chat-controls__container">
          <input type="text" className='custom-input' placeholder='Send a message...' value={transcript} onChange={() => handleInputChange()} />
          <div className="chat-controls__buttons">
            <button className={`control-button ${isListening ? 'active' : ''}`} onClick={toggleListening}>
              <FaMicrophone />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
