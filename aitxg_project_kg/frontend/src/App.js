import logo from './logo.svg';
import './styles/App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import LoginSignup from './components/LoginSignup';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route exact path="/" element={<Home />} />
          <Route path="/login-signup" element={<LoginSignup />} />
        </Routes> 
      </div>
    </Router>
  );
}

export default App;
