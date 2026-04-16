import React, { useEffect, useState } from "react";
import type { Entity } from "@/src/types/entity";
import EntityPath from "./entity_components/EntityPath";
import { useNavigate } from "react-router-dom";
import CreateEntity from "../Modals/CreateEntity";

function PanelEntity({
	universeId,
	onEntityUpdate,
}: {
	universeId: string;
	onEntityUpdate: (selectedEntity?: Entity) => void;
}) {
	const [entities, setEntities] = useState<Entity[]>([]);
	const [selectedEntity, setSelectedEntity] = useState<Entity>();
	const [loading, setLoading] = useState<boolean>(true);
	const [error, setError] = useState<string | null>(null);
	const [refresh, setRefresh] = useState<boolean>(false);
	const navigate = useNavigate();
	// biome-ignore lint/correctness/useExhaustiveDependencies: <we need the refresh dependancy to refresh the view once we created a doc. Otherwise we don't want to do anything with the refresh variable>
	useEffect(() => {
		if (!universeId) return;
		const fetchEntities = async () => {
			try {
				setLoading(true);
				const response = await fetch(`/api/entity/${universeId}/children`, {
					credentials: "include",
					method: "GET",
				});
				if (!response.ok) {
					throw new Error("An error occurred while fetching entities");
				}
				const data = await response.json();
				setEntities(data);
				setError(null);
			} catch (err) {
				setError(err instanceof Error ? err.message : "Unknown error");
				console.error("Error fetching entities:", err);
			} finally {
				setLoading(false);
			}
		};

		fetchEntities();
	}, [universeId, refresh]);

	if (loading) {
		return <div className="text-sm text-gray-500">Loading...</div>;
	}

	if (error) {
		return <div className="text-sm text-red-500">Error: {error}</div>;
	}

	const handleEntityCreated = () => {
		setRefresh(!refresh);
	};

	return (
		<div className="border-b border-r flex flex-col h-full">
			<h1 className="text-3xl text-center border-b mb-5">Your Docs</h1>
			<ul className="m-2 overflow-y-auto">
				{entities.map((entity) => (
					<li key={entity.id}>
						<button
							type="button"
							onClick={() => {
								setSelectedEntity(entity);
								onEntityUpdate(entity);
								navigate(`/universes/${universeId}/entities/${entity.id}`);
							}}
							className="hover:cursor-pointer border-y my-1 p-1 w-full"
						>
							{entity.name}
						</button>
					</li>
				))}
			</ul>
			<div className="place-self-center mt-auto mb-5 p-2 border-t">
				<CreateEntity
					onEntityCreated=}}
					universeId={0}
					parentId={undefined}
				></CreateEntity>
			</div>
		</div>
	);
}

export default PanelEntity;
