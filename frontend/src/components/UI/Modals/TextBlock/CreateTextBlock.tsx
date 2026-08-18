import { useState } from "react";
import RectangularButton from "../../Button/Rectangular.button";
import BaseForm from "../../Forms/BaseForm";
import type { InputInterface } from "../../Forms/Input";
import BaseModal from "../BaseModal";
import type { TextBlockPayloadInterface } from "@/src/types/text_blocks";
import AddTextBlockButton from "../../Button/AddTextBlockButton";

function CreateTextBlock({
	onTextBlockCreated,
	entityId,
	position,
}: {
	onTextBlockCreated: () => void;
	entityId: number;
	position: number;
}) {
	const [isOpen, setIsOpen] = useState<boolean>(false);
	const [textBlockTitle, setTextBlockTitle] = useState<string | undefined>(
		undefined,
	);
	const [textBlockContent, setTextBlockContent] = useState<string | undefined>(
		undefined,
	);

	const inputs: InputInterface[] = [
		{
			type: "text",
			name: "textBlockTitle",
			placeholder: "The Textblock's title",
			required: true,
			onChange: (e) => {
				setTextBlockTitle(e.target.value);
			},
			content: undefined,
		},
		{
			type: "text",
			name: "textBlockContent",
			placeholder: "The content of the textblock (can be set later)",
			required: false,
			onChange: (e) => {
				setTextBlockContent(e.target.value);
			},
			content: undefined,
		},
	];

	const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		if (!textBlockTitle) throw new Error("Textblock's title must be set");
		const payload: TextBlockPayloadInterface = {
			title: textBlockTitle,
			content: textBlockContent ? textBlockContent : "",
			position: position,
			entity_id: entityId,
		};
		try {
			console.log(payload);
			const response = await fetch("/api/text-block/", {
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
			onTextBlockCreated();
		} catch (error) {
			console.log(error);
		} finally {
			setIsOpen(false);
		}
	};
	return (
		<div>
			<AddTextBlockButton onClick={() => setIsOpen(true)} />
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
						title={"Create a new TextBlock"}
						submitTitle={"Create"}
						onSubmit={handleSubmit}
						inputs={inputs}
					/>
				</BaseModal>
			)}
		</div>
	);
}

export default CreateTextBlock;
