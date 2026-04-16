export interface UserInterface {
	id: number;
	email: string;
	password: string;
	username: string;
	bio: string | null;
	picture: ArrayBuffer | null;
}
