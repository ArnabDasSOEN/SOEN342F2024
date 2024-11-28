import React from 'react'
import './ContactUs.css'

export const ContactUs = () => {
  return (
          <div className="contact-us">
                <h2>Contact Us</h2>
                <form className="contact-us-form">
                  <label htmlFor="name">Name</label>
                  <input      
                    type="text"
                    name="name"
                  />
                  <br />
                  <label htmlFor="phone_number">Phone Number</label>
                  <input
                    type="tel"
                    name="phone_number"
                  />
                  <br />
                  <label className="email">Email Address</label>
                  <input
                    type="email"
                    name="email"
                  />
                  <br />
                  <label htmlFor="">Message</label>
                  <textarea name="" id=""></textarea>
                  <br />
          <button type="submit">Submit</button>
      </form>
    </div>
  )
}
