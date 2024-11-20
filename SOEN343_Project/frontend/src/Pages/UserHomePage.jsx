import { Link } from "react-router-dom";
import { DashboardCard } from "../Components/DashboardCard/DashboardCard";
import './CSS/UserHomePage.css'

export const UserHomePage = () => {
    return(
        <div className="user-homepage">
            <h1>Welcome to your User Dashboard</h1>
            <div className="user-homepage-cards-container">
                <Link className="requestdelivery" to="/dashboard" >
                    <DashboardCard
                        title = "Request Delivery"
                        description = "Start a new delivery request here"
                    />
                </Link>
                <DashboardCard 
                    title = "Track Delivery"
                    description = "View the status of ongoing delivieries"
                />
            </div>
        </div>
    );

}