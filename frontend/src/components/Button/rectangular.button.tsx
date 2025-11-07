import type React from "react";

interface RectangularButtonProps {
	url: string;
	text: string;
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
	url,
	text,
	color = "blue",
}) => {
	const colorClasses = colorMap[color] || colorMap.blue;

	return (
		<a
			href={url}
			className={`${colorClasses} text-white font-medium px-6 py-3 rounded-lg transition max-w-3xs`}
		>
			{text}
		</a>
	);
};

export default RectangularButton;
