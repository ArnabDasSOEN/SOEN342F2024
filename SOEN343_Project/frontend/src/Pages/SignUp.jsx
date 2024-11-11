import React from 'react'
import './CSS/SignUp.css'
import { Link } from 'react-router-dom'

export const SignUp = () => {
    return (
        <div className="signup">
            <h2>Sign Up</h2>
            <form className="signup-page">
                <label className="name">Your Name</label>
                <input type="text" />
                <br/>
                <label className='email'>Email</label>
                <input type="email" />
                <br/>
                <label className='password'>Password</label>
                <input type="password" />
            </form>
            <button>Continue</button>
            <p className="loginsignup-login">Already have an account? <Link>Login here</Link></p>
            <div className="signup-agree">
                <input type="checkbox" />
                <p>By continuing, I agree to the terms of use & privacy policy</p>
            </div>
        </div>
    )
}
