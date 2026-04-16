import React from "react";
import { useState } from "react";
import BaseForm from "../Forms/BaseForm";
import BaseModal from "./BaseModal";
import RectangularButton from "../Button/Rectangular.button";

interface UniversePayload {
	name: string;
	description: string;
}

function CreateUniverse({
	onUniverseCreated,
}: {
	onUniverseCreated: () => void;
}) {
	const [isOpen, setIsOpen] = useState<boolean>(false);
	const [docName, setDocName] = useState<string>("");
	const [docDescription, setDocDescription] = useState<string>("");

	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();

		const payload: UniversePayload = {
			name: docName,
			description: docDescription,
		};
		try {
			console.log(payload);
			const response = await fetch("/api/universe/", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(payload),
				credentials: "include",
			});
			if (!response.ok) throw new Error("The doc could not be created");
			const data = await response.json();
			console.log("Réponse Api :", data);
			onUniverseCreated();
		} catch (error) {
			console.log(error);
		} finally {
			setIsOpen(false);
		}
	};
	return (
		<div>
			<RectangularButton text={"Create Universe"} onClick={() => setIsOpen(true)} />
			{isOpen && (
				<BaseModal>
					<div className="flex">
						<button
							type="button"
							className="flex bg-red-700 text-white hover:cursor-pointer rounded-lg px-2 items-center justify-center"
							onClick={() => setIsOpen(false)}
						>
							Cancel
						</button>
					</div>
					<BaseForm
						title={"Create a new doc"}
						submitTitle={"Create"}
						onSubmit={handleSubmit}
						inputs={[
							{
								type: "text",
								name: "docName",
								placeholder: "Your new doc's name",
								required: true,
								onChange: (e) => {
									setDocName(e.target.value);
								},
							},
							{
								type: "text",
								name: "docDescription",
								placeholder: "Your new doc's description",
								required: false,
								onChange: (e) => {
									setDocDescription(e.target.value);
								},
							},
						]}
					/>
				</BaseModal>
			)}
		</div>
	);
}

export default CreateUniverse;
