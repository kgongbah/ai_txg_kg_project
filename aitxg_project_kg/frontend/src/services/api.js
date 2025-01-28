// api.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:80", // FastAPI base URL
});

export default api;