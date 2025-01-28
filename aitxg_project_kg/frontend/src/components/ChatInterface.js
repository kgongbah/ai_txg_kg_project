import React, { useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext"; // Import AuthContext
//import "./../styles/ChatInterface.css";

const ChatInterface = () => {
  const [messages, setMessages] = useState([]); // Chat messages
  const [currentMessage, setCurrentMessage] = useState(""); // User's input message
  const [selectedFile, setSelectedFile] = useState(null); // Uploaded file state
  const [statusMessage, setStatusMessage] = useState(""); // Feedback message
  const [recipeTitle, setRecipeTitle] = useState(""); // Recipe title
  const { user } = useContext(AuthContext); // Get the logged-in user from context

  const handleInputChange = (e) => {
    setCurrentMessage(e.target.value);
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleSendMessage = async () => {
    console.log(messages.length)
    if (!currentMessage && !selectedFile) return;

    // Add the user's message to the chat
    const newMessages = [
      ...messages,
      { type: "user", text: currentMessage || "Image uploaded." },
    ];
    setMessages(newMessages);

    // if (!user) {
    //   setMessages((prev) => [...prev, { type: "bot", text: "Please log in first." }]);
    //   return;
    // }

    try {
      // Prepare FormData for the API request
      const formData = new FormData();
      formData.append("message", currentMessage);
      if (selectedFile) {
        formData.append("file", selectedFile);
      }

      // Hypothetical AWS Endpoint for ML response
      const response = await fetch("http://aws-ml-endpoint-url.com/chat", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${user.token}`, // Pass token if required
        },
        body: formData,
      });

      if (response.ok) {
        // Mock response until actual AWS functionality is implemented
        const responseData = await response.json();
        setMessages((prev) => [...prev, { type: "bot", text: responseData.message || "Response" }]);
      } else {
        setMessages((prev) => [...prev, { type: "bot", text: "An error occurred. Please try again." }]);
      }
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prev) => [...prev, { type: "bot", text: "Failed to process your request." }]);
    }

    // Reset input and file states
    setCurrentMessage("");
    //setSelectedFile(null); //this seems to cause the user to be unable to save a recipe
  };

  const handleSave = async() => {
    if (messages.length == 0) return  //Check if user has submitted at least one message/image

    const title = recipeTitle || prompt("Enter a title for your recipe.")
    if (!title) {
        setStatusMessage("Recipe title required to save recipe.");
        return;
    };

    //Try to save the recipe to the database
    try {
        const formData = new FormData();
        formData.append("recipe_name", title);
        formData.append("specifications_text", messages[0]?.text || "");
        formData.append("recipe_output", messages[1]?.text || "");
        if (selectedFile) formData.append("file", selectedFile);
        
  

        const response = await fetch(`http://localhost:80/user/${user.user_id}/recipes/`, {
            method: "POST",
            //headers: {"Content-Type": "application/json"},
            body: formData
        });

        if (response.ok) {

            const savedRecipe = await response.json();
            console.log(savedRecipe)
            setStatusMessage(`Recipe "${savedRecipe.recipe_name}" with ID ${savedRecipe.recipe_id} saved successfully!`);

            //Logic for when user has more than a single message/response, in which case subsequent messages/responses are in different table
            if (messages.length > 2) {//This means that there is more than one message/response pair
                try {
                    for (let i = 2; i < messages.length; i = i + 2) {
                        const additionalTextPayload = {
                            user_id: savedRecipe.user_id,
                            recipe_id: savedRecipe.recipe_id,
                            prompt: messages[i]?.text || "",
                            response: messages[i + 1]?.text || ""
                        };

                        const additionalTextResponse = await fetch(`http://localhost:80/users/${savedRecipe.user_id}/recipes/${savedRecipe.recipe_id}/recipe_additional_texts/`, {
                            method: "POST",
                            headers: {"Content-Type": "application/json"},
                            body: JSON.stringify(additionalTextPayload)     
                        });
                        if (additionalTextResponse.ok) {
                          console.log(`Additional text for recipe_id ${additionalTextResponse.recipe_id} saved successfully.`)
                        } else {
                          const errorData = await response.json();
                          setStatusMessage(`Error saving recipe's additional text: ${errorData.detail}`);
                        };
                    };

                } catch (error) {
                  console.error("Error saving recipe:", error);
                  setStatusMessage("An error occurred while saving the recipe.");
                };
            };


            setRecipeTitle(""); // Reset the title for future saves
          } else {
            const errorData = await response.json();
            setStatusMessage(`Error saving recipe: ${errorData.detail}`);
          }
        } catch (error) {
          console.error("Error saving recipe:", error);
          setStatusMessage("An error occurred while saving the recipe.");
        };


      
        
    };
  

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h1>Chat Interface</h1>
      </div>
      <div className="chat-body">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.type}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="chat-footer">
        <textarea
          placeholder="Type your message..."
          value={currentMessage}
          onChange={handleInputChange}
        />
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleSendMessage}>Send</button>
      </div>
      {messages.length > 0 && (
        <div className="chat-save">
          <button onClick={handleSave}>Save Recipe</button>
        </div>
      )}
      {statusMessage && <p className="status-message">{statusMessage}</p>}
    </div>
  );
};


export default ChatInterface;
