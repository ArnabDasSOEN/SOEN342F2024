import { useState } from 'react';

import './App.css';
import { Routes, Route, BrowserRouter } from 'react-router-dom';
import { Navbar } from './Components/Navbar/Navbar';
import { Landing } from './Pages/Landing';
import { Login } from './Pages/Login';
import { Footer } from './Components/Footer/Footer';
import { SignUp } from './Pages/SignUp';
import { Chatbot } from './Components/Chatbot/Chatbot';
import { Dashboard } from "./Pages/RequestDelivery.jsx";
import { Logout } from "./Pages/Logout";
import { UserHomePage } from './Pages/UserHomePage.jsx';
import { ViewOrders } from './Pages/ViewOrders.jsx';
import { ViewDeliveryRequest } from "./Pages/ViewDeliveryRequest.jsx"
import { TrackOrders } from './Pages/TrackOrders.jsx';
//import { CancelDeliveryRequest } from './Pages/CancelDeliveryRequest.jsx';
import { PayDeliveryRequest } from './Pages/PayDeliveryRequest.jsx';

function App() {

  const [user_id, setUserId] = useState(localStorage.getItem("user_id"))
  

  return (
    <div className='App'>
      <BrowserRouter>
        <Navbar user_id={user_id} setUserId={setUserId}/>


        <Routes>
          <Route path='/' element={<Landing/>}/>
          <Route path='/login' element={<Login setUserId={setUserId} />}/>
          <Route path='/signup' element={<SignUp/>}/>
          <Route path='/dashboard' element={<Dashboard/>}/>
          <Route path='/logout' element={<Logout/>}/>
          <Route path='/userHomePage' element={<UserHomePage/>}/>

          <Route path='/viewOrders' element={<ViewOrders/>}/>
          <Route path='/viewDeliveryRequest' element={<ViewDeliveryRequest/>}/>
          <Route path='/trackOrders' element={<TrackOrders/>}/>
          {/* <Route path='/cancelDeliveryRequest' element={<CancelDeliveryRequest/>}/> */}
          
          {/* <Route path='/payDeliveryRequest' element={<PayDeliveryRequest/>}/> */}

        </Routes>
        <Chatbot/>
        <Footer/>
      </BrowserRouter>
    </div>
  );
}

export default App;
