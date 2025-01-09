import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./../styles/Home.css";

const Home = () => {
    const [isSignedIn, setIsSignedIn] = useState(false);
    //temporarily lock userState as not signed in

    const Header = () => (
        <header>
            <h1>Recipe Generator</h1>
            <Link to="/login-signup">
                <button className="login-signup-button">Log-in or Sign-up</button>
            </Link>
        </header>
    ); //alert is temporary route for our login

    const NotSignedInContent = () => (
        <div className = "body">
            <p>Please log-in or sign-up to start creating recipes.</p>
        </div>
    );

    const SignedInContent = () => (
        <div className="body">
            <textarea placeholder="Upload an image of your dish and include any speicifications (preferences, dietary restrictions, etc.) you have for your recipe." />
            <br />
            <button>Upload Image</button>
        </div>
    );

    return (
        <div>
            <Header />
            {isSignedIn ? <SignedInContent /> : <NotSignedInContent />}
        </div>
    );
};

export default Home;