import './App.css';
import { Routes, Route, BrowserRouter } from 'react-router-dom';
import { Navbar } from './Components/Navbar/Navbar';
import { Landing } from './Pages/Landing';
import { Login } from './Pages/Login';
import { Footer } from './Components/Footer/Footer';

function App() {
  return (
    <div>
      <BrowserRouter>
        <Navbar/>
        <Routes>
          <Route path='/' element={<Landing/>}/>
          <Route path='/login' element={<Login/>}/>
        </Routes>
        <Footer/>
      </BrowserRouter>
    </div>
  );
}

export default App;
