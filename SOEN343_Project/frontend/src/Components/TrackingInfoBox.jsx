export const TrackingInfoBox = ({message, status}) => {
    //this is just a dummy component to display information.
    //uses pure fabrication design pattern

    return (
        <div>
            <h3>STATUS: {status}</h3>
            <h4>{message}</h4>
        </div>
    )
}