import { useState } from "react";
import axios from "axios";
import { TrackingInfoBox } from "../Components/TrackingInfoBox/TrackingInfoBox.jsx";
import './CSS/TrackOrders.css'

export const TrackOrders = () => {

    const [orderId, setOrderId] = useState(0);

    const handleOrderIdChange = (e) => {
        setOrderId(e.target.value);
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const data = { order_id: orderId };
            const response = await axios.post("http://localhost:5000/delivery_agent/track", data);
            console.log(response.data);
            const { message, status, estimated_delivery_time } = response.data;
            setTrackingInfo(
                <TrackingInfoBox message={message} status={status} estimated_delivery_time={estimated_delivery_time} />
            );
        } catch (e) {
            setTrackingInfo(
                <TrackingInfoBox message="INVALID ORDER" status="INVALID ORDER" />
            );
        }
    }

    const [trackingInfo, setTrackingInfo] = useState(null);

    return (
        <main className="track-orders">
            <h1>Tracking Delivery</h1>
            <h2>Enter Order ID:</h2>
            <form onSubmit={handleSubmit} method="POST">
                <input
                    className="order-id-input"
                    type="number"
                    name="order_id"
                    value={orderId}
                    onChange={handleOrderIdChange} />
                <button className="track-button" type="submit">Track</button>
            </form>
            {trackingInfo && <div className="tracking-info">{trackingInfo}</div>}
        </main>
    );
}
