import React from 'react';
import { Routes, Route, Link } from "react-router-dom";
import './App.css';
import { NavBar } from "./components/ui/NavBar"

function App() {
  return (
    <div className="App">
      <div>
        <NavBar />
      </div>
      <h1>Welcome to React Router!</h1>
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/home" element={<Home />} />
        <Route path="/cocktails" element={<CocktailsPage />}/>
      </Routes>
    </div>
  );
}


const Home = () => {
  return (<>
    <main>
      <h2>Welcome to the homepage!</h2>
      <p>You can do this, I believe in you.</p>
    </main>
    <nav>
      <Link to="/cocktails">Cocktails</Link>
    </nav>
  </>)
}

const CocktailsPage = () => {
  return (
    <>
      <main>
        <h2>Cocktails</h2>
        <p>
          Which cocktail do you prefer?
        </p>
      </main>
      <nav>
        <Link to="/home">Home</Link>
      </nav>
    </>
  )
}

export default App;
