import React from 'react';
import logo from './logo.svg';
import './App.css';

// import AdminProjecrProgressBar from './components/AdminProjecrProgressBar' 
import UserTimeTracker from './components/UserTimeTracker';
import TlTimeTracker from './components/TlTimeTracker';

function App() {
  return (
    <div className="App">
       
       {baseSegment == "/users" ? <UserTimeTracker /> : (baseSegment == "/moni_tasks" ? <TlTimeTracker />:'Not Available')}
     
        {/* <UserTimeTracker />  */}
     
         {/* <UserTimeTracker /> */}
      
        
     
      
      {/* <header className="App-header">
      EF498122700IN
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header> */}
    </div>
  );
}

export default App;
