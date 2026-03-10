import { METHODS } from "http";
import React from "react";

function ProfileActionCard(connected: boolean) {
	const logout = () => {
		fetch("http://localhost:8000/user/signup", {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
			credentials: "include",
		});
	};
	if (connected) {
		return (
			<div className="border rounded-2xl flex justify-items-center ">
				<a href="/profile">Mon profil</a>
				<a href="/universes">Mes Univers</a>
				<button type="button" onClick={logout}>
					Se déconnecter
				</button>
			</div>
		);
	}
}

export default ProfileActionCard;
