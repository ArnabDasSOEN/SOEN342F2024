


export const PaymentBox = ({amount, order_id, payment_date, payment_id, status}) => {




    return (
        <div>
            <p>Order ID: {order_id}</p>
            <p>amount: {amount}</p>
            <p>Date of transaction: {payment_date}</p>
            <p>payment ID: {payment_id}</p>
            <p>Payment status: {status}</p>
        </div>
    );
}