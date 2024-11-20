import { useState } from "react";

export const TrackOrders = () => {

    const [orderId, setOrderId] = useState(0)

    const handleOrderIdChange = (e) => {
        setOrderId(e.target.value)
    }

    const handleSubmit = e => {
        e.preventDefault()

    }

    return (
        <main>
            <h1>Tracking 1 delivery</h1>
            <h2>Enter order id:</h2>
            <form onSubmit={handleSubmit} method="POST">
                <input
                    type="number"
                    name="order_id"
                    value={orderId}
                    onChange={handleOrderIdChange} />
                <button type="submit">Track</button>
            </form>
        </main>
    );
}