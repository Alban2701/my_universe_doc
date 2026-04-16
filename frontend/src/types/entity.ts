export interface Entity {
    id: number;
    name: string;
    not_discovered_name: string | null
    parent: number | null
    universe_id: number
    creator_id: number
}