import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
// biome-ignore lint/correctness/noUnusedImports: <need React>
import React from "react";

interface SortableTextAreasProps {
	id: number;
	value: string;
	onChange: (id: number, newValue: string) => void;
}

export function SortableTextAreas({
	id,
	value,
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
		borderColor: isDragging ? "#ff0000" : "none",
		boxShadow: isDragging ? "0 0 10px rgba(0, 0, 0, 0.2)" : "none",
		opacity: isDragging ? 0.5 : 1,
	};

	return (
		<textarea
			ref={setNodeRef}
			{...attributes}
			{...listeners}
			style={style}
			className="p-2 m-2 border rounded-md w-full"
			value={value}
			onChange={(e) => onChange(id, e.target.value)}
			name="textArea"
			id={id.toString()}
		></textarea>
	);
}
