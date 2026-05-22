import { useNavigate } from "react-router-dom";

function ProfileActionCard({
	connected,
	logoutAction,
}: {
	connected: boolean;
	logoutAction: () => void;
}) {
	const navigate = useNavigate();
	const handleLogout = () => {
		const fetchLogout = async () => {
			navigate("/");
			logoutAction();
			await fetch("/api/user/logout", {
				method: "GET",
				headers: {
					"Content-Type": "application/json",
				},
				credentials: "include",
			});
			window.location.reload();
		};
		fetchLogout();
	};

	const handleLogin = () => {
		navigate("/login");
	};

	const handleSignup = () => {
		navigate("/signup");
	};

	if (connected) {
		return (
			<div className="border rounded-2xl flex justify-items-center z-10 bg-white p-2">
				<button
					type="button"
					className="hover: cursor-pointer"
					onClick={handleLogout}
				>
					Logout
				</button>
			</div>
		);
	} else {
		return (
			<div className="border rounded-2xl flex flex-col justify-items-center p-2 z-10">
				<button
					type="button"
					className="hover: cursor-pointer"
					onClick={handleLogin}
				>
					Login
				</button>
				<button
					type="button"
					className="hover: cursor-pointer"
					onClick={handleSignup}
				>
					Signup
				</button>
			</div>
		);
	}
}

export default ProfileActionCard;
