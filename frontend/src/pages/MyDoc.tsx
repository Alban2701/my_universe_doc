import { useCallback, useEffect, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { fetchEntity, fetchTextBlock, fetchUniverse } from "@/src/fetchers";
import Header from "../components/Shared/Header";
import PanelEntity from "../components/UI/Panels/PanelEntity";
import PanelSettings from "../components/UI/Panels/PanelSettings";
import PanelUniverse from "../components/UI/Panels/PanelUniverse";
import DnDTextBlock from "../components/UI/TextBlock/DnDTextBlock";
import type { EntityInterface } from "../types/entity";
import type { TextBlockInterface } from "../types/text_blocks";
import type { UniverseInterface } from "../types/universe";

function MyDoc() {
	const { universeId, entityId } = useParams<{
		universeId: string;
		entityId: string;
	}>();
	const [selectedUniverse, setSelectedUniverse] = useState<UniverseInterface>();
	const [selectedEntity, setSelectedEntity] = useState<EntityInterface>();
	const [title, setTitle] = useState<string>("");
	const [loadedTextBlocks, setLoadedTextBlocks] = useState<
		TextBlockInterface[]
	>([]);
	const [neTextBlocks, setNewTextBlocks] = useState<TextBlockInterface[]>([]);
	const navigate = useNavigate();
	const location = useLocation();

	const loadData = useCallback(
		async (universeId?: string, entityId?: string) => {
			if (universeId) {
				const fetch = async () => {
					try {
						const data = await fetchUniverse(universeId);
						setSelectedUniverse(data);
					} catch (err) {
						console.error("Error fetching universe:", err);
					}
				};
				fetch();
			} else {
				setSelectedUniverse(undefined);
			}
			if (entityId) {
				const fetch = async () => {
					try {
						const entityData = await fetchEntity(entityId);
						setSelectedEntity(entityData);
					} catch (err) {
						console.error("Error fetching entity:", err);
					}
					try {
						const tbData = await fetchTextBlock(entityId);
						setLoadedTextBlocks(tbData);
						setNewTextBlocks(tbData);
					} catch (error) {
						console.error("Error while fetching text blocks", error);
					}
				};
				fetch();
			} else {
				setSelectedEntity(undefined);
			}
		},
		[],
	);

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

	const handleUniverseEntityUpdate = useCallback(() => {
		const fetch = async () => await loadData(universeId, entityId);
		fetch();
	}, [universeId, entityId, loadData]);

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
		const fetchIsLoggedin = async () => {
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
		fetchIsLoggedin();
	}, [location.pathname, navigate]);

	useEffect(() => {
		const fetch = async () => await loadData(universeId, entityId);
		fetch();
	}, [universeId, entityId, loadData]);

	useEffect(() => {
		if (selectedUniverse) {
			if (selectedEntity) {
				setTitle(selectedEntity.name);
			} else {
				setTitle("Choose a entity");
			}
		} else {
			setTitle("Choose a universe");
		}
		console.log({
			selectedEntity: selectedEntity,
			selectedUniverse: selectedUniverse,
		});
	}, [selectedUniverse, selectedEntity]);

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
						{entityId && <DnDTextBlock entityId={entityId} />}
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
