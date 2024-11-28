import './OrderBox.css';

export const OrderBox = ({ order_id, status, delivery_agent_id, delivery_request }) => {
    const { pick_up_address, drop_off_address } = delivery_request;

    return (
        <div className="order-box">
            <p className="order-id">ORDER ID: {order_id}</p>
            <p className={`status ${status.toLowerCase()}`}>STATUS: {status}</p>
            <p>Delivery Agent ID: {delivery_agent_id}</p>

            <div className="address">
                <h4>Pick Up Address</h4>
                <p>City: {pick_up_address.city}</p>
                <p>Country: {pick_up_address.country}</p>
                <p>House Number: {pick_up_address.house_number}</p>
                <p>Street: {pick_up_address.street}</p>
            </div>

            <div className="address">
                <h4>Drop Off Address</h4>
                <p>City: {drop_off_address.city}</p>
                <p>Country: {drop_off_address.country}</p>
                <p>House Number: {drop_off_address.house_number}</p>
                <p>Street: {drop_off_address.street}</p>
            </div>
        </div>
    );
};
