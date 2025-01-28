import React, { useState } from "react";
import api from "./../services/api";
import "./../styles/LoginSignup.css";
import axios from "axios";

const LoginSignup = () => {
  const [isLogin, setIsLogin] = useState(true); // Toggle between login and signup
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        console.log("hi1")
      if (isLogin) {
        // Login logic
        const response = await fetch("http://localhost:80/users/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                username: formData.username,
                password: formData.password,
            }),
        });
        console.log("hewo")

        // Handle successful login (e.g., store token in localStorage)
        if (response.ok) {
            const data = await response.json(); //For some reason data only gives us the user_id
            const logged_in_user = await fetch(`http://localhost:80/users/${data.user_id}`); //Get the username and other info
            const logged_user_data = await logged_in_user.json();
            localStorage.setItem("user_id", logged_user_data.user_id);
            localStorage.setItem("username", logged_user_data.username); // Optional, for greeting
            
            setMessage("Login successful!");
            console.log("User logged in:", logged_user_data);
            window.location.href = "/"; // Redirect to homepage
          } 
        else {
            const errorData = await response.json();
            setMessage(errorData.message || "Login failed. Please try again.");
        };
      } else {
        // Signup logic
        const response = await fetch("http://localhost:80/users/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: formData.username,
                email: formData.email,
                password: formData.password,
            }),
        });
        setMessage("Signup successful! Please log in.");
        console.log("User signed up:", response.data);
        setIsLogin(true); // Switch to login after signup
      }
    } catch (error) {
      setMessage(error.response?.data?.detail || "An error occurred.");
    }
  };

  return (
    <div className="login-signup-container">
      <h2>{isLogin ? "Login" : "Signup"}</h2>
      <form onSubmit={handleSubmit}>
        {!isLogin && (
          <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        )}
        <div>
            <label htmlFor="username">Username:</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required={!isLogin}
            />
          </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">{isLogin ? "Login" : "Signup"}</button>
      </form>
      {message && <p className="message">{message}</p>}
      <button onClick={() => setIsLogin(!isLogin)}>
        {isLogin ? "Need an account? Sign up" : "Already have an account? Log in"}
      </button>
    </div>
  );
};

export default LoginSignup;
