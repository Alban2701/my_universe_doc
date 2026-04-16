import React, { useEffect, useState } from "react";
import type { UniverseInterface } from "../../../types/universe";
import CreateUniverse from "../Modals/CreateUniverse";
import { useNavigate } from "react-router-dom";

function PanelUniverse({
	universeId,
	onUniverseUpdate,
}: {
	universeId?: string;
	onUniverseUpdate: (selectedUniverse?: UniverseInterface) => void;
}) {
	const [universes, setUniverses] = useState<UniverseInterface[]>([]);
	const [refresh, setRefresh] = useState<boolean>(false);
	const navigate = useNavigate();
	// biome-ignore lint/correctness/useExhaustiveDependencies: <we need the refresh dependancy to refresh the view once we created a doc. Otherwise we don't want to do anything with the refresh variable>
	useEffect(() => {
		const fetchUniverses = async () => {
			try {
				const response = await fetch("/api/universe/my_universes", {
					credentials: "include",
					method: "GET",
				});
				if (!response.ok) {
					throw new Error(
						`An error occured while fetching universes\n${await response.json()}`,
					);
				}
				const data = await response.json();
				setUniverses(data);
				return data;
			} catch (error) {
				console.log("Error:", error);
			}
		};
		fetchUniverses();
		return;
	}, [refresh]);

	const handleUniverseCreated = () => {
		setRefresh(!refresh);
	};

	return (
		<div className="border-b border-r flex flex-col h-full">
			<h1 className="text-3xl text-center border-b mb-5">Your Docs</h1>
			<ul className="m-2 overflow-y-auto">
				{universes.map((universe) => (
					<li key={universe.id}>
						<button
							type="button"
							onClick={() => {
								onUniverseUpdate(universe);
								navigate(`/universes/${universe.id}`);
							}}
							className="hover:cursor-pointer border-y my-1 p-1 w-full"
						>
							{universe.name}
						</button>
					</li>
				))}
			</ul>
			<div className="place-self-center mt-auto mb-5 p-2 border-t">
				<CreateUniverse onUniverseCreated={handleUniverseCreated} />
			</div>
		</div>
	);
}

export default PanelUniverse;
