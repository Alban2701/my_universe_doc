export interface TextBlockInterface {
	id: number;
	title: string | null;
	content: string | null;
	position: number;
	creator_id: number;
	entity_id: number;
}

export interface TextBlockPayloadInterface {
	title: string | null;
	content: string | null;
	position: number;
	entity_id: number;
}

export interface TextBlocksPayloadInterface {
	to_create: TextBlockInterface[];
	to_delete: TextBlockInterface[];
	to_move: TextBlockInterface[];
	to_update: TextBlockInterface[];
}
