import React, { useState } from "react";
import "./CSS/Login.css";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import facebook_logo from "../Components/Assets/Facebook.png";
import google_logo from "../Components/Assets/Google.png";
import twitter_logo from "../Components/Assets/TwitterX.png";
import apple_logo from "../Components/Assets/Apple Logo.png";
import amazon_logo from "../Components/Assets/Amazon.png";

export const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); // Clear previous errors

    try {
      const response = await axios.post(
        "http://localhost:5000/auth/login",
        {
          email,
          password,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      // Handle successful login (e.g., redirect or save token)
      //console.log(response.data);
      localStorage.setItem("username", response.data.username);
      localStorage.setItem("user_id", response.data.user_id);
      //console.log("logged user is: ", localStorage.getItem("username"));

      navigate("/dashboard"); // Redirect to a dashboard or home page on success
    } catch (err) {
      setError(err.response?.data?.error || "An error occurred during login.");
    }
  };

  return (
    <div className="loginPage">
      <h2>Log In</h2>
      <form className="loginForm" onSubmit={handleSubmit}>
        <label>Email or Username</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required/>
        <br />
        <label>Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required/>
        <br />
        {error && <p className="error-message">{error}</p>}
        <button type="submit" className="loginButton">Login</button>
      </form>
      <div className="otherLoginOptions">
        <p>
          <span>Or with</span>
        </p>
      </div>
      <div className="company-logos">
        <img src={google_logo} alt="Google" className="google" />
        <img src={facebook_logo} alt="Facebook" className="facebook" />
        <img src={twitter_logo} alt="Twitter" className="twitter" />
        <img src={apple_logo} alt="Apple" className="apple" />
        <img src={amazon_logo} alt="Amazon" className="amazon" />
      </div>
      <p className="signup-from-login">
        Don't have an account?{" "}
        <Link to="/signup" className="signup-link"> Sign up here </Link>
      </p>
    </div>
  );
};
