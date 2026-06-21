import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { fetchLogin } from "@/src/fetchers";
import BadCredentials from "../components/UI/Cards/BadCredentials";
import BaseForm from "../components/UI/Forms/BaseForm";

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
			const response = await fetchLogin(payload);
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
						content: undefined,
					},
					{
						type: "password",
						name: "password",
						placeholder: "Input your password",
						required: true,
						onChange(e) {
							setPassword(e.target.value);
						},
						content: undefined,
					},
				]}
			/>
			²{" "}
		</div>
	);
}
