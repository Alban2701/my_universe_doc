import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

import TextareaAutosize from "react-textarea-autosize";

interface SortableTextAreasProps {
	id: number;
	value: string;
	title: string | null;
	onChange: (id: number, newValue: string) => void;
}

export function SortableTextBlock({
	id,
	value,
	title,
	onChange,
}: SortableTextAreasProps) {
	const {
		attributes,
		listeners,
		setNodeRef,
		transform,
		transition,
		isDragging,
	} = useSortable({ id });

	const style = {
		transform: CSS.Transform.toString(transform),
		transition,
		backgroundColor: isDragging ? "#dbeafe" : "transparent",
		borderColor: isDragging ? "#ff0000" : "#000000",
		boxShadow: isDragging ? "0 0 10px rgba(0, 0, 0, 0.2)" : "none",
		opacity: isDragging ? 0.5 : 1,
	};

	const drag_handle_style = {
		// transform: CSS.Transform.toString(transform),
		// transition,
		cursor: isDragging ? "grabbing" : "grab",
	};

	return (
		<div
			ref={setNodeRef}
			style={style}
			className="flex flex-col mb-2 p-2 rounded-md w-full"
		>
			<h3 className="text-xl mb-2">{title}</h3>
			<div className="flex flex-row items-center ml-2 p-1 bg-gray-200 rounded w-full">
				<TextareaAutosize
					className="flex-1 p-2 w-full border rounded-md focus:outline-none"
					value={value}
					onChange={(e) => onChange(id, e.target.value)}
					name="textArea"
					title={title ? title : "no title"}
					id={id.toString()}
				/>
				<p
					{...attributes}
					{...listeners}
					style={drag_handle_style}
					className="mx-2"
				>
					☰
				</p>
			</div>
		</div>
	);
}
