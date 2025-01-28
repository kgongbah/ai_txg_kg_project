import React, { useContext } from "react";
import { AuthContext } from "./../context/AuthContext";
import ChatInterface from "./ChatInterface";
import "./../styles/Home.css";

const HomePage = () => {
    const { user, logout } = useContext(AuthContext);
  
    return (
      <div>
        <header className="top-bar">
          <h1>Recipe Generator</h1>
          <div className="top-bar-actions">
            {user ? (
              <>
                <span className="welcome-message">Hi, {user.username}!</span>
                <button className="profile-button" onClick={() => (window.location.href = "/profile")}>
                  Profile
                </button>
                <button className="logout-button" onClick={logout}>
                  Logout
                </button>
              </>
            ) : (
              <button onClick={() => (window.location.href = "/login-signup")}>
                Login / Signup
              </button>
            )}
          </div>
        </header>
        <main className="main-content">
            {user ? (
                <ChatInterface />
            ) : (
                <p>Please login or signup to start creating recipes.</p>
            )}
        </main>
      </div>
    );
  };
  
  export default HomePage;