import { Route, Routes } from "react-router-dom";
import Controller from "./components/Controller";
import Home from "./components/Home";
import Login from "./components/Login";
import Register from "./components/Register";

function App() {
  return (
    <>
      <div className="">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/app" element={ <Controller />}/>
          <Route path="/register" element={ <Register />}/>
          <Route path="/login" element={ <Login />}/>
        </Routes>
        {/* <Controller /> */}
      </div>
    </>
  );
}

export default App;
