import { useState } from "react";
import BaseForm from "../components/UI/Forms/BaseForm";
import { redirect, useLocation, useNavigate } from "react-router-dom";

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

	const navigate = useNavigate();

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
		try {
			const response = await fetch("http://localhost:8000/user/signup", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(verified_payload),
				credentials: "include",
			});
			if (!response.ok) throw new Error("erreur lors de l'inscription");
			const data = await response.json();
			console.log("Réponse Api :", data);
			const redirectTo = "/login";
			navigate(redirectTo, { replace: true });
		} catch (error) {
			console.log(error);
		}
	};
	return BaseForm({
		title: "Signup",
		submitTitle: "Signup",
		onSubmit: handleSubmit,
		inputs: [
			{
				type: "text",
				name: "username",
				placeholder: "Input your Username",
				required: true,
				onChange: (e) => {
					setUsername(e.target.value);
				},
			},
			{
				type: "email",
				name: "email",
				placeholder: "Input your Email",
				required: true,
				onChange: (e) => {
					setEmail(e.target.value);
				},
			},
			{
				type: "password",
				name: "password",
				placeholder: "Input your Password",
				required: true,
				onChange: (e) => {
					setPassword(e.target.value);
				},
			},
			{
				type: "password",
				name: "checkPassword",
				placeholder: "Check your Password",
				required: true,
				onChange: (e) => {
					setCheckPassword(e.target.value);
				},
			},
		],
	});
}
