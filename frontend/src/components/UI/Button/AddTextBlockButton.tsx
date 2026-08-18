import type { MouseEventHandler } from "react";

interface RectangularButtonProps {
	onClick: MouseEventHandler | undefined;
}

const AddTextBlockButton: React.FC<RectangularButtonProps> = ({ onClick }) => {
	return (
		<button
			type="button"
			className={`w-full cursor-pointer text-center text-xl text-white font-medium rounded-lg transition bg-gray-400 hover:bg-gray-500`}
			onClick={onClick}
		>
			<p className="text-center">+</p>
		</button>
	);
};

export default AddTextBlockButton;
