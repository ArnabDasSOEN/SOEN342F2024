//import { PayDeliveryRequest } from "../../Pages/PayDeliveryRequest";
//import { useState } from "react"
import axios from "axios";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
//import './DeliveryRequests.css'
import { useNavigate } from "react-router-dom";

export const DeliveryRequest = ({ id, status, pickUp, dropOff, quotation }) => {
    const navigate = useNavigate();

    //const [wantToPay, setWantToPay] = useState(false)

    // const handleWantToPay = (e) => {
    //     setWantToPay(!wantToPay);
    // }

    const handleWantToPay = (e) => {
        navigate("/payDeliveryRequest", { state: { id, quotation } })
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
            <span>Quotation: ${quotation}</span>
            <span className={`status ${status.toLowerCase()}`}>{status}</span>
            {/* <button onClick={handleWantToPay}>Want to pay now?</button> */}

            {/* { status === "Paid" ? null: <button onClick={handleWantToPay}>Want to pay now?</button>} */}

            {/* {wantToPay ? <PayDeliveryRequest id={id} /> : null} */}



            {/* {
                status !== "Paid" ? (
                    status !== "Cancelled" ? <button onClick={handleWantToPay}>Want to pay now?</button> : null
                ) : null
            } */}

            {
                status !== "Paid" ? (
                    status !== "Cancelled" ? (
                        <>
                            <button onClick={handleWantToPay}>Want to pay now?</button>
                            <button type="button" onClick={handleCancelDeliveryRequest}> Cancel Delivery Request </button>
                        </>
                    ) : null
                ) : null
            }


            {/* {
                wantToPay
                    ? (
                        status !== "Cancelled" ?  <PayDeliveryRequest id={id} /> : null
                    )
                    : null
            } */}


            {/* Can touch CSS for this*/}
            {/* {
                status !== "Cancelled" ? (
                    <button type="button" onClick={handleCancelDeliveryRequest}> cancel delivery request </button>
                ) : null

            } */}

        </div>
    );
}