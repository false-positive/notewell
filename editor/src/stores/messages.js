import { writable } from 'svelte/store';

/**
 * @typedef {('info'|'success'|'warning'|'error')} MessageSeverity
 */

/**
 * @typedef {Object} Message
 * @property {Number} id
 * @property {string} text
 * @property {MessageSeverity} severity
 */

/**
 * @type {import('svelte/store').Writable<Message[]>}
 */
export const messages = writable([
    { id: 0, severity: 'info', text: 'Info' },
    { id: 1, severity: 'success', text: 'Success' },
    { id: 2, severity: 'warning', text: 'Warning' },
    { id: 3, severity: 'error', text: 'Error' },
]);
