import { useState, useEffect } from "react";
//import axios from "axios";
//import { PaymentForm } from "../Components/PaymentForm";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

//our Key values
const SQUAREUP_APPLICATION_ID = process.env.REACT_APP_SQUAREUP_APPLICATION_ID;
const SQUAREUP_LOCATION_ID = process.env.REACT_APP_SQUAREUP_LOCATION_ID;

export const PayDeliveryRequest = () => {

  const [paymentID, setPaymentID] = useState(null)
  const onIDChange = (e) => {
    const { value } = e.target;
    setPaymentID(value);
  }

  const [paymentForm, setPaymentForm] = useState("");

  // Initialize the Square Payment Form
  useEffect(() => {
    // We"re handling this error in case yall didn"t download the SDK. Run "npm i square" if you didn"t already
    if (!window.Square) {
      console.error('Square Web Payments SDK not loaded');
      return;
    }

    const initializePaymentForm = async () => {
      //we start by setting up the actual payment. This is the token that gets sent to the backend. Read more abty this here: https://developer.squareup.com/docs/web-payments/take-card-payment
      const payments = window.Square.payments(SQUAREUP_APPLICATION_ID, SQUAREUP_LOCATION_ID);
      const card = await payments.card();// Cwe need to creat the card payment thing before we do anything. 
      await card.attach('#card-container'); // attaching directly to the DOM is discouraged but in this case we got to do it. DW tho, this only loads when the file gets loaded.
      //just a note, in the above code, were attaching the card to the div returned in this component. SO althought were "directly manipulating the DOM" when we change pages, react
      //unmounts everything that it added from this component.
      setPaymentForm({ payments, card });// Store the payment form state (basically create the form and set it aside for now)
    };
    initializePaymentForm(); //create the form
  }, []);//empty array ensures this gets created everytime this component loads.

  // Handle Payment Submission
  const handlePayment = async (e) => {
    e.preventDefault();
    if (!paymentForm) return; //handling this error just in case there is no form

    try {
      // create a token out of the payment and send it to the backend. I believe thtis uses Oauth but im not sure. Check square up documentation on how to take web payments for more info
      const result = await paymentForm.card.tokenize();
      if (result.status === 'OK') {
        console.log('Token:', result.token);
        toast.success("Payment successful. Tokenizing")

        // This is where we send "result.token" to the backend to log the payment. Remeber that were using a sandbox
        try{

        } catch (e) {
          //axios.post("/payment/make_payment") // , + data in a object
        }


      } else {
        console.error('Tokenization failed:', result);
        toast.error("Payment failed. Cannot tokenize")
      }
    } catch (error) {
      console.error('Error processing payment:', error);
      toast.error("error processing payment")
    }
  };


  return (
    <main>
      <h1>Pay a delivery request</h1>
      <ToastContainer />
      <form action="POST" onSubmit={handlePayment}>
        <label>
          <input type="number" value={paymentID} onChange={onIDChange} placeholder="ID of your delivery request"></input>
        </label>

        <div className="PaymentForm">
          <h2>Payment Form</h2>
            {/* This div is where the Square card input will render */}
            <div id="card-container"></div>
        </div>
        <button type="submit" disabled={!paymentForm}>Pay Now</button>
      </form>

    </main>
  );
}


//1st attach the payment form once
//send the token to backend