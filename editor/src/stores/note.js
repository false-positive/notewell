import { getNote, updateNote } from '../api';
import { writable } from 'svelte/store';

function createNote() {
    const { subscribe, set } = writable(null);

    const setNote = (data) => set({ ...data, isLocal: data.uuid === null });

    return {
        subscribe,
        setInitial: setNote,
        load: async (/** @type {string} */ uuid) => {
            const note = await getNote(uuid);
            if (note) {
                setNote(note);
            }
        },
        update: async (
            /** @type {string} */ uuid,
            /** @type {import("../api").NoteData} */ noteData
        ) => {
            const note = await updateNote(uuid, noteData);
            if (note) {
                setNote(note);
            }
        },
    };
}

export const note = createNote();
