// biome-ignore lint/correctness/noUnusedImports: <need React>
import React, { useState } from "react";
import { DndContext, type DragEndEvent, closestCenter } from "@dnd-kit/core";
import {
	SortableContext,
	verticalListSortingStrategy,
	arrayMove,
} from "@dnd-kit/sortable";
import { SortableTextBlock } from "../components/UI/TextBlock/TextBlocks";

function DragAndDrop() {
	const [textAreas, setTextAreas] = useState([
		{ id: 1, content: "Texte 1" },
		{ id: 2, content: "Texte 2" },
		{ id: 3, content: "Texte 3" },
		{ id: 4, content: "Texte 4" },
		{ id: 5, content: "Texte 5" },
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
					<SortableTextBlock
						key={item.id}
						id={item.id}
						value={item.content}
						onChange={handleTextChange}
						title={null}
					/>
				))}
			</SortableContext>
		</DndContext>
	);
}

export default DragAndDrop;
