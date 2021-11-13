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
export const messages = writable([]);
