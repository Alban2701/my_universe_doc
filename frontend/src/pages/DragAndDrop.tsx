// biome-ignore lint/correctness/noUnusedImports: <need React>
import React, { useState } from "react";
import { DndContext, type DragEndEvent, closestCenter } from "@dnd-kit/core";
import {
	SortableContext,
	verticalListSortingStrategy,
	arrayMove,
} from "@dnd-kit/sortable";
import { SortableTextAreas } from "../components/UI/TextBlock/Tests/SortableTextArea";

function DragAndDrop() {
	const [textAreas, setTextAreas] = useState([
		{ id: 1, content: "Texte 1" },
		{ id: 2, content: "Texte 2" },
	]);

	const handleDragEnd = (event: DragEndEvent) => {
		const { active, over } = event;
		if (active.id !== over?.id) {
			setTextAreas((items) => {
				const oldIndex = items.findIndex((item) => item.id === active.id);
				const newIndex = items.findIndex((item) => item.id === over?.id);
				return arrayMove(items, oldIndex, newIndex);
			});
		}
	};

	const handleTextChange = (id: number, newValue: string) => {
		setTextAreas((items) =>
			items.map((item) =>
				item.id === id ? { ...item, content: newValue } : item,
			),
		);
	};

	return (
		<DndContext collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
			<SortableContext items={textAreas} strategy={verticalListSortingStrategy}>
				{textAreas.map((item) => (
					<SortableTextAreas
						key={item.id}
						id={item.id}
						value={item.content}
						onChange={handleTextChange}
					/>
				))}
			</SortableContext>
		</DndContext>
	);
}

export default DragAndDrop;
