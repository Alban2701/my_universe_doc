import { useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

interface SignUpPayload {
	email: string;
	password: string;
	checkPassword: string;
	username: string;
}

export default function SignUp() {
	const [email, setEmail] = useState<string>("");
	const [password, setPassword] = useState<string>("");
	const [checkPassword, setCheckPassword] = useState<string>("");
	const [username, setUsername] = useState<string>("");

	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();

		const payload: SignUpPayload = { email, password, checkPassword, username };
		if (payload.password !== payload.checkPassword) {
			throw new Error("Les mots de passes ne correspondent pas");
		}
		const verified_payload = {
			email: payload.email,
			password: payload.password,
			username: payload.username,
			bio: null,
			picture: null,
		};
		console.log(verified_payload);
		try {
			const response = await fetch("http://localhost:8000/signup", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(verified_payload),
			});
			if (!response.ok) throw new Error("erreur lors de l'inscription");
			const data = await response.json();
			console.log("Réponse Api :", data);
		} catch (error) {
			console.log(error);
		}
	};
	return (
		<Form onSubmit={handleSubmit}>
			<Form.Group>
				<Form.Label>Adresse Email</Form.Label>
				<Form.Control
					type="email"
					placeholder="Entrez votre adresse mail"
					value={email}
					onChange={(e) => {
						setEmail(e.target.value);
					}}
				/>
			</Form.Group>
			<Form.Group>
				<Form.Label>Mot de passe</Form.Label>
				<Form.Control
					type="password"
					value={password}
					onChange={(e) => {
						setPassword(e.target.value);
					}}
				/>
			</Form.Group>
			<Form.Group>
				<Form.Label>Vérifier le mot de passe</Form.Label>
				<Form.Control
					type="password"
					value={checkPassword}
					onChange={(e) => {
						setCheckPassword(e.target.value);
					}}
				/>
			</Form.Group>
			<Form.Group>
				<Form.Label>Pseudonyme</Form.Label>
				<Form.Control
					value={username}
					onChange={(e) => {
						setUsername(e.target.value);
					}}
				/>
			</Form.Group>
			<Button variant="primary" type="submit">
				S'inscrire
			</Button>
		</Form>
	);
}
