import React, { useState, useEffect, useContext } from "react";
import { AuthContext } from "../context/AuthContext";

const Profile = () => {
    const { user } = useContext(AuthContext);
    const [recipes, setRecipes] = useState([]);
    const [selectedRecipe, setSelectedRecipe] = useState(null);

    

    useEffect(() => {
        // Ensure user exists before accessing its properties
        if (!user) {
            return <p>Loading user data...</p>; // Prevents errors if user is null
        }
        
        const fetchRecipes = async () => {
            try {
                const response = await fetch(`http://localhost:8000/user/${user.user_id}/recipes/`);
                if (response.ok) {
                    const data = await response.json();
                    setRecipes(data);
                } else {
                    console.error("Failed to fetch recipes");
                }
            } catch (error) {
                console.error("Error fetching recipes:", error);
            }
        };

        fetchRecipes();
    }, [user]);

    const handleViewRecipe = async (recipeId) => {
        try {
            const response = await fetch(`http://localhost:8000/user/${user.user_id}/recipes/${recipeId}`);
            if (response.ok) {
                const recipeData = await response.json();
                setSelectedRecipe(recipeData);
            } else {
                console.error("Failed to fetch recipe details");
            }
        } catch (error) {
            console.error("Error fetching recipe details:", error);
        }
    };

    return (
        <div>
            <h2>{user.username}'s Recipes</h2>
            <ul>
                {recipes.map((recipe) => (
                    <li key={recipe.recipe_id}>
                        {recipe.recipe_name}
                        <button onClick={() => handleViewRecipe(recipe.recipe_id)}>View</button>
                    </li>
                ))}
            </ul>

            {selectedRecipe && (
                <div>
                    <h3>{selectedRecipe.recipe_name}</h3>
                    <p><strong>Specifications:</strong> {selectedRecipe.specifications_text}</p>
                    <p><strong>Output:</strong> {selectedRecipe.recipe_output}</p>
                    {selectedRecipe.file_url && <img src={`http://localhost:8000/${selectedRecipe.file_url}`} alt="Recipe" />}
                    <button onClick={() => setSelectedRecipe(null)}>Close</button>
                </div>
            )}
        </div>
    );
};

export default Profile;
