import logo from './logo.svg';
import './styles/App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import LoginSignup from './components/LoginSignup';
import ChatInterface from './components/ChatInterface';
import { AuthProvider } from './context/AuthContext'; // Import AuthProvider

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route exact path="/" element={<Home />} />
            <Route path="/login-signup" element={<LoginSignup />} />
            <Route path="/chat" element={<ChatInterface />} />
          </Routes> 
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
