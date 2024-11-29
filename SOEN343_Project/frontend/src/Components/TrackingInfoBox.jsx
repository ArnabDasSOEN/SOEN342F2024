export const TrackingInfoBox = ({message, status, estimated_delivery_time}) => {
    //this is just a dummy component to display information.
    //uses pure fabrication design pattern

    return (
        <div>
            <h3>STATUS: {status}</h3>
            <h4>{message}</h4>
            {typeof estimated_delivery_time !== "undefined" ? <h5>ETA: {estimated_delivery_time}</h5> : null}
            
        </div>
    )
}