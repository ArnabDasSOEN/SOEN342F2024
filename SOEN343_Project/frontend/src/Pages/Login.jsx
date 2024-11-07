import React from 'react'
import './CSS/Login.css'
export const Login = () => {
  return (
    <div className="loginForm">
        <form className="login">
            <div className="loginFormElement">
                <h2>Log In</h2>
                <label>Email or Username</label>
                <input type="email"></input>
                <br/>
                <label>Password</label>
                <input type="password"></input>
                <br/>
                <button type="submit" className="loginButton">Login</button>
                <p><span>Or with</span></p>
            </div>
        </form>
    </div>
  )
}
