import { closestCenter, DndContext, type DragEndEvent } from "@dnd-kit/core";
import {
	arrayMove,
	SortableContext,
	verticalListSortingStrategy,
} from "@dnd-kit/sortable";
import { useCallback, useEffect, useState } from "react";
import type {
	TextBlockInterface,
	TextBlocksPayloadInterface,
} from "@/src/types/text_blocks";
import { SortableTextBlock } from "./TextBlocks";
import { itemsEqual } from "@dnd-kit/sortable/dist/utilities";

function DnDTextBlock({ entityId }: { entityId?: string }) {
	const [textBlocks, setTextBlocks] = useState<TextBlockInterface[]>([]);
	const [loadedTextBlocks, setLoadedTextBlocks] = useState<
		TextBlockInterface[]
	>([]);
	const [_updateIsActive, setUpdateIsActive] = useState<boolean>(false);
	const [_textBlocksPayload, setTextBlocksPayload] =
		useState<TextBlocksPayloadInterface>();

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
				setLoadedTextBlocks(data);
				// console.log(data);
			} catch (err) {
				console.error("Error while fetching text blocks", err);
			}
		};
		fetchTextBlocks();
	}, [entityId]);

	useEffect(() => {
		setUpdateIsActive(textBlocks === loadedTextBlocks);
	}, [textBlocks, loadedTextBlocks]);

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

	useEffect(() => {
		const partialPayload: Omit<TextBlocksPayloadInterface, "to_delete"> = {
			to_create: [],
			to_move: [],
			to_update: [],
		};
		textBlocks.forEach((tb) => {
			const loaded = loadedTextBlocks.find((loadedTb) => tb.id === loadedTb.id);

			if (!loaded) {
				partialPayload.to_create.push(tb);
			} else if (JSON.stringify(loaded) !== JSON.stringify(tb)) {
				const { position: _loaded_position, ...loaded_no_pos } = loaded;
				const { position: _tb_position, ...tb_no_pos } = tb;
				if (
					loaded.position !== tb.position &&
					JSON.stringify(loaded_no_pos) === JSON.stringify(tb_no_pos)
				) {
					partialPayload.to_move.push(tb);
				} else {
					partialPayload.to_update.push(tb);
				}
			}
		});

		const to_delete = loadedTextBlocks.filter((ltb) => {
			return !textBlocks.some((tb) => tb.id === ltb.id);
		});
		setTextBlocksPayload({
			...partialPayload,
			to_delete: to_delete,
		});
	}, [loadedTextBlocks, textBlocks]);

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

export default DnDTextBlock;
