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
 * @type {string}
 */
let accessToken = null;

/**
 * The API refresh token of the current interaction.
 * Must be set before refresh calls to the API are made
 *
 * @type {string}
 */
let refreshToken = null;

/**
 * @param {string} accessValue
 * @param {string} refreshValue
 */
export function setTokenPair(accessValue, refreshValue) {
    accessToken = accessValue;
    refreshToken = refreshValue;
}

/**
 * @param {string} url
 * @param {RequestInit} opts
 * @returns {Promise<Response>}
 */
function makeRequest(url, opts) {
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
 * @type {Promise<Response>}
 */
let refreshTokenPairResponse = null;

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

/**
 * @param {string} url
 * @param {RequestInit} opts
 * @returns {Promise<Response>}
 */
async function makeAuthenticatedRequest(url, opts) {
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
 * @type {Map<string, Set<Function>>}
 */
const apiEventHandlers = new Map();

/**
 * @param {string} event
 * @param {Function} handler
 */
export function apiOn(event, handler) {
    if (!apiEventHandlers.has(event)) {
        apiEventHandlers.set(event, new Set());
    }
    apiEventHandlers.get(event).add(handler);
}

/**
 * @param {string} event
 * @param {Function} handler
 */
export function apiOff(event, handler) {
    if (!apiEventHandlers.get(event)?.has(handler)) return;

    apiEventHandlers.get(event).delete(handler);
    if (!apiEventHandlers.get(event).size) {
        apiEventHandlers.delete(event);
    }
}

/**
 * @param {string} event
 * @param {any} details
 */
function apiDispatch(event, details) {
    if (!apiEventHandlers.has(event)) return;

    for (const handler of apiEventHandlers.get(event)) {
        handler(details);
    }
}

/**
 * Perform a request and return the `data` field.
 *
 * By default, it is authenticated, unless the param is set to false
 * @param {string} url
 * @param {boolean} [authenticated=true]
 * @param {boolean} [isTopLevel=false] - whether the data is inside a data field of the json response, or it is just the top level. Temporary hack
 */
async function getData(url, authenticated = true, isTopLevel = false) {
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

/**
 * @param {string} url
 * @param {NoteData} updatedData
 * @param {boolean} [isTopLevel=false] - whether the data is inside a data field of the json response, or it is just the top level. Temporary hack
 * @param {('PUT'|'PATCH')} [method='PATCH'] - whether to use PUT or PATCH
 */
async function updateData(
    url,
    updatedData,
    authenticated = true,
    isTopLevel = false,
    method = 'PATCH'
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

/**
 * @typedef {Object} Note
 * @property {boolean} isLocal - whether the Note is stored in the server or in mempoy
 * @property {string} uuid - the uuid of the Note used for updating. `null` if local.
 * @property {string} author
 * @property {string} title
 * @property {string} content - the content of the note in markdown
 * @property {string[]} categories - the categories that the nore is present in
 * @property {Date} creation_date
 */

/**
 * Get the data of note with uuid.
 *
 * @param {string} uuid
 * @returns {Promise<Note>}
 */
export async function getNote(uuid) {
    const [data] = await getData(`notes/${uuid}/`);
    return data;
}

/**
 * The data required for modifying a Note
 *
 * @typedef {Object} NoteData
 * @property {string} [uuid]
 * @property {string} [title]
 * @property {string} [content]
 * @property {string[]} [categories]
 */

/**
 * @param {string} uuid
 * @param {NoteData} noteData
 * @returns {Promise<Note>}
 */
export async function updateNote(uuid, noteData) {
    const [data] = await updateData(`notes/${uuid}/`, noteData);
    return data;
}

/**
 * @typedef {Object} Permission - a.k.a. SharedItem in the Django source ;-;
 * @property {string} user - the name of the user that receives the note
 * @property {('R'|'W')} perm_level - wether the user can edit or just view the note
 */

/**
 * Get Edit and View permissions of a Note
 *
 * @param {string} uuid - the uuid of the node to query
 * @returns {Promise<Permission[]>}
 */
export async function getNotePermissions(uuid) {
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
 * @param {string} uuid - the uuid of the node to query
 * @param {Permission[]} permissions - the new, updated list of permissions
 * @returns {Promise<Permission[]>}
 */
export async function updateNotePermissions(uuid, permissions) {
    const [data] = await updateData(
        `notes/${uuid}/permissions/`,
        permissions,
        /* authenticated = */ true,
        /* isTopLevel = */ false,
        /* method = */ 'PUT'
    );
    return data;
}
