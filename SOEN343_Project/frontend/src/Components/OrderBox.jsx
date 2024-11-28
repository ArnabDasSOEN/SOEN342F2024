export const OrderBox = ({order_id, status, delivery_agent_id, delivery_request}) => {
    const {pick_up_address, drop_off_address } = delivery_request
    
    return (
        <div>
            <p>ORDER ID: {order_id}</p>
            <p>STATUS: {status}</p>
            <p>delivery agent ID: {delivery_agent_id}</p>
            
            <h4>Pick up address</h4>
            <p>city: {pick_up_address.city}</p>
            <p>country: {pick_up_address.country}</p>
            <p>house number: {pick_up_address.house_number}</p>
            <p>street: {pick_up_address.street}</p>
            
            
            <h4>Drop Off address</h4>
            <p>city: {drop_off_address.city}</p>
            <p>country: {drop_off_address.country}</p>
            <p>house number: {drop_off_address.house_number}</p>
            <p>street: {drop_off_address.street}</p>
    
            
        </div>
    )
}