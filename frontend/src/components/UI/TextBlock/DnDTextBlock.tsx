import { closestCenter, DndContext, type DragEndEvent } from "@dnd-kit/core";
import {
	arrayMove,
	SortableContext,
	verticalListSortingStrategy,
} from "@dnd-kit/sortable";
import { useMemo, useEffect, useState, useCallback } from "react";
import type {
	TextBlockInterface,
	TextBlocksPayloadInterface,
} from "@/src/types/text_blocks";
import { SortableTextBlock } from "./TextBlocks";
import AddTextBlockButton from "../Button/AddTextBlockButton";
import CreateTextBlock from "../Modals/TextBlock/CreateTextBlock";

function DnDTextBlock({
	entityId,
	onTextBlockUpdate,
}: {
	entityId?: string;
	onTextBlockUpdate: () => void;
}) {
	const [textBlocks, setTextBlocks] = useState<TextBlockInterface[]>([]);
	const [loadedTextBlocks, setLoadedTextBlocks] = useState<
		TextBlockInterface[]
	>([]);
	const [refresh, setRefresh] = useState<number>(0);

	// biome-ignore lint/correctness/useExhaustiveDependencies: <refresh>
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
	}, [entityId, refresh]);

	const addTextBlock = async (position: number) => {
		try {
			const response = await fetch(`/api/text-block/`, {
				credentials: "include",
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ position: position, entityId: entityId }),
			});
			if (!response.ok) throw new Error("The textblock could not be created");
			const data = response.json();
			console.log(`API response :\n${data}`);
			setRefresh((prev) => prev + 1);
		} catch (err) {
			console.error(err);
		}
	};

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

	const handleTextChange = useCallback((id: number, newValue: string) => {
		setTextBlocks((items) =>
			items.map((item) =>
				item.id === id ? { ...item, content: newValue } : item,
			),
		);
	}, []);

	const textBlockPayload = useMemo<TextBlocksPayloadInterface>(() => {
		const payload: TextBlocksPayloadInterface = {
			to_create: [],
			to_move: [],
			to_update: [],
			to_delete: [],
		};
		textBlocks.forEach((tb) => {
			const loaded = loadedTextBlocks.find((loadedTb) => tb.id === loadedTb.id);

			if (!loaded) {
				payload.to_create.push(tb);
			} else if (JSON.stringify(loaded) !== JSON.stringify(tb)) {
				const { position: _loaded_position, ...loaded_no_pos } = loaded;
				const { position: _tb_position, ...tb_no_pos } = tb;
				if (
					loaded.position !== tb.position &&
					JSON.stringify(loaded_no_pos) === JSON.stringify(tb_no_pos)
				) {
					payload.to_move.push(tb);
				} else {
					payload.to_update.push(tb);
				}
			} else {
				payload.to_delete = loadedTextBlocks.filter((ltb) => {
					return !textBlocks.some((tb) => tb.id === ltb.id);
				});
			}
		});
		return payload;
	}, [loadedTextBlocks, textBlocks]);

	const updateIsActive = Object.values(textBlockPayload).some(
		(list) => list.length > 0,
	);

	return (
		<span className="transition-all duration-300">
			<DndContext collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
				<SortableContext
					items={textBlocks}
					strategy={verticalListSortingStrategy}
				>
					{textBlocks.map((item) => (
						<div key={item.id} className="group flex flex-col items-center">
							<span className="invisible opacity-0 transition-all duration-500 w-2/7 group-hover:visible group-hover:opacity-70 hover:opacity-100 hover:w-5/7">
								<CreateTextBlock
									onTextBlockCreated={() => setRefresh((prev) => prev + 1)}
									entityId={Number(entityId)}
									position={item.position}
								/>
							</span>
							<SortableTextBlock
								id={item.id}
								value={item.content ? item.content : "no-content"}
								title={item.title}
								onChange={handleTextChange}
							/>
							<span className="mt-2 h-0 invisible opacity-0 transition-all duration-500 w-2/7 group-hover:visible group-hover:opacity-70 hover:opacity-100 hover:w-5/7">
								<CreateTextBlock
									onTextBlockCreated={() => setRefresh((prev) => prev + 1)}
									entityId={Number(entityId)}
									position={item.position}
								/>
							</span>
						</div>
					))}
				</SortableContext>
			</DndContext>
		</span>
	);
}

export default DnDTextBlock;
