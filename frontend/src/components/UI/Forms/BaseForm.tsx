import React, { type FormEventHandler, JSX } from "react";
import type { InputInterface } from "./Input";
import Input from "./Input";

function BaseForm({
	title,
	submitTitle,
	onSubmit,
	inputs,
}: {
	title: string;
	submitTitle: string;
	onSubmit: FormEventHandler<Element> | undefined;
	inputs: Array<InputInterface>;
}) {
	return (
		<span className="h-screen flex items-center justify-center">
			<div className="px-5 py-2 border-collapse items-center flex flex-col rounded-md shadow-xl/10 ring ring-gray-100">
				<h1 className="text-3xl text-center border-b mb-5">{title}</h1>
				<form action="/" onSubmit={onSubmit} className="flex flex-col p-2">
					{inputs.map((i) => {
						return Input(i);
					})}
					<div className="flex justify-center m-3">
						<button
							type="submit"
							className="cursor-pointer bg-blue-600 text-white font-medium min-w-3xs px-6 py-3 rounded-lg transition max-w-3xs mt-7  hover:bg-blue-800 active:inset-shadow-sm/70"
						>
							{submitTitle}
						</button>
					</div>
				</form>
			</div>
		</span>
	);
}

export default BaseForm;
