import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import type { Entity as EntityInterface } from "@/src/types/entity";
import type { UniverseInterface } from "@/src/types/universe";
import CreateEntity from "../Modals/CreateEntity";
import EntityPath from "./entity_components/EntityPath";

function PanelEntity({
	universeId,
	entityId,
	entityParentId,
	onEntityUpdate,
	onPreviousButton,
}: {
	universeId: string;
	entityId: string;
	entityParentId: number | null;
	onEntityUpdate: (selectedEntity?: EntityInterface) => void;
	onPreviousButton: (selectedUniverse?: UniverseInterface) => void;
}) {
	const [entities, setEntities] = useState<EntityInterface[]>([]);
	const [loading, setLoading] = useState<boolean>(true);
	const [error, setError] = useState<string | null>(null);
	const [refresh, setRefresh] = useState<boolean>(false);
	const navigate = useNavigate();

	// biome-ignore lint/correctness/useExhaustiveDependencies: <need Refresh>
	useEffect(() => {
		if (!(universeId || entityId)) return;
		const fetchEntityChildren = async () => {
			try {
				setLoading(true);
				const response = entityId
					? await fetch(`/api/entity/${entityId}/direct-children`, {
							credentials: "include",
							method: "GET",
						})
					: await fetch(`/api/universe/${universeId}/first-entities`, {
							credentials: "include",
							method: "GET",
						});
				if (!response.ok) {
					throw new Error("An error occurred while fetching entity's children");
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

		fetchEntityChildren();
	}, [universeId, entityId, refresh]);

	const handleEntityCreated = () => {
		setRefresh(!refresh);
	};

	if (loading) {
		return <div className="text-sm text-gray-500">Loading...</div>;
	}

	if (error) {
		return <div className="text-sm text-red-500">Error: {error}</div>;
	}

	return (
		<div className="border-b border-r flex flex-col h-full">
			<h1 className="text-3xl text-center border-b mb-5">Entities</h1>
			<button
				type="button"
				onClick={() => {
					onPreviousButton();
				}}
				name="PreviousButton"
				className="bg-red-600 w-25 ml-5 rounded-2xl text-white shadow hover:cursor-pointer hover:shadow-none hover:bg-red-900 overflow-hidden transition-all duration-300"
			>
				Previous
			</button>
			<ul className="m-2 overflow-y-auto">
				{entities.map((entity) => (
					<li key={entity.id}>
						<button
							type="button"
							onClick={() => {
								onEntityUpdate(entity);
								navigate(`/mydoc/${universeId}/entities/${entity.id}`);
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
					onEntityCreated={handleEntityCreated}
					universeId={Number(universeId)}
					parentId={entityParentId}
				></CreateEntity>
			</div>
		</div>
	);
}

export default PanelEntity;
