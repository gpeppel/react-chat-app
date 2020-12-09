import * as React from 'react';
import { Socket } from './Socket';

function handleSubmit(event) {
    let newUsername = document.getElementById("user_name");
    let newPw = document.getElementById("pw");
    Socket.emit('user_status', {
        'username': newUsername.value,
        'password': newPw.value
    });

    console.log('Sent the user data: ' + newUsername.value + ' and ' + newPw.value + ' to server!');
    newUsername.value = ''
    newPw.value = ''
    event.preventDefault();
}

export function Button() {
    return (
        <div className="container">
        <form className="form-control" onSubmit={handleSubmit}>
            <input id="user_name" type="text" placeholder="Enter Username" />
            <input id="pw" type="text" placeholder="Enter Password" />
            <input type="submit" value = "Submit" className="btn btn-primary"/>
        </form>
        </div>
    );
}
