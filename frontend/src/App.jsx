import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import SignUp from "./pages/Signup";
import MyDoc from "./pages/MyDoc";

function App() {
	return (
		<Router>
			<Routes>
				<Route path="/" element={<Home />} />
				<Route path="/signup" element={<SignUp />} />
				<Route path="/login" element={<Login />} />
				<Route path="/universes/:universeId" element={<MyDoc />} />
				<Route
					path="/universes/:universeId/entities/:entityId"
					element={<MyDoc />}
				/>
			</Routes>
		</Router>
	);
}

export default App;
