import React, { createContext, useState, useEffect } from "react";

// Create the AuthContext
export const AuthContext = createContext();

// Create the AuthProvider component
export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null); // State to store user information

    // Initialize user state from localStorage when the app loads
    useEffect(() => {
        const user_id = localStorage.getItem("user_id");
        const username = localStorage.getItem("username");
        
        
        setUser({ user_id, username });
        
    }, []);

    // Logout function to clear user data
    const logout = () => {
        localStorage.removeItem("user_id");
        localStorage.removeItem("username");
        setUser(null);
    };

    // Provide the context values (user, setUser, logout) to children
    return (
        <AuthContext.Provider value={{ user, setUser, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
