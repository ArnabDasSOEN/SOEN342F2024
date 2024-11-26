import React from 'react';
import './DashboardCard.css';

export const DashboardCard = ({ title, description }) => {
  return (
    <div className="dashboard-card">
      <h5 className="dashboard-card-title">{title}</h5>
      <p className="dashboard-card-description">{description}</p>
    </div>
  );
};
