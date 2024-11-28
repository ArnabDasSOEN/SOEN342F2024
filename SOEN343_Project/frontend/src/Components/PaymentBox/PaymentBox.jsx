import './PaymentBox.css'
export const PaymentBox = ({ amount, order_id, payment_date, payment_id, status }) => {
    return (
        <div className="payment-box">
            <div className="payment-details">
                <div><span className="label">Order ID:</span> <span className="value">{order_id}</span></div>
                <div><span className="label">Amount:</span> <span className="value">{amount}</span></div>
                <div><span className="label">Payment Date:</span> <span className="value">{payment_date}</span></div>
                <div><span className="label">Payment ID:</span> <span className="value">{payment_id}</span></div>
                <div><span className="label">Payment Status: </span> 
                    <span className={`status ${status.toLowerCase()}`}>{status}</span>
                </div>
            </div>
        </div>
    );
};
