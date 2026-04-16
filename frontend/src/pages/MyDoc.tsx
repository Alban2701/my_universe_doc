import React, { useCallback, useEffect, useState } from "react";
import type { UniverseInterface } from "../types/universe";
import PanelUniverse from "../components/UI/Panels/PanelUniverse";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import PanelSettings from "../components/UI/Panels/PanelSettings";
import Header from "../components/Shared/Header";
import type { Entity } from "../types/entity";
import PanelEntity from "../components/UI/Panels/PanelEntity"; // Assure-toi d'importer PanelEntity

function MyDoc() {
	const { universeId, entityId } = useParams<{
		universeId: string;
		entityId: string;
	}>();
	const [selectedUniverse, setSelectedUniverse] = useState<UniverseInterface>();
	const [selectedEntity, setSelectedEntity] = useState<Entity>();
	const navigate = useNavigate();
	const location = useLocation();

	const handleUniverseUpdate = useCallback(
		(selectedUniverse?: UniverseInterface) => {
			if (selectedUniverse) {
				setSelectedUniverse(selectedUniverse);
				navigate(`/universes/${selectedUniverse.id}`);
			}
		},
		[navigate],
	);

	const handleEntityUpdate = useCallback(
		(selectedEntity?: Entity) => {
			if (selectedEntity) {
				setSelectedEntity(selectedEntity);
				navigate(`/universes/${universeId}/entities/${selectedEntity.id}`);
			}
		},
		[universeId, navigate],
	);

	useEffect(() => {
		const fetchIsLogin = async () => {
			try {
				const response = await fetch("/api/user/logged-in");
				if (!response.ok) {
					navigate("/login", {
						replace: true,
						state: { from: location.pathname },
					});
				}
			} catch (e) {
				console.log(e);
			}
		};
		fetchIsLogin();
	}, [location.pathname, navigate]);

	useEffect(() => {
		if (universeId) {
			const fetchUniverse = async () => {
				try {
					const response = await fetch(`/api/universe/${universeId}`, {
						credentials: "include",
						method: "GET",
					});
					if (!response.ok) throw new Error("Universe not found");
					const data = await response.json();
					setSelectedUniverse(data);
				} catch (err) {
					console.error("Error fetching universe:", err);
				}
			};
			fetchUniverse();
		}
	}, [universeId]);

	useEffect(() => {
		if (entityId && universeId) {
			const fetchEntity = async () => {
				try {
					const response = await fetch(`/api/entity/${entityId}`, {
						credentials: "include",
						method: "GET",
					});
					if (!response.ok) throw new Error("Entity not found");
					const data = await response.json();
					setSelectedEntity(data);
				} catch (err) {
					console.error("Error fetching entity:", err);
				}
			};
			fetchEntity();
		}
	}, [entityId, universeId]);

	return (
		<div className="h-screen flex flex-col">
			<Header />
			<div className="flex flex-row h-full">
				<div className="basis-1/7 h-full">
					{selectedEntity ? (
						<PanelEntity
							universeId={universeId || ""}
							onEntityUpdate={handleEntityUpdate}
						/>
					) : (
						<PanelUniverse
							universeId={universeId}
							onUniverseUpdate={handleUniverseUpdate}
						/>
					)}
				</div>
				<span className="flex flex-row flex-auto justify-center-safe">
					<div className="overflow-y-clip">
						<h1 className="text-4xl">
							{selectedUniverse ? selectedUniverse.name : "Select a universe"}
						</h1>
						{selectedEntity && (
							<p className="text-xl mt-2">
								Current entity: {selectedEntity.name}
							</p>
						)}
					</div>
				</span>
				<span className="basis-1/7">
					<PanelSettings universeId={universeId} />
				</span>
			</div>
		</div>
	);
}

export default MyDoc;
