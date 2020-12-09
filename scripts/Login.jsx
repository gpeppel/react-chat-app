import React, { useState, useEffect } from 'react';
import { Button } from './Button';
import { Socket } from './Socket';
import { Chat } from './Chat';

export function Login() {
    const [user, setUser] = useState('');
    const [status, setStatus] = useState(false);
    
    useEffect(() => {
        Socket.on("existing_user", data => {
            setStatus(data['status']), setUser(data['username']);
        });
    });
    
    
        return (
        <div className="container">
        <div>
        {status
        ?<div>
            <Chat currentUser={ user }/>
        </div>
        :<div className="header">
           <img src="static/images/logo.png" />
            <Button />
        </div>
        }
        </div>
        </div>
        );
}