import { useEffect, useState } from "react";
import { Spinner } from "react-bootstrap";

type UserProfile = {
	id: number;
	email: string;
};

export default function Profile() {
	const [user, setUser] = useState<UserProfile | null>(null);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		const fetchProfile = async () => {
			try {
				const res = await fetch("http://localhost:8000/me", {
					method: "GET",
					credentials: "include",
				});

				if (res.status === 200) {
					const data = await res.json();
					console.log("Profil récupéré :", data);
					setUser(data);
				} else {
					console.log("Utilisateur non connecté.");
					setUser(null);
				}
			} catch (err) {
				console.error("Erreur réseau :", err);
				setUser(null);
			} finally {
				setLoading(false);
			}
		};

		fetchProfile();
	}, []);

	if (loading) {
		return (
			<div className="d-flex justify-content-center mt-5">
				<Spinner animation="border" />
			</div>
		);
	}

	if (!user) {
		return (
			<div className="container mt-5">
				<h3>Vous n'êtes pas connecté.</h3>
			</div>
		);
	}

	return (
		<div className="container mt-5">
			<h3>Profil</h3>
			<p>Email : {user.email}</p>
			<p>ID : {user.id}</p>
		</div>
	);
}
