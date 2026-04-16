import type React from "react";
import type { MouseEventHandler } from "react";

interface RectangularButtonProps {
	text: string;
	onClick: MouseEventHandler | undefined
	color?: "blue" | "red" | "green" | "purple" | "orange";
}

const colorMap: Record<string, string> = {
	blue: "bg-blue-600 hover:bg-blue-700",
	red: "bg-red-600 hover:bg-red-700",
	green: "bg-green-600 hover:bg-green-700",
	purple: "bg-purple-600 hover:bg-purple-700",
	orange: "bg-orange-600 hover:bg-orange-700",
};

const RectangularButton: React.FC<RectangularButtonProps> = ({
	text,
	onClick,
	color = "blue",
}) => {
	const colorClasses = colorMap[color] || colorMap.blue;

	return (
		<button
			type="button"
			className={`cursor-pointer text-white font-medium px-6 py-3 rounded-lg transition max-w-3xs ${colorClasses}`}
			onClick={onClick}
		>
			{text}
		</button>
	);
};

export default RectangularButton;
