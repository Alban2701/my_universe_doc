import { closestCenter, DndContext, type DragEndEvent } from "@dnd-kit/core";
import {
	arrayMove,
	SortableContext,
	verticalListSortingStrategy,
} from "@dnd-kit/sortable";
import { useEffect, useState } from "react";
import type { TextBlockInterface } from "@/src/types/text_blocks";
import { SortableTextBlock } from "./TextBlocks";

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
