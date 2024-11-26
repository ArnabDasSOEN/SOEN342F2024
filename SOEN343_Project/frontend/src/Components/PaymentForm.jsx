import {useState, useEffect} from "react"
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


const SQUARE_APPLICATION_ID = process.env.SQUAREUP_APPLICATION_ID; 
const SQUARE_LOCATION_ID = process.env.SQUAREUP_LOCATION_ID;



export const PaymentForm = () => {

    const [paymentForm, setPaymentForm] = useState(null);

    // Initialize the Square Payment Form
     useEffect(() => {
    // We"re handling this error in case yall didn"t download the SDK. Run "npm i square" if you didn"t already
    if (!window.Square) {
      console.error('Square Web Payments SDK not loaded');
      return;
    }

    const initializePaymentForm = async () => {
      //we start by setting up the actual payment. This is the token that gets sent to the backend. Read more abty this here: https://developer.squareup.com/docs/web-payments/take-card-payment
      const payments = window.Square.payments(SQUARE_APPLICATION_ID, SQUARE_LOCATION_ID);
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

    if (!paymentForm) return; //handling this error just in case

    try {
      // create a token out of the payment and send it to the backend. I believe thtis uses Oauth but im not sure. Check square up documentation on how to take web payments for more info
      const result = await paymentForm.card.tokenize();
      if (result.status === 'OK') {
        // This is where we send "result.token" to the backend to log the payment. Remeber that were using a sandbox
        console.log('Token:', result.token);
        toast.success("Payment successful. Tokenizing")
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
    <div>
      <h2>Payment Form</h2>
      <ToastContainer />
      <form onSubmit={handlePayment}>
        {/* This div is where the Square card input will render */}
        <div id="card-container"></div>
        <button type="submit" disabled={!paymentForm}>Pay Now</button>
      </form>
    </div>
  );
}

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







  /* <label>
    payment method:
    <select name="payment_method">

      <option value="" disabled>Select an option</option>
      <option value="Debit (VISA)">Debit (VISA)</option>
      <option value="Credit (Master Card)">Credit (Master Card)</option>
      <option value="Credit (VISA)">Credit (VISA)</option>

    </select>

  </label> */