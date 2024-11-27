import {  useState, useEffect } from "react"
import axios from "axios"
import { PaymentBox } from "../Components/PaymentBox"

export const ViewPayments = () => {
    
    const [payments, setPayments] = useState(null);

    useEffect( () => {

        const getPayments = async () => {
        try{
            const user_id = +localStorage.getItem("user_id")
            //user_id = +user_id
            const requestData = {
                user_id
            }
            const response = await axios.post("http://localhost:5000/payment/payment_history", requestData)
            console.log(response.data)
            setPayments(
                response.data.map( el => (<PaymentBox key={el.order_id} amount={el.amount} order_id={el.order_id} payment_date={el.payment_date} payment_id={el.payment_id} status={el.status}/>))
            )

            //console.log(response.data)
        } catch (e) {
            console.log("error viewing payments", e)
        }
        }
        getPayments();

    }, [])




    return(
        <main>
            <h1>Payments made</h1>
            {payments}

        </main>
    )

}