import React, { useState } from "react";
import "./CSS/SignUp.css";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

export const SignUp = () => {
  const [formData, setFormData] = useState({
    name: "",
    phone_number: "",
    email: "",
    password: "",
    confirm_password: "",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (formData.password !== formData.confirm_password) {
      setError("Passwords do not match");
      return;
    }

    try {
      const response = await axios.post(
        "http://localhost:5000/auth/sign_up",
        {
          name: formData.name,
          phone_number: formData.phone_number,
          email: formData.email,
          password: formData.password,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      alert(response.data.message);
      navigate("/login"); // Redirect to login page after successful signup
    } catch (err) {
      // Check if the error has a response
      setError(err.response?.data?.error || "An error occurred");
    }
  };

  return (
    <div className="signup">
      <h2>Sign Up</h2>
      <form className="signup-page" onSubmit={handleSubmit}>
        <label htmlFor="name">Name</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <br />
        <label htmlFor="phone_number">Phone Number</label>
        <input
          type="tel"
          name="phone_number"
          value={formData.phone_number}
          onChange={handleChange}
          required
        />
        <br />
        <label className="email">Email Address</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <br />
        <label htmlFor="password">Password</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <br />
        <label htmlFor="confirm_password">Confirm Password</label>
        <input
          type="password"
          name="confirm_password"
          value={formData.confirm_password}
          onChange={handleChange}
          required
        />
        <br />
        {error && <p className="error-message">{error}</p>}
        <button type="submit">Continue</button>
      </form>
      <p className="loginsignup-login">
        Already have an account?{" "}
        <Link to="/login" className="login-link">
          Login here
        </Link>
      </p>
      <div className="signup-agree">
        <input type="checkbox" required />
        <p>By continuing, I agree to the terms of use & privacy policy</p>
      </div>
    </div>
  );
};
