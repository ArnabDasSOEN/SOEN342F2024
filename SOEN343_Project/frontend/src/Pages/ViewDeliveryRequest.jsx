import { useEffect } from "react";
import axios from "axios";

export const ViewDeliveryRequest = () => {

    useEffect(() => {
        //  /delivery_request/view_delivery_requests
        async function ViewDeliveries(){
            try{
                const user_id = parseInt(localStorage.getItem("user_id"))
                const data = {user_id}
                console.log(data);
                const response = await axios.post("http://localhost:5000/delivery_request/view_delivery_requests", data )
                console.log(response);
            }catch (err){
                console.log("Got an error viewing requests", err)
            }
        }
        ViewDeliveries();


      }, []); //empty dependency implies tha tthe compoenent only rnders after initial rerender. aka, each time user clicks view deliveries, this will trigger a request and no more.
    



    

    return (
        <main>
            <h1>Pending delivery Request</h1>
            <h2>Implement cancel as well from this</h2>
        </main>
    );
}