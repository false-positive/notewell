import { makeAuthRequest } from './request';

export type PermissionLevel = 'R' | 'W';

export type Permission = {
    username: string;
    permLevel: PermissionLevel;
};
type APIPermission = { user: string; perm_level: PermissionLevel };

const fromAPIPermissions = (apiPerms: APIPermission[]): Permission[] =>
    apiPerms.map(({ user, perm_level }) => ({
        username: user,
        permLevel: perm_level,
    }));
const toAPIPermissions = (perms: Permission[]): APIPermission[] =>
    perms.map(({ username, permLevel }) => ({
        user: username,
        perm_level: permLevel,
    }));

export const getNotePermissions = async (
    uuid: string
): Promise<Permission[]> => {
    const request = await makeAuthRequest(`notes/${uuid}/permissions/`);
    const data = (await request.json()) as APIPermission[]; // TODO: validate
    return fromAPIPermissions(data);
};

export const updateNotePermissions = async (
    uuid: string,
    permissions: Permission[]
): Promise<Permission[]> => {
    const apiPerms: APIPermission[] = toAPIPermissions(permissions);
    const request = await makeAuthRequest(`notes/${uuid}/permissions/`, {
        method: 'PUT',
        body: JSON.stringify(apiPerms),
    });
    const { data } = (await request.json()) as { data: APIPermission[] };
    return fromAPIPermissions(data);
};
