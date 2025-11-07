import SquareButton from "./Button/square.button";

const Header = () => {
	return (
		<div className="fixed top-0 left-0 w-full bg-gray-50 text-black flex justify-between items-center px-6 py-3 shadow-md">
			<div>
				<img
					width={40}
					height={40}
					sizes="100vw"
					alt=""
					src={"/my_universe_doc_logo.png"}
				/>
			</div>
			<div>My Universe Doc</div>
			<SquareButton
				src={"/profile_icon.svg"}
				alternativeText={"User Button / Profile"}
			/>
		</div>
	);
};

export default Header;
