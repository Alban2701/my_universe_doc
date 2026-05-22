import ProfileButton from "../UI/Button/ProfileButton";

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
			<div>
				<h1>My Universe Doc</h1>
			</div>
			<div>
				<ProfileButton
					src={"/profile_icon.svg"}
					alternativeText={"User Button / Profile"}
					width={35}
					height={35}
				/>
			</div>
		</div>
	);
};

export default Header;
