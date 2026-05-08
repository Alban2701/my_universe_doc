import { useState } from "react";
import { redirect, useLocation, useNavigate } from "react-router-dom";
import BaseForm from "../components/UI/Forms/BaseForm";

interface UpdateUserPayload {
	id: number;
	password: string;
	checkPassword: string;
}

export default function UpdateUserPassword() {
	const [id, setId] = useState<number>(1);
	const [password, setPassword] = useState<string>("");
	const [checkPassword, setCheckPassword] = useState<string>("");

	const navigate = useNavigate();

	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();

		const payload: UpdateUserPayload = { id, password, checkPassword };
		if (payload.password !== payload.checkPassword) {
			throw new Error("Les mots de passes ne correspondent pas");
		}
		const verified_payload = {
			id: payload.id,
			password: payload.password,
			bio: null,
			picture: null,
		};
		try {
			const response = await fetch(`/api/user/${id}`, {
				method: "PATCH",
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
		title: "Update a User",
		submitTitle: "Signup",
		onSubmit: handleSubmit,
		inputs: [
			{
				type: "number",
				name: "id",
				placeholder: "Input the user's id",
				required: true,
				onChange: (e) => {
					setId(e.target.valueAsNumber);
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
