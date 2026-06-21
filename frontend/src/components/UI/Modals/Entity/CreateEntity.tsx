import { useState } from "react";
import RectangularButton from "../../Button/Rectangular.button";
import BaseForm from "../../Forms/BaseForm";
import type { InputInterface } from "../../Forms/Input";
import BaseModal from "../BaseModal";

interface EntityPayload {
	name: string;
	description: string;
	parent: number | null;
	universe_id: number;
}

function CreateEntity({
	onEntityCreated,
	universeId,
	parentId,
}: {
	onEntityCreated: () => void;
	universeId: number;
	parentId: number | null;
}) {
	const [isOpen, setIsOpen] = useState<boolean>(false);
	const [entityName, setEntityName] = useState<string>("");
	const [entityNotDiscoveredName, setEntityNotDiscoveredName] =
		useState<string>("");

	const inputs: InputInterface[] = [
		{
			type: "text",
			name: "entityName",
			placeholder: "Your entity's name",
			required: true,
			onChange: (e) => {
				setEntityName(e.target.value);
			},
			content: undefined,
		},
		{
			type: "text",
			name: "entityNotDiscoveredName",
			placeholder: "Your not discovered entity's name ",
			required: false,
			onChange: (e) => {
				setEntityNotDiscoveredName(e.target.value);
			},
			content: undefined,
		},
	];

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
			console.log("Api Response :", data);
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
				text={"Create Entity"}
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
						title={"Create a new entity"}
						submitTitle={"Create"}
						onSubmit={handleSubmit}
						inputs={inputs}
					/>
				</BaseModal>
			)}
		</div>
	);
}

export default CreateEntity;
