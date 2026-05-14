import { useState } from "react";
import type { UniverseInterface } from "@/src/types/universe";
import RectangularButton from "../../Button/Rectangular.button";
import BaseForm from "../../Forms/BaseForm";
import DeleteForm from "../../Forms/DeleteForm";
import BaseModal from "../BaseModal";

function DeleteUniverse({
	universe,
	onUniverseDeleted,
}: {
	universe: UniverseInterface;
	onUniverseDeleted: () => void;
}) {
	const [isOpen, setIsOpen] = useState<boolean>(false);
	const [deleting, setDeleting] = useState<boolean>(false);

	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		try {
			setDeleting(true);
			const response = await fetch(`/api/universe/${universe.id}`, {
				method: "DELETE",
				headers: {
					"Content-Type": "application/json",
				},
				credentials: "include",
			});
			if (!response.ok) throw new Error("The doc could not be deleted");
			const data = await response.json();
			console.log("Api Response :", data);
			onUniverseDeleted();
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
				text={"Delete Universe"}
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
						title={"Delete Universe"}
						submitTitle={deleting ? "Deleting" : "Delete"}
						onSubmit={handleSubmit}
						expectedValue={universe.name}
						pleaseMessage={`You are going to delete your universe. Please, copy the following in the input box : ${universe.name}`}
						warningMessage="Once submited, anybody will be able to restore the deleted datas"
					></DeleteForm>
				</BaseModal>
			)}
		</div>
	);
}

export default DeleteUniverse;
