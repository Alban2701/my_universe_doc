// biome-ignore lint/correctness/noUnusedImports: <need React>
import React, { useEffect, useState } from "react";
import { DndContext, type DragEndEvent, closestCenter } from "@dnd-kit/core";
import {
	SortableContext,
	verticalListSortingStrategy,
	arrayMove,
} from "@dnd-kit/sortable";
import { SortableTextBlock } from "./TextBlocks";
import type { TextBlockInterface } from "@/src/types/text_blocks";

function DragAndDropTextBlock({ entityId }: { entityId?: string }) {
	const [textBlocks, setTextBlocks] = useState<TextBlockInterface[]>([]);

	useEffect(() => {
		console.log("in DnD", textBlocks);
	}, [textBlocks]);

	useEffect(() => {
		const fetchTextBlocks = async () => {
			try {
				const response = await fetch(`/api/text-block/entity/${entityId}`, {
					credentials: "include",
					method: "GET",
				});
				if (!response.ok) throw new Error("Entity not found");
				const data = await response.json();
				setTextBlocks(data);
				console.log(data);
			} catch (err) {
				console.error("Error while fetching text blocks", err);
			}
		};
		fetchTextBlocks();
	}, [entityId]);

	const handleDragEnd = (event: DragEndEvent) => {
		const { active, over } = event;
		if (active.id !== over?.id) {
			setTextBlocks((items) => {
				const oldIndex = items.findIndex((item) => item.id === active.id);
				const newIndex = items.findIndex((item) => item.id === over?.id);
				return arrayMove(items, oldIndex, newIndex);
			});
		}
	};

	const handleTextChange = (id: number, newValue: string) => {
		setTextBlocks((items) =>
			items.map((item) =>
				item.id === id ? { ...item, content: newValue } : item,
			),
		);
	};

	return (
		<DndContext collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
			<SortableContext
				items={textBlocks}
				strategy={verticalListSortingStrategy}
			>
				{textBlocks.map((item) => (
					<SortableTextBlock
						key={item.id}
						id={item.id}
						value={item.content ? item.content : "no-content"}
						title={item.title}
						onChange={handleTextChange}
					/>
				))}
			</SortableContext>
		</DndContext>
	);
}

export default DragAndDropTextBlock;
