import type { ChangeEventHandler, HTMLInputTypeAttribute } from "react";

export interface InputInterface {
	type: HTMLInputTypeAttribute | undefined;
	name: string | undefined;
	placeholder: string | undefined;
	required: boolean;
	onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export default function Input({
	type,
	name,
	placeholder,
	required,
	onChange,
}: InputInterface) {
	return (
		<>
			<label htmlFor={name}>{name}</label>
			<br />
			<input
				type={type}
				id={name}
				name={name}
				placeholder={placeholder}
				required={required}
				onChange={onChange}
				className="pt-2 pl-2 w-full h-full justify-center"
			/>
		</>
	);
}
