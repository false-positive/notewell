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

export function setTokenPair(accessValue, refreshValue) {
    accessToken = accessValue;
    refreshToken = refreshValue;
}

/**
 * @param {string} url
 * @param {RequestInit} opts
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

async function refreshTokenPair() {
    const response = await makeRequest(`token/refresh/`, {
        method: 'POST',
        body: JSON.stringify({
            refresh: refreshToken,
        }),
    });
    const { access, refresh } = await response.json();
    if (access && refresh) {
        accessToken = access;
        refreshToken = refresh;
        return true;
    }
    return false;
}

async function makeAuthenticatedRequest(url, opts) {
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
            return await makeRequest(url, requestOpts());
        }
    }
    return response;
}
/**
 * @typedef {Object} Note
 * @property {string} author
 * @property {string} uuid
 * @property {string} title
 * @property {string[]} categories
 * @property {Date} creation_date
 */

/**
 * Get the data of note with uuid.
 *
 * @param {string} uuid
 * @returns {Promise<Note>}
 */
export async function getNote(uuid) {
    const response = await makeAuthenticatedRequest(`notes/${uuid}/`, {
        method: 'GET',
    });
    const data = await response.json();
    return data;
}

/**
 * The data required for modifying a Note
 *
 * @typedef {Object} NoteData
 * @property {string} [uuid]
 * @property {string} title
 * @property {string[]} [categories]
 */

/**
 * @param {string} uuid
 * @param {NoteData} noteData
 * @returns {Promise<Note>}
 */
export async function updateNote(uuid, noteData) {
    const response = await makeAuthenticatedRequest(`notes/${uuid}/`, {
        method: 'PUT',
        body: JSON.stringify(noteData),
    });
    const data = await response.json();
    return data;
}
