import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import BaseForm from "../components/UI/Forms/BaseForm";

interface LoginPayload {
	email: string;
	password: string;
}

export default function Login() {
	const [email, setEmail] = useState<string>("");
	const [password, setPassword] = useState<string>("");

	const navigate = useNavigate();
	const location = useLocation();

	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();

		const payload: LoginPayload = { email, password };
		console.log(payload);
		try {
			const response = await fetch("/api/user/login", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				credentials: "include",
				body: JSON.stringify(payload),
			});
			if (!response.ok) throw new Error("erreur lors de l'inscription");
			const redirectTo = location.state?.from?.pathname || "/";
			navigate(redirectTo, { replace: true });
		} catch (error) {
			console.log(error);
		}
	};
	return BaseForm({
		title: "Log In",
		submitTitle: "Log In",
		onSubmit: handleSubmit,
		inputs: [
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
		],
	});
}
