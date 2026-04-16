import SquareButton from "../UI/Button/square.button";

const Header = () => {
	return (
		<div className="top-0 left-0 w-full h-10 bg-white text-black flex justify-between items-center px-6 py-3 border-b">
			<img
				width={35}
				height={35}
				sizes="100vw"
				alt=""
				src={"/my_universe_doc_logo.png"}
			/>
			<div>My Universe Doc</div>
			<SquareButton
				src={"/profile_icon.svg"}
				alternativeText={"User Button / Profile"}
			/>
		</div>
	);
};

export default Header;
