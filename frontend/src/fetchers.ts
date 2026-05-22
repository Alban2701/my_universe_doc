interface SignUpPayload {
    email: string;
    password: string;
    checkPassword: string;
    username: string;
}

export const fetchEntity = async (entityId: string) => {
    try {
        const response = await fetch(`/api/entity/${entityId}`, {
            credentials: "include",
            method: "GET",
        });
        if (!response.ok) throw new Error("Entity not found");
        return response.json();
    } catch (error) {
        console.error("Error fetching entities:", error);
        throw new Error(`An unknown error occurred: ${error}`)
    }
};

export const fetchEntityChildren = async (universeId: string, entityId?: string) => {
    try {
        const response = entityId
            ? await fetch(`/api/entity/${entityId}/direct-children`, {
                credentials: "include",
                method: "GET",
            })
            : await fetch(`/api/universe/${universeId}/first-entities`, {
                credentials: "include",
                method: "GET",
            });
        if (!response.ok) {
            throw new Error("An error occurred while fetching entity's children");
        }
        return response.json()
    } catch (error) {
        console.error("Error fetching entities:", error);
        throw new Error(`An unknown error occurred: ${error}`)
    }
}

export const fetchUniverses = async () => {
    try {
        const response = await fetch("/api/universe/my-universes", {
            credentials: "include",
            method: "GET",
        });
        if (!response.ok) {
            throw new Error(
                `An error occured while fetching universes\n${await response.json()}`,
            );
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching entities:", error);
        throw new Error(`An unknown error occurred: ${error}`)
    }
}

export const fetchUniverse = async (universeId: string) => {
    try {
        const response = await fetch(`/api/universe/${universeId}`, {
            credentials: "include",
            method: "GET",
        });
        if (!response.ok) throw new Error("Universe not found");
        return response.json();
    } catch (error) {
        console.log(error);
        throw new Error(`An unknown error occurred: ${error}`)
    }
};

export const fetchMe = async () => {
    try {
        const response = await fetch("/api/user/me");
        if (!response.ok) {
            throw new Error("user not found or token expired", await response.json())
        }
        return response.json()
    } catch (error) {
        console.log(error);
        throw new Error(`An unknown error occurred: ${error}`)
    }
}

export const fetchTextBlock = async (entityId: string) => {
    try {
        const response = await fetch(`/api/text-block/entity/${entityId}`, {
            credentials: "include",
            method: "GET",
        });
        if (!response.ok) throw new Error("Entity not found", await response.json());
        return response.json();
    } catch (error) {
        console.error("Error while fetching text blocks", error);
        throw new Error(`An unknown error occurred: ${error}`)
    }
}

export const fetchSignup = async (verified_payload: { email: string, password: string }) => {
    try {
        const response = await fetch("/api/user/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(verified_payload),
            credentials: "include",
        });
        if (!response.ok) throw new Error("erreur lors de l'inscription");
        return await response.json();
    } catch (error) {
        console.log(error);
    }
}

export const fetchLogin = async (login_payload: { email: string, password: string }) => {
    const response = await fetch(`/api/user/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(login_payload),
    });
    return response
}