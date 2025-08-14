import "./App.css";
import { Routes, Route } from "react-router-dom";
import HomePage from "./views/Home";
import ViewPage from "./views/View";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/view" element={<ViewPage />} />
      </Routes>
    </div>
  );
}

export default App;
