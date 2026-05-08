import { useCallback, useEffect, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import Header from "../components/Shared/Header";
import PanelEntity from "../components/UI/Panels/PanelEntity";
import PanelSettings from "../components/UI/Panels/PanelSettings";
import PanelUniverse from "../components/UI/Panels/PanelUniverse";
import DragAndDropTextBlock from "../components/UI/TextBlock/ListTextBlocks";
import type { Entity } from "../types/entity";
import type { UniverseInterface } from "../types/universe";

function MyDoc() {
	const { universeId, entityId } = useParams<{
		universeId: string;
		entityId: string;
	}>();
	const [selectedUniverse, setSelectedUniverse] = useState<UniverseInterface>();
	const [selectedEntity, setSelectedEntity] = useState<Entity>();
	const navigate = useNavigate();
	const location = useLocation();

	const handleUniverseUpdate = useCallback(() => {
		console.log("previous buttons");
		console.log(selectedEntity);
		console.log(selectedUniverse);
		if (selectedEntity?.parent) {
			navigate(`/mydoc/${universeId}/entities/${selectedEntity.parent}`);
		} else if (selectedUniverse) {
			setSelectedUniverse(selectedUniverse);
			navigate(`/mydoc/${selectedUniverse.id}`);
		} else {
			setSelectedEntity(undefined);
			setSelectedUniverse(undefined);
			navigate(`/mydoc`);
		}
	}, [navigate, selectedEntity, universeId, selectedUniverse]);

	const handleEntityUpdate = useCallback(
		(selectedEntity?: Entity) => {
			if (selectedEntity) {
				setSelectedEntity(selectedEntity);
				navigate(`/mydoc/${universeId}/entities/${selectedEntity.id}`);
			}
		},
		[universeId, navigate],
	);

	useEffect(() => {
		const fetchIsLogin = async () => {
			try {
				const response = await fetch("/api/user/me");
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
		if (universeId && !entityId) {
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
	}, [universeId, entityId]);

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
					{selectedUniverse || selectedEntity ? (
						<PanelEntity
							universeId={universeId || ""}
							entityId={entityId || ""}
							entityParentId={
								selectedEntity ? selectedEntity.parent?.toString() : undefined
							}
							onEntityUpdate={handleEntityUpdate}
							onUnselectUniverse={handleUniverseUpdate}
						/>
					) : (
						<PanelUniverse
							universeId={universeId}
							onUniverseUpdate={handleUniverseUpdate}
						/>
					)}
				</div>
				<span className="flex flex-row flex-auto justify-center-safe">
					<div className="overflow-y-clip w-full">
						<h1 className="text-center text-4xl">
							{selectedEntity ? selectedEntity.name : "Select a universe"}
						</h1>
						{selectedEntity && <DragAndDropTextBlock entityId={entityId} />}
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
