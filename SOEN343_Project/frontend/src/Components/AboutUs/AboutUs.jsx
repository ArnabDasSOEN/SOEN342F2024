import React, { useEffect } from 'react';
import './AboutUs.css';

export const AboutUs = () => {
  useEffect(() => {
    const aboutContainer = document.querySelector('.about-container');
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          aboutContainer.classList.add('fade-in');
        } else {
          aboutContainer.classList.remove('fade-in');
        }
      },
      { threshold: 0.5 }
    );

    if (aboutContainer) observer.observe(aboutContainer);

    return () => {
      if (aboutContainer) observer.unobserve(aboutContainer);
    };
  }, []);

  return (
    <div className="about-container">
      <h1 className="about-heading">We Simplify Deliveries</h1>
      <p className="about-description">
        We are passionate about revolutionizing delivery services by combining speed, reliability, and customer
        satisfaction. Our platform bridges the gap between convenience and efficiency, offering features like 
        real-time tracking, secure payment processing, and dedicated customer support. Whether it's fragile items 
        or regular deliveries, we ensure every package reaches its destination safely and on time.
      </p>
    </div>
  );
};

export default AboutUs;
