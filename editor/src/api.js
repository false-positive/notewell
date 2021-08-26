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
 * @param {string} url
 */
async function getData(url, authenticated = true) {
    const func = authenticated ? makeAuthenticatedRequest : makeRequest;
    try {
        const response = await func(url, {
            method: 'GET',
        });
        const { data } = await response.json();
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
 */
async function updateData(url, updatedData, authenticated = true) {
    const func = authenticated ? makeAuthenticatedRequest : makeRequest;
    try {
        const response = await func(url, {
            method: 'PATCH',
            body: JSON.stringify(updatedData),
        });
        const { data } = await response.json();
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
