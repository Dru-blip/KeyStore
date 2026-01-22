export interface Vault{
    id:string;
    name:string;
    records:Record[];
}

export interface Record{
    id:string;
    name:string;
    usernameOrEmail:string;
    password:string;
}

export const createVault= (name:string):Vault => {
    return {
        id: crypto.randomUUID(),
        name,
        records:[],
    };
}

export const createRecord= (name:string, usernameOrEmail:string, password:string):Record => {
    return {
        id: crypto.randomUUID(),
        name,
        usernameOrEmail,
        password,
    };
}
