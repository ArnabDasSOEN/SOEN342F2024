import { Link } from "react-router-dom";
import { DashboardCard } from "../Components/DashboardCard/DashboardCard";
import './CSS/UserHomePage.css'

export const UserHomePage = () => {
    return(
        <div className="user-homepage">
            <h1>Welcome to your User Dashboard</h1>
            <div className="user-homepage-cards-container">
                <Link to="/dashboard" className="user-homepage-card">
                <DashboardCard 
                    title = "Request Delivery" 
                    description = "Start a new delivery request here"/>
                </Link>
                <Link to="/viewDeliveryRequest" className="user-homepage-card">
                    <DashboardCard 
                        title = "View Delivery Requests" 
                        description = "View your pending delivery requests"/>
                </Link>
                {/* <Link to="/payDeliveryRequest" className="user-homepage-card">
                    <DashboardCard 
                        title = "Pay Delivery Requests" 
                        description = "Pay for a delivery requests you already made"/>
                </Link> */}
                <Link to="/viewOrders" className="user-homepage-card">
                    <DashboardCard 
                        title = "View Orders" 
                        description = "View your orders you've already payed for"/>
                </Link>
                <Link to="/trackOrders" className="user-homepage-card">
                    <DashboardCard 
                        title = "Track Orders" 
                        description = "View the status of ongoing Orders here"/>
                </Link>

                <Link to="/viewPayments" className="user-homepage-card">
                    <DashboardCard 
                        title = "View Payments" 
                        description = "View all your payments here"/>
                </Link>

                {/* <Link to="/cancelDeliveryRequest"><DashboardCard title = "Cancel Delivery Requests" description = "Cancel your delivery requests here"/></Link> */}

            </div>
        </div>
    );

}