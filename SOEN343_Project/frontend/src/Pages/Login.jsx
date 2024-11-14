import React from 'react'
import './CSS/Login.css'
import { Link } from 'react-router-dom'
import facebook_logo from '../Components/Assets/Facebook.png'
import google_logo from '../Components/Assets/Google.png'
import twitter_logo from '../Components/Assets/TwitterX.png'
import apple_logo from '../Components/Assets/Apple Logo.png'
import amazon_logo from '../Components/Assets/Amazon.png'

export const Login = () => {
  return (
    <div className="loginPage">
        <h2>Log In</h2>
        <form className="loginForm">
          <label>Email or Username</label>
          <input type="email"></input>
          <br/>
          <label>Password</label>
          <input type="password"></input>
          <br/>
        </form>
          <div className='otherLoginOptions'>
          <button type="submit" className="loginButton">Login</button>
          <p><span>Or with</span></p>
          </div>
          <div className="company-logos">
            <img src={google_logo} alt="" className="google" />
            <img src={facebook_logo} alt="" className="facebook" />
            <img src={twitter_logo} alt="" className="twitter" />
            <img src={apple_logo} alt="" className="apple" />
            <img src={amazon_logo} alt="" className="amazon" />
          </div>
          <p className='signup-from-login'>Don't have an account? <Link to='/signup' className='signup-link'>Sign up here</Link></p>
        
    </div>
  )
}
