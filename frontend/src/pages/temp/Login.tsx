import { useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

interface LoginPayload {
	email: string;
	password: string;
}

export default function SignUp() {
	const [email, setEmail] = useState<string>("");
	const [password, setPassword] = useState<string>("");

	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();

		const payload: LoginPayload = { email, password };
		console.log(payload);
		try {
			const response = await fetch("http://localhost:8000/login", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
                credentials: "include",
				body: JSON.stringify(payload),
			});
			if (!response.ok) throw new Error("erreur lors de l'inscription");
			console.log(response);
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
			<Button variant="primary" type="submit">
				Se connecter
			</Button>
		</Form>
	);
}
