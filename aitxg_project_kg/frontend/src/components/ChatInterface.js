import React, { useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext"; // Import AuthContext
import "./../styles/ChatInterface.css";
import { SignatureV4 } from "@aws-sdk/signature-v4";
import { Sha256 } from "@aws-crypto/sha256-browser";
// import { BedrockRuntimeClient, InvokeModelCommand } from "@aws-sdk/client-bedrock-runtime"; // Old method (commented out)

const ChatInterface = () => {
  const [messages, setMessages] = useState([]); // Chat messages
  const [currentMessage, setCurrentMessage] = useState(""); // User's input message
  const [selectedFile, setSelectedFile] = useState(null); // Uploaded file state
  const [statusMessage, setStatusMessage] = useState(""); // Feedback message
  const [recipeTitle, setRecipeTitle] = useState(""); // Recipe title
  const { user } = useContext(AuthContext); // Get the logged-in user from context

  const api = "http://localhost:8000";

  //AWS Signature V4 Signer: Instead of using BedrockRuntimeClient, which requires permanent access keys,
  //we use AWS Signature V4, which manually signs each request with temporary access keys and tokens.
  const signer = new SignatureV4({
    credentials: {
      accessKeyId: process.env.REACT_APP_AWS_ACCESS_KEY_ID,
      secretAccessKey: process.env.REACT_APP_AWS_SECRET_ACCESS_KEY,
      sessionToken: process.env.REACT_APP_AWS_SESSION_TOKEN, // Only needed for temporary credentials
    },
    service: "bedrock",
    region: "us-east-1",
    sha256: Sha256,
  });

  // Commented this out as this object is used for permanent AWS access key, which I don't have
  // const bedrockClient = new BedrockRuntimeClient({
  //   region: "us-east-1",
  //   credentials: {
  //     accessKeyId: process.env.REACT_APP_AWS_ACCESS_KEY_ID,
  //     secretAccessKey: process.env.REACT_APP_AWS_SECRET_ACCESS_KEY,
  //     sessionToken: process.env.REACT_APP_AWS_SESSION_TOKEN,
  //   },
  // });

  //Updates the current message whenever user changes it.
  const handleInputChange = (e) => {
    setCurrentMessage(e.target.value);
  };

  //Updates the file whenever the user changes it. 
  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  //Claude 3.5 requires files in requests converted to Base64
  const convertFileToBase64 = async (file) => {
    return new Promise((resolve, reject) => { //Promise function returns asynchronous functions depending on success
      const reader = new FileReader(); //Built-in JavaScript Object
      reader.readAsDataURL(file);
      reader.onload = () => {
        const base64String = reader.result.split(",")[1]; // Remove metadata part
        resolve(base64String);
      };
      reader.onerror = (error) => reject(error);
    });
  };

  const handleSendMessage = async () => {
    if (!currentMessage && !selectedFile) return;

    //Add user message to chat, stored as JSON indicating who sent the message (user or AWs) and text
    const newUserMessage = { type: "user", text: currentMessage || "Image uploaded." };
    //prev is the old state of messages, and (prev) => [...prev, newUserMessage] updates the useState of messages,
    //appending newUserMessage to prev.
    setMessages((prev) => [...prev, newUserMessage]); 

    let base64Image = null;
    if (selectedFile) {
      base64Image = await convertFileToBase64(selectedFile);
    }

    // Construct full conversation history, acts similar to [msg for msg in messages] one-line python array construction
    // Each entry in conversationHistory relates to a msg in messages, with property role which is the same as the role
    //in msg, and content, which is the msg's contents. AWS Bedrock requires this format (See Bedrock Claude 3.5 API Request for more info)
    const conversationHistory = messages.map((msg) => ({
      role: msg.type === "user" ? "user" : "assistant",
      content: [{ type: "text", text: msg.text }],
    }));

    // Add the new user message to history. Formats the msg with property "role" and property "content", which
    // includes an array of info representing image if it exists or an empty array otherwise, and the message text.
    conversationHistory.push({
      role: "user",
      content: [
        ...(base64Image //... operator gets rid array wrapping image, otherwise -> content: {[{image_info}], {text_info}}, which is unwanted
          ? [
              {
                type: "image",
                source: {
                  type: "base64",
                  media_type: "image/png",
                  data: base64Image,
                },
              },
            ]
          : []),
        { type: "text", text: currentMessage },
      ],
    });

    const requestBody = {
      anthropic_version: "bedrock-2023-05-31",
      max_tokens: 1000,
      messages: conversationHistory, // Send full conversation history
    };

    try {
      // Sign the request using SignatureV4
      //Can't find any documentation on this nor the example I follow, but it works lol
      const signedRequest = await signer.sign({
        method: "POST",
        hostname: "bedrock-runtime.us-east-1.amazonaws.com",
        path: "/model/anthropic.claude-3-5-sonnet-20240620-v1:0/invoke",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
          "Host": `bedrock-runtime.us-east-1.amazonaws.com`,
        },
        body: JSON.stringify(requestBody),
      });

      // Send the signed request using fetch
      const response = await fetch(`https://${signedRequest.hostname}${signedRequest.path}`, {
        method: signedRequest.method,
        headers: signedRequest.headers,
        body: signedRequest.body,
      });

      if (response.ok) {
        const responseData = await response.json();

        //Construct the bot's response. Get responseData, ?.content grabs content if it exists or returns undefined otherwise
        //to avoid errors. ?.map() returns an array of item.text for item in in content and joins them, in case the bot returns
        //multiple text objects in the content of its response (unknown if this actually happens, but it works lol).
        const botResponse = responseData?.content?.map(item => item.text).join(" ") || "No response";

        //Appends botResponse to all previous messages in messages.
        setMessages((prev) => [...prev, { type: "bot", text: botResponse }]);
        console.log("API Response received with no errors.")
      } else {
        //Prints message indicating API Request error
        setMessages((prev) => [...prev, { type: "bot", text: "Error: Could not get a response from AWS." }]);
      }
    } catch (error) {
      //Logs error regarding 
      console.error("Error sending message:", error);
      setMessages((prev) => [...prev, { type: "bot", text: "Failed to process your request." }]);
    }

    // Reset input and file states
    setCurrentMessage("");
    // setSelectedFile(null); // This may interfere with saving the recipe
  };

  const handleSave = async () => {
    if (messages.length === 0) return; // Ensure at least one message exists

    const title = recipeTitle || prompt("Enter a title for your recipe.");
    if (!title) {
      setStatusMessage("Recipe title required to save recipe.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("recipe_name", title);
      formData.append("specifications_text", messages[0]?.text || "");
      formData.append("recipe_output", messages[1]?.text || "");
      if (selectedFile) formData.append("file", selectedFile);

      const response = await fetch(`${api}/user/${user.user_id}/recipes/`, {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const savedRecipe = await response.json();
        setStatusMessage(`Recipe "${savedRecipe.recipe_name}" saved successfully!`);
        if (messages.length > 2) {
          for (let i = 2; i < messages.length; i += 2) {
            const additionalTextPayload = {
              user_id: savedRecipe.user_id,
              recipe_id: savedRecipe.recipe_id,
              prompt: messages[i]?.text || "",
              response: messages[i + 1]?.text || "",
            };

            await fetch(`${api}/users/${savedRecipe.user_id}/recipes/${savedRecipe.recipe_id}/recipe_additional_texts/`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(additionalTextPayload),
            });
          }
        }

        setRecipeTitle("");
      } else {
        const errorData = await response.json();
        setStatusMessage(`Error saving recipe: ${errorData.detail}`);
      }
    } catch (error) {
      console.error("Error saving recipe:", error);
      setStatusMessage("An error occurred while saving the recipe.");
    }
  };

  //Note that index is the index position of msg in messages, type is either bot or user
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
        <textarea placeholder="Type your message..." value={currentMessage} onChange={handleInputChange} />
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
