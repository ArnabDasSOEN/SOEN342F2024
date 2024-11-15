import { useNavigate } from "react-router-dom";
import { useState } from "react";

export const Logout = () => {
    localStorage.removeItem('username');
    localStorage.removeItem('user_id');
    const navigate = useNavigate();
    const [timer, setTimer] = useState(3);

    const intervalId = setInterval(() => {
        if (timer === 1) {
            clearInterval(intervalId); // Stop the interval
            navigate("/login");
        }
        setTimer(timer - 1);
    }, 1000);

    return(
        <main>
            <h1>Succesfully logged out!</h1>
            <h2>Redirecting in {timer}</h2>
        </main>
    )
}