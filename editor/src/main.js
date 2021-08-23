import { getNote, updateNote } from './api';
import App from './App.svelte';

// HACK: clean the contents of #app
document.getElementById('app').innerHTML = '';

// HACK: expects that the url has /notes/ followed by the uuid
// TODO: use better way of sharing this data...
const pathComponents = window.location.pathname.split('/');
const idxId = pathComponents.indexOf('notes') + 1;
const note_uuid = idxId + 1;

const app = new App({
    target: document.getElementById('app'),
    props: {
        api_token: '27ffc72a83f3e4318fbfd9745bf55de656224857', // XXX: hey maybe don't hardcode tokens
        note_uuid,
    },
});

export default app;
