import React from 'react'
import './Navbar.css'
import deliver_icon from '../Assets/Express_Delivery.png'

export const Navbar = () => {
  return (
    <div className='navbar'>
      <div className='nav-logo'>
        <img src={deliver_icon} alt=''></img>
        <p>WHEELS UP</p>
      </div>
        <ul className="nav-menu">
          <li>Tracking</li>
          <li>Proposal</li>
          <li>Delivery</li>
          <li>Quotation</li>
        </ul>
        <div className='login-items'>
          <div className='login'>
              <li>Login</li>
          </div>
          <div className='signup'>
            <button>Sign Up</button>
          </div>
        </div>
    </div>
  )
}
