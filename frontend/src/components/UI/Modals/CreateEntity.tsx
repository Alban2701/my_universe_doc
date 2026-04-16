import React from "react";
import { useState } from "react";
import BaseForm from "../Forms/BaseForm";
import BaseModal from "./BaseModal";
import RectangularButton from "../Button/Rectangular.button";

interface EntityPayload {
	name: string;
	description: string;
	parent: number | undefined;
	universe_id: number;
}

function CreateEntity({
	onEntityCreated,
	universeId,
	parentId,
}: {
	onEntityCreated: () => void;
	universeId: number;
	parentId: number | undefined;
}) {
	const [isOpen, setIsOpen] = useState<boolean>(false);
	const [entityName, setEntityName] = useState<string>("");
	const [entityNotDiscoveredName, setEntityNotDiscoveredName] =
		useState<string>("");

	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();

		const payload: EntityPayload = {
			name: entityName,
			description: entityNotDiscoveredName,
			parent: parentId,
			universe_id: universeId,
		};
		try {
			console.log(payload);
			const response = await fetch("/api/entity/", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(payload),
				credentials: "include",
			});
			if (!response.ok) throw new Error("The entity could not be created");
			const data = await response.json();
			console.log("Réponse Api :", data);
			onEntityCreated();
		} catch (error) {
			console.log(error);
		} finally {
			setIsOpen(false);
		}
	};
	return (
		<div>
			<RectangularButton
				text={"Create Universe"}
				onClick={() => setIsOpen(true)}
			/>
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
								name: "entityName",
								placeholder: "Your entity's name",
								required: true,
								onChange: (e) => {
									setEntityName(e.target.value);
								},
							},
							{
								type: "text",
								name: "entityNotDiscoveredName",
								placeholder: "Your not discovered entity's name ",
								required: true,
								onChange: (e) => {
									setEntityName(e.target.value);
								},
							},
						]}
					/>
				</BaseModal>
			)}
		</div>
	);
}

export default CreateEntity;
