import React from 'react';
import './Footer.css';
import deliver_icon from '../Assets/Express_Delivery_White.png'

export const Footer = () => {
    return (
        <div className='footer'>        
            <ul className="footer-links">
                <li>Company</li>
                <li>Products</li>
                <li>Offices</li>
                <li>About</li>
                <li>Contact</li>
            </ul>
            <div className="footer-logo">
                <img src={deliver_icon} alt=''></img>
                <p>WHEELS UP</p>
            </div>
            <div className="footer-copyright">
                <p>Copyright @2024 - All Rights Reserved</p>
            </div>
        </div>
    );
}
