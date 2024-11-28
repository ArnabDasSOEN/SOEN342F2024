import { useEffect, useState } from "react";
import axios from "axios"
import { OrderBox } from "../Components/OrderBox";

export const ViewOrders = () => {


    const [orders, setOrders] = useState(null)


    useEffect(() => {
        
        const ViewOrders = async () => {
            try{
                const user_id = parseInt(localStorage.getItem("user_id"))
                //user_id = parseInt(user_id)
                const data = {user_id}
                const response = await axios.post("http://localhost:5000/order/get_orders_by_user",data)
                //console.log(response.data);

                setOrders(
                    response.data.map( el => (
                        <OrderBox key={el.order_id} order_id={el.order_id}  status={el.status} delivery_agent_id={el.delivery_agent_id} delivery_request={el.delivery_request} />
                    ))
                )



            }catch (err){
                console.log("Got an error viewing requests", err)
            }
        }
        ViewOrders();
      }, []);



    return (
        <main>
            <h1>{localStorage.getItem("username")}'s orders</h1>
            {orders}

        </main>
    )
}