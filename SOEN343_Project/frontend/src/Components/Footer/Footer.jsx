import React from 'react';
import './Footer.css';
import deliver_icon from '../Assets/Express_Delivery.png'

export const Footer = () => {
    return (
        <div className='footer'>
            <div className="footer-logo">
                <p><img src={deliver_icon} alt=''></img>WHEELS UP</p>
            </div>
            <div className="footer-copyright">
                <p>Copyright @2024 - All Rights Reserved</p>
            </div>
        </div>
    );
}
