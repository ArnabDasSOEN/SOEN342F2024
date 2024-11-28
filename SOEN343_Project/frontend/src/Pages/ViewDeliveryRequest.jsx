import { useEffect, useState } from "react";
import axios from "axios";
import { DeliveryRequest } from "../Components/DeliveryRequests/DeliveryRequests";
//import { PayDeliveryRequest } from "./PayDeliveryRequest";
import './CSS/ViewDeliveryRequest.css'

export const ViewDeliveryRequest = () => {

    const [requests, setRequests] = useState([]);
    useEffect(() => {
        //  /delivery_request/view_delivery_requests
        async function ViewDeliveries(){
            try{
                const user_id = parseInt(localStorage.getItem("user_id"))
                const data = {user_id}
                //console.log(data);
                const response = await axios.post("http://localhost:5000/delivery_request/view_delivery_requests", data )
                //console.log(response.data);

                setRequests(response.data.map( item => {
                    return <DeliveryRequest key={item.delivery_request_id} id={item.delivery_request_id} status={item.status} pickUp={item.pick_up_address} dropOff={item.drop_off_address} />
                }))


            }catch (err){
                console.log("Got an error viewing requests", err)
            }
        }
        ViewDeliveries();
      }, []); //empty dependency implies tha tthe compoenent only rnders after initial rerender. aka, each time user clicks view deliveries, this will trigger a request and no more.
    

    return (
        <div className="view-delivery-request">
            <h1>Pending Delivery Request</h1>
            <h2>Implement cancel as well from this</h2>
            <div className="view-delivery-request-container">
                {requests}
            </div>
        </div>
    );
}