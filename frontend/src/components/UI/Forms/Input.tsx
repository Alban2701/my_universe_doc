import type { HTMLInputTypeAttribute } from "react";

export interface InputInterface {
	type: HTMLInputTypeAttribute | undefined;
	name: string | undefined;
	placeholder: string | undefined;
	content: string | undefined;
	required: boolean;
	onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export default function Input({
	type,
	name,
	placeholder,
	content,
	required,
	onChange,
}: InputInterface) {
	return (
		<>
			<label htmlFor={name}>{name}</label>
			<br />
			{content ? (
				<input
					type={type}
					id={name}
					name={name}
					placeholder={placeholder}
					value={content}
					required={required}
					onChange={onChange}
					className="pt-2 pl-2 w-full h-full justify-center"
				/>
			) : (
				<input
					type={type}
					id={name}
					name={name}
					placeholder={placeholder}
					required={required}
					onChange={onChange}
					className="pt-2 pl-2 w-full h-full justify-center"
				/>
			)}
		</>
	);
}
