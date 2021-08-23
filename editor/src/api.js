/**
 * Functions for working with notewell_web's API
 *
 */

const API_URL = '/api';

/**
 * The API token of the current interaction.
 * Must be set before any calls to the API are made
 *
 * @type {string}
 */
let token = null;

export function setToken(value) {
    token = value;
}

/**
 * @param {string} url
 * @param {RequestInit} opts
 */
function makeRequest(url, opts) {
    if (!token) {
        throw new Error('API Token is not set!!');
    }
    console.log(opts.method, `${API_URL}/${url}`);
    return fetch(`${API_URL}/${url}`, {
        ...opts,
        headers: {
            ...opts.headers, // in case we want to add other headers
            Authorization: `Token ${token}`,
            'Content-Type': 'application/json',
        },
    });
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
    const response = await makeRequest(`notes/${uuid}/`, {
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
    const response = await makeRequest(`notes/${uuid}/`, {
        method: 'PUT',
        body: JSON.stringify(noteData),
    });
    const data = await response.json();
    return data;
}
