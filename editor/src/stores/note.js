import { writable } from 'svelte/store';

/**
 * @var note
 * @type {import('svelte/store').Writable<import('src/api').Note>}
 */
export const note = writable(null);
