interface SquareButtonInterface {
	src: string;
	alternativeText: string;
	width?: number;
	height?: number;
}

export default function SquareButton({
	src,
	alternativeText,
	width = 100,
	height = 100,
}: SquareButtonInterface) {
	return (
		<button
			type="button"
			className="relative w-10 h-10 p-2 group cursor-pointer bg-white rounded-lg shadow-[1px_2px_4px_0px_rgba(0,0,0,0.25)] hover:shadow-none overflow-hidden transition-all duration-500"
		>
			<span className="absolute inset-0 rounded-lg shadow-[inset_0_0_0_0_rgba(0,0,0,0.25)] transition-all duration-500 group-hover:shadow-[inset_1px_2px_4px_rgba(0,0,0,0.25)]" />
			<img
				width={width}
				height={height}
				className="relative w-auto h-auto z-10"
				src={src}
				alt={alternativeText}
			/>
		</button>
	);
}
