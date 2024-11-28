import { useState } from "react";
import axios from "axios"
import {TrackingInfoBox} from "../Components/TrackingInfoBox.jsx";

export const TrackOrders = () => {

    const [orderId, setOrderId] = useState(0)

    const handleOrderIdChange = (e) => {
        setOrderId(e.target.value)
    }

    const handleSubmit = async e => {
        e.preventDefault()
        try{
        const data = {order_id: orderId}
        const response = await axios.post("http://localhost:5000/delivery_agent/track", data)
        const { message, status} = response.data
        setTrackingInfo(<TrackingInfoBox message={message} status={status}/>)
        } catch (e){
            setTrackingInfo(<TrackingInfoBox message="INVALID ORDER" status="INVALID ORDER"/>)
        }

    }


    const [trackingInfo, setTrackingInfo] = useState(null)



    return (
        <main>
            <h1>Tracking 1 delivery</h1>
            <h2>Enter order id:</h2>
            <form onSubmit={handleSubmit} method="POST">
                <input
                    type="number"
                    name="order_id"
                    value={orderId}
                    onChange={handleOrderIdChange} />
                <button type="submit">Track</button>
            </form>

            {trackingInfo}



        </main>
    );
}