/**
 * Functions for working with notewell_web's API
 *
 */

const API_URL = '/api';

/**
 * The API access token of the current interaction.
 * Must be set before any calls to the API are made
 * Must get refreshed withe the refresh token
 *
 */
let accessToken: string = null;

/**
 * The API refresh token of the current interaction.
 * Must be set before refresh calls to the API are made
 *
 */
let refreshToken: string = null;

export function setTokenPair(accessValue: string, refreshValue: string) {
    accessToken = accessValue;
    refreshToken = refreshValue;
}

function makeRequest(url: string, opts: RequestInit): Promise<Response> {
    return fetch(`${API_URL}/${url}`, {
        ...opts,
        headers: {
            ...opts.headers,
            'Content-Type': 'application/json',
        },
    });
}

/**
 * The last response Promise from the `/api/token/refresh/` endpoint
 *
 * If not null, it must be awaited to avoid race conditions
 * and sending requests with outdated, expired access tokens
 * while the new access token is being generated.
 *
 */
let refreshTokenPairResponse: Promise<Response> = null;

async function refreshTokenPair() {
    refreshTokenPairResponse = makeRequest(`token/refresh/`, {
        method: 'POST',
        body: JSON.stringify({
            refresh: refreshToken,
        }),
    });
    const response = await refreshTokenPairResponse;
    refreshTokenPairResponse = null;
    const { access, refresh } = await response.json();
    if (access && refresh) {
        accessToken = access;
        refreshToken = refresh;
        return true;
    }
    return false;
}

async function makeAuthenticatedRequest(
    url: string,
    opts: RequestInit
): Promise<Response> {
    if (refreshTokenPairResponse) {
        await refreshTokenPairResponse;
    }
    if (!accessToken) {
        throw new Error('API Token is not set!!');
    }
    const requestOpts = () => ({
        ...opts,
        headers: {
            ...opts.headers,
            Authorization: `Bearer ${accessToken}`,
        },
    });
    const response = await makeRequest(url, requestOpts());
    if (response.status === 401) {
        const isRefreshed = await refreshTokenPair();
        if (isRefreshed) {
            return makeRequest(url, requestOpts());
        }
    }
    return response;
}

/**
 * Map of all handlers registered to API events
 *
 */
const apiEventHandlers: Map<string, Set<Function>> = new Map();

export function apiOn(event: string, handler: Function) {
    if (!apiEventHandlers.has(event)) {
        apiEventHandlers.set(event, new Set());
    }
    apiEventHandlers.get(event).add(handler);
}

export function apiOff(event: string, handler: Function) {
    if (!apiEventHandlers.get(event)?.has(handler)) return;

    apiEventHandlers.get(event).delete(handler);
    if (!apiEventHandlers.get(event).size) {
        apiEventHandlers.delete(event);
    }
}

function apiDispatch(event: string, details: any) {
    if (!apiEventHandlers.has(event)) return;

    for (const handler of apiEventHandlers.get(event)) {
        handler(details);
    }
}

async function getData(
    url: string,
    authenticated: boolean = true,
    isTopLevel: boolean = false
) {
    const func = authenticated ? makeAuthenticatedRequest : makeRequest;
    try {
        const response = await func(url, {
            method: 'GET',
        });
        const json = await response.json();
        const data = isTopLevel ? json : json.data;
        return [data, null];
    } catch (err) {
        console.error(err);
        apiDispatch('error', err);
        return [null, err];
    }
}

async function updateData(
    url: string,
    updatedData: any,
    authenticated = true,
    isTopLevel: boolean = false,
    method: 'PUT' | 'PATCH' = 'PATCH'
) {
    const func = authenticated ? makeAuthenticatedRequest : makeRequest;
    try {
        const response = await func(url, {
            method,
            body: JSON.stringify(updatedData),
        });
        const json = await response.json();
        const data = isTopLevel ? json : json.data;
        return [data, null];
    } catch (err) {
        console.error(err);
        apiDispatch('error', err);
        return [null, err];
    }
}

type Note = {
    isLocal: true;
    uuid: string;
    author: string;
    title: string;
    content: string;
    categories: string[];
    creation_date: Date;
};

/**
 * Get the data of note with uuid.
 *
 */
export async function getNote(uuid: string): Promise<Note> {
    const [data] = await getData(`notes/${uuid}/`);
    return data;
}

type NoteData = {
    uuid: string;
    title: string;
    content: string;
    categories: string[];
};

export async function updateNote(
    uuid: string,
    noteData: NoteData
): Promise<Note> {
    const [data] = await updateData(`notes/${uuid}/`, noteData);
    return data;
}

/**
 * a.k.a. SharedItem in the Django source ;-;
 */
type Permission = {
    user: string;
    perm_level: 'R' | 'W';
};

/**
 * Get Edit and View permissions of a Note
 *
 */
export async function getNotePermissions(uuid: string): Promise<Permission[]> {
    const [data] = await getData(
        `notes/${uuid}/permissions/`,
        /* authenticated = */ true,
        /* isTopLevel = */ true
    );
    return data;
}

/**
 * Update Edit and View permissions of a Note
 *
 */
export async function updateNotePermissions(
    uuid: string,
    permissions: Permission[]
): Promise<Permission[]> {
    const [data] = await updateData(
        `notes/${uuid}/permissions/`,
        permissions,
        /* authenticated = */ true,
        /* isTopLevel = */ false,
        /* method = */ 'PUT'
    );
    return data;
}

type User = {
    username: string;
    email: string;
    first_name: string;
    last_name: string;
};

/**
 * Search users by username
 *
 * Used mainly for autocompletion.
 *
 */
export async function searchUsers(username: string): Promise<User[]> {
    const [data] = await getData(
        `user_search/?search_query=${encodeURIComponent(username)}`
    );
    return data;
}

export async function summarizeText(text) {
    const response = await makeRequest(`ai/summarize/`, {
        method: 'POST',
        body: JSON.stringify({ text }),
    });
    const { result } = await response.json();
    return result;
}
