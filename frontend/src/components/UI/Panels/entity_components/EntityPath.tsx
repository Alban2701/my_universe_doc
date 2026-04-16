import React, { useState, useEffect } from "react";
import type { Entity } from "@/src/types/entity";

interface EntityPathProps {
	entity: Entity;
}

function EntityPath({ entity }: EntityPathProps) {
	const [parents, setParents] = useState<Entity[]>([]);
	const [loading, setLoading] = useState<boolean>(true);
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		const fetchParents = async () => {
			try {
				setLoading(true);
				const response = await fetch(`/api/entity/${entity.id}/parents`, {
					credentials: "include",
					method: "GET",
				});
				if (!response.ok) {
					throw new Error(
						`An error occurred while fetching parents: ${response.statusText}`,
					);
				}
				const data = await response.json();
				setParents(data);
				setError(null);
			} catch (err) {
				setError(err instanceof Error ? err.message : "Unknown error");
				console.error("Error fetching parents:", err);
			} finally {
				setLoading(false);
			}
		};

		fetchParents();
	}, [entity.id]);

	if (loading) {
		return <div className="text-sm text-gray-500">Loading...</div>;
	}

	if (error) {
		return <div className="text-sm text-red-500">Error: {error}</div>;
	}

	const renderChain = () => {
		const chain = [...parents].reverse();

		return (
			<div className="flex flex-col items-start gap-1 text-sm">
				{chain.map((parent, index) => (
					<React.Fragment key={parent.id}>
						<div className="font-medium">{parent.name}</div>
						{index < chain.length - 1 && <div className="text-gray-400">›</div>}
					</React.Fragment>
				))}
				<div className="font-medium">{entity.name}</div>
			</div>
		);
	};

	return <div>{renderChain()}</div>;
}

export default EntityPath;
