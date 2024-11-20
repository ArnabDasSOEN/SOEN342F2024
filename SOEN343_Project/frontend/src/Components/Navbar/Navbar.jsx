// import React, { useState } from 'react'
import './Navbar.css'
import { Link } from 'react-router-dom'
import deliver_icon from '../Assets/Express_Delivery_Blue.png'
//import { useState } from 'react'

export const Navbar = ({isLoggedIn}) => {

  // const [menu, setMenu] = useState("landing")
  
  

  return (
    <div className='navbar'>
      <Link to='/' className='linkToLanding'>
        <div className='nav-logo'>
          <img src={deliver_icon} alt=''></img>
          <p>WHEELS UP</p>
        </div>
      </Link>
        <ul className="nav-menu">
          <li>Tracking</li>
          <li>Proposal</li>
          <li>Delivery</li>
          <li>Quotation</li>
        </ul>
        <div className='login-items'>
          <div className='login'>
            {/* {user_id == null ? <Link to='/login'><button>Login</button></Link> : <Link to='/logout'><button>Logout</button></Link>} */}
            <Link to='/login'><button>Login</button></Link>
          </div>
          <div className='signup'>
            <Link to='/signup'><button>Sign Up</button></Link>
          </div>
        </div>
    </div>
  )
}
