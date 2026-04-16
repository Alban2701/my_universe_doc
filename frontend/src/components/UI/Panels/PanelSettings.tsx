import React, { useEffect, useState } from "react";
import type { UniverseInterface } from "../../../types/universe";

function PanelSettings({ universeId }: { universeId?: string }) {
	const [universe, setUniverse] = useState<UniverseInterface>();

	useEffect(() => {
		if (!universeId) return;
		const fetchUniverse = async () => {
			try {
				const response = await fetch(`/api/universe/${universeId}`, {
					credentials: "include",
					method: "GET",
				});
				if (!response.ok) throw new Error("Universe not found");
				const data = await response.json();
				setUniverse(data);
			} catch (error) {
				console.log("Error:", error);
			}
		};
		fetchUniverse();
	}, [universeId]);

	return (
		<div className="border-b border-l h-full">
			<h1 className="text-3xl text-center border-b mb-5">
				Settings for {universe?.name}
			</h1>
		</div>
	);
}

export default PanelSettings;
