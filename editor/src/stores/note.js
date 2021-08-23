import { getNote, updateNote } from '../api';
import { writable } from 'svelte/store';

function createNote() {
    const { subscribe, set } = writable(null);

    return {
        subscribe,
        load: async (/** @type {string} */ uuid) => {
            const note = await getNote(uuid);
            set(note);
        },
        update: async (
            /** @type {string} */ uuid,
            /** @type {import("../api").NoteData} */ noteData
        ) => {
            const note = await updateNote(uuid, noteData);
            set(note);
        },
    };
}

export const note = createNote();
