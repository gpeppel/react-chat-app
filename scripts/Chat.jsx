import React, { useState, useEffect } from 'react';
import { Socket } from './Socket';

export function Chat(props) {
    const [messages, setMessages] = useState(["Hello and Welcome!"]);
    const [message, setMessage] = useState([]);
    const [user, setUser] = useState('');
    let [alert, setAlert]= useState(false);
    
    // useEffect ---> componentDidUpdate in hook form 
    // calls when message length changes
    useEffect(() => {
        getMessages();
    });
    
    // called 1st time app renders & every time message length changes
    const getMessages = () => {
        Socket.on("msg", msg => {
           setMessages(msg['all_messages']);
            // setUser(msg['all_users']);
            let arr2 = msg['all_users'];
            let arr = msg['all_messages'];
            let arr3 = []
                //  setMessages(arr.map((data, index) => 
            let i;
            for (i = 0; i <= arr.length; i++) {
                arr3.push(<ul key={i}>{ arr2[i] } { arr[i] }</ul>);
            };
            setMessages(arr3);
        });
    };
    
    // input field called
    const onChange = e => {
        setMessage(e.target.value);
    };

    const onClick = () => {
        if (message !== "") {
            // btn clicked ---> send msg to server
            Socket.emit("message", {"message" : message, "username": props.currentUser});
            setMessage("");
            // setUser(props.currentUser);
        } else {
            alert("Please Add a Message");
        }
    };
    
    return (
        <div>
            <div className="msg_container">
                { messages }
            </div>
            <div className="container">
            {/* input */}
            <input value={ message } name="message" onChange={ e => onChange(e) } />
            {/* btn */}
            <button onClick={ () => onClick() }>Send Message</button>
            </div>
        </div>
    );
};