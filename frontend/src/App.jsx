import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import SignUp from "./pages/Signup";

// import Profile from "./pages/temp/Profile";

function App() {
	return (
		<Router>
			<Routes>
				<Route path="/" element={<Home />} />
				<Route path="/signup" element={<SignUp />} />
				<Route path="/login" element={<Login />} />
				{/* <Route path="/profile" element={<Profile />} /> */}
			</Routes>
		</Router>
	);
}

export default App;
