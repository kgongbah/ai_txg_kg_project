import React, { useState } from "react";
import "./../styles/LoginSignup.css";

const LoginSignup = () => {
  const [isLogin, setIsLogin] = useState(true); // Toggle between login and signup
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [message, setMessage] = useState("");

  //Backend API
  const api = "http://localhost:8000";

  //This formatting is a bit weird, but in the HTML, any input that is submitted (ie email, username, or password)
  //has a name and value property. e.target refers to the entire input field. name refers to either email, username,
  //or password. value is the value of the name, ie name = email, value = kg@gmail.com
  const handleChange = (e) => {
    const { name, value } = e.target;
    //Above line is equivalent to:
    //const name = e.target.name;
    //const value = e.target.value;
    setFormData({ 
      ...formData, //Keeps unedited portion of form
      [name]: value, //Updates edited value of the form
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); //Prevents page refresh when form is submitted.

    try {
      if (isLogin) {
        // Login logic
        const response = await fetch(`${api}/users/login`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                username: formData.username,
                password: formData.password,
            }),
        });

        // Handle successful login (e.g., store token in localStorage)
        if (response.ok) {
            const data = await response.json(); //For some reason data only gives us the user_id
            const logged_in_user = await fetch(`${api}/users/${data.user_id}`); //Get the username and other info
            const logged_user_data = await logged_in_user.json();

            //localStorage is 
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
        const response = await fetch(`${api}/users/`, {
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

  //Note: whenever any of the forms are changed, the onChange property calls handleChange
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
