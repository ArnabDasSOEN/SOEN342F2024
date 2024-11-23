import { useState } from "react";
import axios from "axios";


export const PayDeliveryRequest = () => {

    // /payment/make_payment
    // /payment/make_payment
    const [paymentID, setPaymentID] = useState(null)

     const onIDChange = (e) => {
        const {value} = e.target;
        setPaymentID(value);
        //console.log(paymentID)
     }

    const handleFormSubmission = e => {
        e.preventDefault()
        
        try{
            axios.post("")
        }catch (e) {

        }
    }


    //
    const { Client, Environment, ApiError } = require("square");

    const client = new Client({
        bearerAuthCredentials: {
          accessToken: process.env.SQUARE_ACCESS_TOKEN
        },
      environment: Environment.Sandbox,
    });
    
    const { locationsApi } = client;
    
    async function getLocations() {
      try {
        let listLocationsResponse = await locationsApi.listLocations();
    
        let locations = listLocationsResponse.result.locations;
    
        locations.forEach(function (location) {
          console.log(
            location.id + ": " +
              location.name +", " +
              location.address.addressLine1 + ", " +
              location.address.locality
          );
        });
      } catch (error) {
        if (error instanceof ApiError) {
          error.result.errors.forEach(function (e) {
            console.log(e.category);
            console.log(e.code);
            console.log(e.detail);
          });
        } else {
          console.log("Unexpected error occurred: ", error);
        }
      }
    };
    
    getLocations();
    

    

    //
    return (
        <main>
            <h1>Pay a delivery request</h1>

            <form action="POST" onSubmit={handleFormSubmission}>
                <label>
                    <input type="number" value={paymentID} onChange={onIDChange} placeholder="ID of your delivery request"></input>
                </label>

                <label>
                    payment method:
                    <select name="payment_method">
                    
                    <option value="" disabled>Select an option</option>
                    <option value="Debit (VISA)">Debit (VISA)</option>
                    <option value="Credit (Master Card)">Credit (Master Card)</option>
                    <option value="Credit (VISA)">Credit (VISA)</option>
                    
                    </select>
                   
                </label>


                <button type="submit">Pay delivery request</button>
            </form>

        </main>
    );
}