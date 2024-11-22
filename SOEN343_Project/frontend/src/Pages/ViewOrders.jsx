import { useEffect } from "react";
import axios from "axios"

export const ViewOrders = () => {

    useEffect(() => {
        async function ViewOrders(){
            try{
                const user_id = parseInt(localStorage.getItem("user_id"))
                const data = {user_id}
                const response = await axios.post("http://localhost:5000/get_orders_by_user", data )
                console.log(response);
            }catch (err){
                console.log("Got an error viewing requests", err)
            }
        }
        ViewOrders();
      }, []);






    return (
        <main>
            <h1>{localStorage.getItem("username")}'s orders</h1>
        </main>
    )
}