import React, { useEffect } from 'react';
import './ServiceDescription.css';

export const ServiceDescription = () => {
  useEffect(() => {
    // Select all description items
    const descriptionItems = document.querySelectorAll('.description-item');

    // Function to check if the element is in the viewport
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          // Add the fade-in class when the item is in the viewport
          entry.target.classList.add('fade-in');
        } else {
          // Optional: Remove class when the item is out of view (to allow animation trigger again)
          entry.target.classList.remove('fade-in');
        }
      });
    }, { threshold: 0.5 }); // Trigger when 50% of the item is visible

    // Observe each description item
    descriptionItems.forEach((item) => {
      observer.observe(item);
    });

    return () => {
      descriptionItems.forEach((item) => {
        observer.unobserve(item);
      });
    };
  }, []);

  return (
    <section className="service-description">
      <div className="description-item">
        <h3>Fast Delivery</h3>
        <p>
          Get your packages delivered in record time with our express delivery service.
        </p>
      </div>
      <div className="description-item">
        <h3>Real-Time Tracking</h3>
        <p>
          Track your delivery in real time to stay updated on its status from start to finish.
        </p>
      </div>
      <div className="description-item">
        <h3>Customer Support</h3>
        <p>
          Our dedicated support team is available 24/7 to assist you with any concerns or inquiries.
        </p>
      </div>
    </section>
  );
};

export default ServiceDescription;
