import { useEffect, useState } from "react";
import type { EntityInterface } from "@/src/types/entity";
import type { UniverseInterface } from "../../../types/universe";
import DeleteEntity from "../Modals/Entity/DeleteEntity";
import UpdateEntity from "../Modals/Entity/UpdateEntity";
import DeleteUniverse from "../Modals/Universe/DeleteUniverse";
import UpdateUniverse from "../Modals/Universe/UpdateUniverse";

function PanelSettings({
	selectedUniverse,
	selectedEntity,
	onUniverseEntityUpdated,
	onUniverseDeleted,
	onEntityDeleted,
}: {
	selectedUniverse?: UniverseInterface;
	selectedEntity?: EntityInterface;
	onUniverseEntityUpdated: () => void;
	onUniverseDeleted: () => void;
	onEntityDeleted: () => void;
}) {
	const [title, setTitle] = useState<string | undefined>("");
	useEffect(() => {
		setTitle(selectedUniverse?.name);
	}, [selectedUniverse]);

	return (
		<div className="border-b border-l h-full">
			<h1 className="text-3xl text-center border-b mb-5">
				Settings for {title}
			</h1>
			<div className="flex flex-col">
				{selectedUniverse ? (
					<div className="flex flex-row p-2 gap-2">
						<UpdateUniverse
							universe={selectedUniverse}
							onUniverseUpdated={onUniverseEntityUpdated}
						/>
						<DeleteUniverse
							universe={selectedUniverse}
							onUniverseDeleted={onUniverseDeleted}
						/>
					</div>
				) : (
					<p>select a universe</p>
				)}
				{selectedEntity ? (
					<div className="flex flex-row p-2 gap-2">
						<UpdateEntity
							entity={selectedEntity}
							onEntityUpdated={onUniverseEntityUpdated}
						/>
						<DeleteEntity
							entity={selectedEntity}
							onEntityDeleted={onEntityDeleted}
						/>
					</div>
				) : (
					<p>select an entity</p>
				)}
			</div>
		</div>
	);
}

export default PanelSettings;
