import React, { useState } from "react";
import "./../styles/LoginSignup.css";

const LoginSignup = () => {
    const [isSignUp, setIsSignUp] = useState(true);

    const handleSwitch = () => {
        setIsSignUp(!isSignUp);
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        if (isSignUp) {
            console.log("Signing up...");
            //TODO: sign-up logic
        }
        else {
            console.log("Logging in...");
            //TODO: log-in logic
        };
    }

    return (
        <div className="login-signup-container">
            <h2>{isSignUp ? "Sign-up" : "Log-in"}</h2>
            <form onSubmit={handleSubmit}>
                {/*Username input */}
                <div className="input-field">
                    <label htmlFor="username">Username</label>
                    <input type="text" id="username" name="username" required />
                </div>
                {/*Password input*/}
                <div className="intput-field">
                    <label htmlFor="Password">Password</label>
                    <input type="text" id="password" name="password" required />
                </div>
                {/*Submit button*/}
                <button type="submit">{isSignUp ? "Sign-up" : "Log-in"}</button>
            </form>

            <div className="toggle">
                <p>
                    {isSignUp ? "Already have an account?" : "Don't have an account?"}
                    <button onClick={handleSwitch}>
                        {isSignUp ? "Log-in" : "Sign-up"}
                    </button>
                </p>
            </div>
        </div>
    );
};

export default LoginSignup