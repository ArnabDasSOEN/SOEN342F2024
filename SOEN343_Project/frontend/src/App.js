import './App.css';
import { Routes, Route, BrowserRouter } from 'react-router-dom';
import { Navbar } from './Components/Navbar/Navbar';
import { Landing } from './Pages/Landing';
import { Login } from './Pages/Login';
import { Footer } from './Components/Footer/Footer';
import { SignUp } from './Pages/SignUp';
import { Chatbot } from './Components/Chatbot/Chatbot';

function App() {
  return (
    <div>
      <BrowserRouter>
        <Navbar/>
        <Routes>
          <Route path='/' element={<Landing/>}/>
          <Route path='/login' element={<Login/>}/>
          <Route path='/signup' element={<SignUp/>}/>
        </Routes>
        <Chatbot/>
        <Footer/>
      </BrowserRouter>
    </div>
  );
}

export default App;
