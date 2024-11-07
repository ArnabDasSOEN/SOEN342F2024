// import React, { useState } from 'react'
import './Navbar.css'
import { Link } from 'react-router-dom'
import deliver_icon from '../Assets/Express_Delivery.png'

export const Navbar = () => {

  // const [menu, setMenu] = useState("landing")

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
              <Link to='/login'><button>Login</button></Link>
          </div>
          <div className='signup'>
            <button>Sign Up</button>
          </div>
        </div>
    </div>
  )
}
