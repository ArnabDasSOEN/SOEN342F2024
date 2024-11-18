import { Link, useNavigate } from "react-router-dom";


export const UserHomePage = () => {
    const navigate = useNavigate();

return(
    <main>
        <h1>UserHomePage</h1>
        <button onClick={navigate("/dashboard")}></button>
        <Link to="/dashboard" >Hello senior (Carlo butt cheeks)</Link>
    </main>
);

}