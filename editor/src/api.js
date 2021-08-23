/**
 * Functions for working with notewell_web's API
 *
 */

const API_URL = '/api';

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
 * @param {string} token
 * @param {string} uuid
 * @returns {Promise<Note>}
 */
export async function getNote(token, uuid) {
    const response = await fetch(`${API_URL}/notes/${uuid}/`, {
        method: 'GET',
        headers: {
            Authorization: `Token ${token}`,
            'Content-Type': 'application/json',
        },
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
 * @param {string} token
 * @param {string} uuid
 * @param {NoteData} noteData
 * @returns {Promise<Note>}
 */
export async function updateNote(token, uuid, noteData) {
    const response = await fetch(`${API_URL}/notes/${uuid}/`, {
        method: 'PUT',
        headers: {
            Authorization: `Token ${token}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(noteData),
    });
    const data = await response.json();
    return data;
}
