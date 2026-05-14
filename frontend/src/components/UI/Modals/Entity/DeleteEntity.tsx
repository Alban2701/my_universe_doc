import { useState } from "react";
import type { EntityInterface } from "@/src/types/entity";
import RectangularButton from "../../Button/Rectangular.button";
import DeleteForm from "../../Forms/DeleteForm";
import BaseModal from "../BaseModal";

function DeleteUniverse({
	entity,
	onEntityDeleted,
}: {
	entity: EntityInterface;
	onEntityDeleted: () => void;
}) {
	const [isOpen, setIsOpen] = useState<boolean>(false);
	const [deleting, setDeleting] = useState<boolean>(false);

	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		try {
			setDeleting(true);
			const response = await fetch(`/api/entity/${entity.id}`, {
				method: "DELETE",
				headers: {
					"Content-Type": "application/json",
				},
				credentials: "include",
			});
			if (!response.ok) throw new Error("The entity could not be deleted");
			const data = await response.json();
			console.log("Api Response :", data);
			onEntityDeleted();
		} catch (error) {
			console.log(error);
		} finally {
			setDeleting(false);
			setIsOpen(false);
		}
	};
	return (
		<div>
			<RectangularButton
				text={"Delete Entity"}
				onClick={() => setIsOpen(true)}
				color="red"
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
					<DeleteForm
						title={"Delete Entity"}
						submitTitle={deleting ? "Deleting" : "Delete"}
						onSubmit={handleSubmit}
						expectedValue={entity.name}
						pleaseMessage={`You are going to delete this entity and its entities' child. Please, copy the following in the input box : ${entity.name}`}
						warningMessage="Once submited, anybody will be able to restore the deleted datas"
					></DeleteForm>
				</BaseModal>
			)}
		</div>
	);
}

export default DeleteUniverse;
