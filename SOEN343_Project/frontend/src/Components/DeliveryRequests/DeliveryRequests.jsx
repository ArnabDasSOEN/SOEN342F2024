import { PayDeliveryRequest } from "../../Pages/PayDeliveryRequest";
import { useState } from "react"
import axios from "axios";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './DeliveryRequests.css'

export const DeliveryRequest = ({ id, status, pickUp, dropOff }) => {

    //pickUp and dropOff are objects that contain the following attributes: city country house_number street

    const [wantToPay, setWantToPay] = useState(false)

    const handleWantToPay = (e) => {
        setWantToPay(!wantToPay);
    }

    const handleCancelDeliveryRequest = async e => {
        e.preventDefault()
        try {
            const data = {
                delivery_request_id: id
            }
            const response = await axios.post("http://localhost:5000/delivery_request/cancel_delivery_request", data)
            console.log(response)
            toast.success("Succesfully cancelled request")

            window.location.reload()
            
        } catch (e) {
            console.log("error cancelling delivery request", e)
            toast.error("error cancelling delivery request")
        }

    }



    return (
        <div className="delivery-request-container">
            <ToastContainer />
            <span>{id}</span>
            <h6>Pick up location</h6>
            <div>
                <span>{pickUp.city}</span>
                <span>{pickUp.country}</span>
                <span>{pickUp.house_number}</span>
                <span>{pickUp.street}</span>
            </div>
            <h6>Drop off location</h6>
            <div>
                <span>{dropOff.city}</span>
                <span>{dropOff.country}</span>
                <span>{dropOff.house_number}</span>
                <span>{dropOff.street}</span>
            </div>
            <span className={`status ${status.toLowerCase()}`}>{status}</span>
            <button onClick={handleWantToPay}>Pay Now</button>

            {/* {wantToPay ? <PayDeliveryRequest id={id} /> : null} */}
            
            {
                wantToPay
                    ? (
                        status !== "Cancelled" ?<div className="pay-delivery-container"> <PayDeliveryRequest id={id} /> </div>: null
                    )
                    : null
            }

            {status === "Cancelled" ? null : <button type="button" className="cancel-button" onClick={handleCancelDeliveryRequest} >cancel delivery request</button>}




        </div>
    );
}