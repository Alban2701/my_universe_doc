import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import BaseForm from "../components/UI/Forms/BaseForm";
import BadCredentials from "../components/UI/Cards/BadCredentials";
import React from "react";

interface LoginPayload {
	email: string;
	password: string;
}

export default function Login() {
	const [email, setEmail] = useState<string>("");
	const [password, setPassword] = useState<string>("");
	const [badCredentials, setBadCredentials] = useState<boolean>(false);

	const navigate = useNavigate();
	const location = useLocation();

	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();

		const payload: LoginPayload = { email, password };
		try {
			const response = await fetch(`/api/user/login`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				credentials: "include",
				body: JSON.stringify(payload),
			});
			if (!response.ok) {
				setBadCredentials(true);
				throw new Error("erreur lors de l'inscription");
			}
			const redirectTo = location.state?.from?.pathname || "/";
			navigate(redirectTo, { replace: true });
		} catch (error) {
			console.log(error);
		}
	};
	return (
		<div>
			{badCredentials && <BadCredentials />}
			<BaseForm
				title={"Login"}
				submitTitle={"Log In"}
				onSubmit={handleSubmit}
				inputs={[
					{
						type: "text",
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
						placeholder: "Input your password",
						required: true,
						onChange(e) {
							setPassword(e.target.value);
						},
					},
				]}
			/>
			²{" "}
		</div>
	);
}
