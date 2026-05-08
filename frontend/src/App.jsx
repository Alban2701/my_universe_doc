import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import DragAndDrop from "./pages/DragAndDrop";
import Home from "./pages/Home";
import Login from "./pages/Login";
import MyDoc from "./pages/MyDoc";
import SignUp from "./pages/Signup";
import UpdatePassword from "./pages/UpdatePassword";

function App() {
	return (
		<Router>
			<Routes>
				<Route path="/" element={<Home />} />
				<Route path="/signup" element={<SignUp />} />
				<Route path="/login" element={<Login />} />
				<Route path="/mydoc/" element={<MyDoc />} />
				<Route path="/mydoc/:universeId" element={<MyDoc />} />
				<Route
					path="/mydoc/:universeId/entities/:entityId"
					element={<MyDoc />}
				/>
				<Route path="/dnd" element={<DragAndDrop />} />
				<Route path="/update-user" element={<UpdatePassword />} />
			</Routes>
		</Router>
	);
}

export default App;
