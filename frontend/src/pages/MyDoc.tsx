import { useCallback, useEffect, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import Header from "../components/Shared/Header";
import PanelEntity from "../components/UI/Panels/PanelEntity";
import PanelSettings from "../components/UI/Panels/PanelSettings";
import PanelUniverse from "../components/UI/Panels/PanelUniverse";
import DragAndDropTextBlock from "../components/UI/TextBlock/ListTextBlocks";
import type { EntityInterface } from "../types/entity";
import type { UniverseInterface } from "../types/universe";

function MyDoc() {
	const { universeId, entityId } = useParams<{
		universeId: string;
		entityId: string;
	}>();
	const [selectedUniverse, setSelectedUniverse] = useState<UniverseInterface>();
	const [selectedEntity, setSelectedEntity] = useState<EntityInterface>();
	const [title, setTitle] = useState<string>("");
	const navigate = useNavigate();
	const location = useLocation();

	const handlePreviousButton = useCallback(() => {
		if (selectedEntity) {
			if (selectedEntity.parent !== null && selectedEntity !== undefined) {
				navigate(`/mydoc/${universeId}/entities/${selectedEntity.parent}`);
			} else {
				navigate(`/mydoc/${universeId}`);
			}
		} else {
			navigate(`/mydoc`);
		}
	}, [selectedEntity, universeId, navigate]);

	const handleUniverseEntityUpdate = useCallback(
		(selectedEntity?: EntityInterface) => {
			if (selectedEntity) {
				navigate(`/mydoc/${universeId}/entities/${selectedEntity.id}`);
			}
		},
		[universeId, navigate],
	);

	const handleEntityDeleted = useCallback(() => {
		selectedEntity?.parent
			? navigate(`/mydoc/${universeId}/entities/${selectedEntity?.parent}`)
			: navigate(`mydoc/${universeId}`);
	}, [universeId, selectedEntity, navigate]);

	const handleUniverseDeleted = useCallback(
		() => navigate(`/mydoc`),
		[navigate],
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
		} else {
			setSelectedUniverse(undefined);
		}
		if (entityId) {
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
		} else {
			setSelectedEntity(undefined);
		}
	}, [universeId, entityId]);

	useEffect(() => {
		console.log(selectedEntity, selectedUniverse);
		if (selectedUniverse) {
			if (selectedEntity) {
				setTitle(selectedEntity.name);
			} else {
				setTitle("Choose a entity");
			}
		} else {
			setTitle("Choose a universe");
		}
	});

	return (
		<div className="h-screen flex flex-col">
			<Header />
			<div className="flex flex-row h-full">
				<div className="basis-1/7 h-full">
					{selectedUniverse || selectedEntity ? (
						<PanelEntity
							universeId={universeId || ""}
							entityId={entityId || ""}
							entityParentId={selectedEntity ? selectedEntity.parent : null}
							onEntityUpdate={handleUniverseEntityUpdate}
							onPreviousButton={handlePreviousButton}
						/>
					) : (
						<PanelUniverse />
					)}
				</div>
				<span className="flex flex-row flex-auto justify-center-safe">
					<div className="overflow-y-clip w-full">
						<h1 className="text-center text-4xl">{title}</h1>
						{entityId && <DragAndDropTextBlock entityId={entityId} />}
					</div>
				</span>
				<span className="basis-1/7">
					<PanelSettings
						selectedUniverse={selectedUniverse}
						selectedEntity={selectedEntity}
						onUniverseEntityUpdated={handleUniverseEntityUpdate}
						onUniverseDeleted={handleUniverseDeleted}
						onEntityDeleted={handleEntityDeleted}
					/>
				</span>
			</div>
		</div>
	);
}

export default MyDoc;
