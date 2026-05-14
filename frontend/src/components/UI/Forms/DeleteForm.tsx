import { type FormEventHandler, useState } from "react";
import Input from "./Input";

export default function BaseForm({
	title,
	submitTitle,
	onSubmit,
	expectedValue,
	pleaseMessage,
	warningMessage,
}: {
	title: string;
	submitTitle: string;
	onSubmit: FormEventHandler<Element> | undefined;
	expectedValue: string;
	pleaseMessage: string;
	warningMessage?: string;
}) {
	const [userValue, setUserValue] = useState<string>("");
	return (
		<span className="h-screen flex items-center justify-center">
			<div className="px-5 py-2 border-collapse items-center flex flex-col rounded-md shadow-xl/10 ring ring-gray-100">
				<h1 className="text-3xl text-center border-b mb-5">{title}</h1>
				<p>{pleaseMessage}</p>
				{warningMessage ? (
					<p className="text-red-600">{warningMessage}</p>
				) : null}
				<form action="/" onSubmit={onSubmit} className="flex flex-col p-2">
					<div
						key={"check"}
						className="my-2 rounded-md border border-gray-400 shadow inset-shadow-sm inset-shadow-black/50 justify-items-center"
					>
						<Input
							key={"check"}
							type="text"
							name={"check"}
							required={true}
							onChange={(e) => {
								e.preventDefault();
								setUserValue(e.target.value);
							}}
							content=""
							placeholder={undefined}
							blockPaste={true}
						/>
					</div>
					<div className="flex justify-center m-3">
						{expectedValue === userValue ? (
							<button
								type="submit"
								className="cursor-pointer bg-blue-600 text-white font-medium min-w-3xs px-6 py-3 rounded-lg transition max-w-3xs my-2 hover:bg-blue-800 active:inset-shadow-sm/70"
							>
								{submitTitle}
							</button>
						) : (
							<button
								type="submit"
								disabled={true}
								className="cursor-not-allowed bg-gray-600 text-white font-medium min-w-3xs px-6 py-3 rounded-lg transition max-w-3xs my-2"
							>
								{submitTitle}
							</button>
						)}
					</div>
				</form>
			</div>
		</span>
	);
}
