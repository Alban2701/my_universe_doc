import { useEffect, useState } from "react";
import type { EntityInterface } from "@/src/types/entity";
import RectangularButton from "../../Button/Rectangular.button";
import BaseForm from "../../Forms/BaseForm";
import BaseModal from "../BaseModal";

interface EntityPayload {
	name: string;
	notDiscoveredName: string;
}

function UpdateEntity({
	entity,
	onEntityUpdated,
}: {
	entity: EntityInterface;
	onEntityUpdated: () => void;
}) {
	const [isOpen, setIsOpen] = useState<boolean>(false);
	const [entityName, setEntityName] = useState<string>("");
	const [entityNotDiscoveredName, setEntityNotDiscoveredName] =
		useState<string>("");

	useEffect(() => {
		setEntityName(entity.name);
		setEntityNotDiscoveredName(
			entity.not_discovered_name ? entity.not_discovered_name : "",
		);
	}, [entity]);
	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();

		const payload: EntityPayload = {
			name: entityName,
			notDiscoveredName: entityNotDiscoveredName,
		};
		try {
			console.log(payload);
			const response = await fetch(`/api/entity/${entity.id}`, {
				method: "PATCH",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(payload),
				credentials: "include",
			});
			if (!response.ok) throw new Error("The entity could not be updated");
			const data = await response.json();
			console.log("Api Response :", data);
			onEntityUpdated();
		} catch (error) {
			console.log(error);
		} finally {
			setIsOpen(false);
		}
	};
	return (
		<div>
			<RectangularButton
				text={"Update Entity"}
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
						title={"Update an entity"}
						submitTitle={"Update"}
						onSubmit={handleSubmit}
						inputs={[
							{
								type: "text",
								name: "entityName",
								placeholder: "Your new entity's name",
								required: true,
								onChange: (e) => {
									setEntityName(e.target.value);
								},
								content: entityName,
							},
							{
								type: "text",
								name: "entityNotDiscoverdName",
								placeholder: "Your new entity's not discovered name",
								required: false,
								onChange: (e) => {
									setEntityNotDiscoveredName(e.target.value);
								},
								content: entityNotDiscoveredName,
							},
						]}
					/>
				</BaseModal>
			)}
		</div>
	);
}

export default UpdateEntity;
