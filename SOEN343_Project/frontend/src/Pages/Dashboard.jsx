import { Link } from "react-router-dom";

export const Dashboard = () => {


    const handleSubmitForm = (e) => {
        e.preventDefault();

        const formData = new FormData(e.target);
        const formObject = Object.fromEntries(formData.entries()); //data to send to axios post requst to "/create_delivery_request"
    }





    return(
        <main className="Dashboard">
            <h1>Dashboard</h1>

            <h2>make request for delivery</h2>
            <form action="/create_delivery_request" method="POST" onSubmit={handleSubmitForm}>
                <label>pick up address   </label>
                <input type="text" ></input>
                <br/>
                <label>drop off address   </label>
                <input type="text" ></input>
                <br/>
                <label>package data   </label>
                <p>length - width - height</p>
                <p>checkboxes ;)</p>
                <input type="checkbox"></input>
                <input type="checkbox"></input>
                <input type="checkbox"></input>
                <button type="submit">submit delivery request</button>
            </form>




            <Link to="/logout" className="logout">logout</Link>
        </main>
    )
}