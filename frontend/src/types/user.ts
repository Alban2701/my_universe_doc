export interface User {
	id: number;
	email: string;
	password: string;
	username: string;
	bio: string | null;
	picture: ArrayBuffer | null;
}
