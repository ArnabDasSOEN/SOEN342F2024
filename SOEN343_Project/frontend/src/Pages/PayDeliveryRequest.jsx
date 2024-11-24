import { useState, useEffect } from "react";
import axios from "axios";
//const { Client, Environment, ApiError } = require("square");
//import { Client, Environment, ApiError } from "square"


export const PayDeliveryRequest = () => {

  const SQUARE_APPLICATION_ID = 123; // get these tokens from Roberto and add hem to the .env file
  const SQUARE_LOCATION_ID = 123;


  // /payment/make_payment
  const [paymentID, setPaymentID] = useState(null)

  const onIDChange = (e) => {
    const { value } = e.target;
    setPaymentID(value);
    //console.log(paymentID)
  }

  const handleFormSubmission = e => {
      e.preventDefault()

      try{
          //axios.post("/payment/make_payment") // , + data in a object
      }catch (e) {

      }
  }

  const [paymentForm, setPaymentForm] = useState(null);

  // useEffect( () => {
  //   //create the client, maybe ill put this in the useEffect block for everytime this page loads? idk. actually ye imma do that
  //   const client = new Client({
  //     bearerAuthCredentials: {
  //       accessToken: process.env.SQUARE_ACCESS_TOKEN
  //     },
  //     environment: Environment.Sandbox,
  //   });
  //   const { locationsApi } = client;

  //   async function getLocations() {
  //     try {
  //       let listLocationsResponse = await locationsApi.listLocations();

  //       let locations = listLocationsResponse.result.locations;

  //       locations.forEach(function (location) {
  //         console.log(
  //           location.id + ": " +
  //           location.name + ", " +
  //           location.address.addressLine1 + ", " +
  //           location.address.locality
  //         );
  //       });
  //     } catch (error) {
  //       if (error instanceof ApiError) {
  //         error.result.errors.forEach(function (e) {
  //           console.log(e.category);
  //           console.log(e.code);
  //           console.log(e.detail);
  //         });
  //       } else {
  //         console.log("Unexpected error occurred: ", error);
  //       }
  //     }
  //   };

  //   getLocations();



  //   //in the documentation, https://developer.squareup.com/docs/payments-api/take-payments. It says every seller has a locaion. so im guessing i need 3 API keys actually?
  //   //if we don"t, ill delete everything that was written previously. Just don"t touch it for now.
    

  //   // We"re handling this error in case yall didn"t download the SDK. Run "npm i square" if you didn"t already
  //   if (!window.Square) {
  //     console.error("Square Web Payments SDK not loaded");
  //     return;
  //   }
  //   //Since we only care about the actual form to send the data to the backend, we just got to render it
  //   const initializePaymentForm = async () => {
  //     const payments = window.Square.payments(SQUARE_APPLICATION_ID, SQUARE_LOCATION_ID);
  //     // Create a card instance
  //     const card = await payments.card();
  //     await card.attach("#card-container"); //this attaches it to the DOM. idk how necesasry this is
  //     //btw tahsin, the argument passed inside is the ID of the component if you want to do some CSS with it.
  //     // an object that represents the form with the payments and card.
  //     setPaymentForm({ payments, card });
  //   };
  //   initializePaymentForm();


  //   const handlePayment = async (event) => {
  //     event.preventDefault();

  //     if (!paymentForm) return;

  //     try {
  //       // Tokenize card details
  //       const result = await paymentForm.card.tokenize();
  //       if (result.status === "OK") {
  //         // You now have a payment token that can be sent to your backend to process the payment
  //         console.log("Payment token:", result.token);

  //         // Implement the logic to send this token to your backend for processing
  //         console.log("Payment worked (finally)");
  //       } else {
  //         console.error("Tokenization failed:", result);
  //       }
  //     } catch (error) {
  //       console.error("Error processing payment:", error);
  //     }
  //   };



  // }, [])









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