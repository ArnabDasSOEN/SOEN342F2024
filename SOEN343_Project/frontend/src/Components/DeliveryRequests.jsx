import { PayDeliveryRequest } from "../Pages/PayDeliveryRequest";
import { useState} from "react"

export const DeliveryRequest = ({id, status, pickUp, dropOff}) => {

    //pickUp and dropOff are objects that contain the following attributes: city country house_number street

    const [wantToPay, setWantToPay] = useState(false)

    const handleWantToPay = (e) => {
        setWantToPay(!wantToPay);
    }

    return (
        <div>
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
            
            <span>{status}</span> 

            <button onClick={handleWantToPay}>pay now bozo</button>
            
            {wantToPay ? <PayDeliveryRequest id={id} /> : null}

            {/* <div id={`#D${id}card-container`}></div> */}
        </div>
    );
}