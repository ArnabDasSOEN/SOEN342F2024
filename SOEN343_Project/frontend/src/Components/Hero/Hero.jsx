import React from 'react'
import delivery_boxes from '../Assets/delivery_package_boxes.png'
import './Hero.css'

export const Hero = () => {
  return (
    <div className='hero'>
        <div className="hero-left">
            <p>
                SEND, <br/> TRACK, <br/> DELIVER, <br/> DONE.
            </p>
        </div>
        <div className="hero-right">
            <img src={delivery_boxes} alt=''></img>
        </div>
    </div>
  )
}
