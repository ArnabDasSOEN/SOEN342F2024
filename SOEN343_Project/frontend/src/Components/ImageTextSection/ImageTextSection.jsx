import React from 'react';
import './ImageTextSection.css';
import delivery_woman from '../Assets//ParcelDeliveryWoman.png'

export const ImageTextSection = () => {
  return (
    <div className="image-text-section">
      <div className="image-container">
        <img
          src={delivery_woman} 
          alt="Feature"
        />
      </div>
      <div className="text-container">
        <h2>Exclusive Discounts</h2>
        <p>
          Save big on your next delivery with our special offers. Experience the fastest and 
          most reliable delivery services at unbeatable prices. Don't miss out!
        </p>
        <button className="action-button">View Offers</button>
      </div>
    </div>
  );
};

export default ImageTextSection;
