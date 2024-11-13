import React from 'react'
import './CSS/SignUp.css'
import { Link } from 'react-router-dom'

export const SignUp = () => {
    return (
        <div className="signup">
            <h2>Sign Up</h2>
            <form className="signup-page">
                <label htmlFor="name">Name</label>
                <input type="text" />
                <br/>
                <label htmlFor="phone_number">Phone Number</label>
                <input type="tel" />
                <br/>
                <label className='email'>Email Address</label>
                <input type="email" />
                <br/>
                <label htmlFor='password'>Password</label>
                <input type="password" />
                <br/>
                <label htmlFor="confirm_password">Confirm Password</label>
                <input type="password" />
            </form>
            <button>Continue</button>
            <p className="loginsignup-login">Already have an account? <Link to='/login' className='login-link'>Login here</Link></p>
            <div className="signup-agree">
                <input type="checkbox" />
                <p>By continuing, I agree to the terms of use & privacy policy</p>
            </div>
        </div>
    )
}
