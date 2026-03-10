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
		<input
			type={type}
			name={name}
			placeholder={placeholder}
			required={required}
			onChange={onChange}
			className="py-2 mt-2 pl-2 rounded-md inset-shadow-sm inset-ring-gray-200 inset-ring-1"
		/>
	);
}
