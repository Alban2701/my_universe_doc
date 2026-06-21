import { useCallback, useEffect, useState } from "react";
import ProfileActionCard from "../Cards/ProfileActionCard";
import SquareButton, { type SquareButtonInterface } from "./square.button";

interface ProfileButtonInterface {
	src: string;
	alternativeText: string;
	width: number;
	height: number;
}

function ProfileButton({
	src,
	alternativeText,
	width,
	height,
}: ProfileButtonInterface) {
	const [profileCardActive, setProfileCardActive] = useState<boolean>(false);
	const [loggedIn, setLoggedIn] = useState<boolean>(false);

	const handleClick = useCallback(async () => {
		setProfileCardActive(!profileCardActive);
	}, [profileCardActive]);

	const handleLogout = useCallback(async () => {
		setProfileCardActive(false);
	}, []);

	useEffect(() => {
		const fetchIsLoggedin = async () => {
			try {
				const response = await fetch("/api/user/me");
				if (!response.ok) {
					setLoggedIn(false);
				} else {
					setLoggedIn(true);
				}
			} catch (e) {
				console.log(e);
			}
		};
		fetchIsLoggedin();
	}, []);

	return (
		<div className="flex flex-col relative">
			<SquareButton
				src={src}
				alternativeText={alternativeText}
				width={width}
				height={height}
				onClick={handleClick}
			/>
			{profileCardActive && (
				<div className="absolute top-full right-0 z-20 mt-1">
					<ProfileActionCard connected={loggedIn} logoutAction={handleLogout} />
				</div>
			)}
		</div>
	);
}

export default ProfileButton;
