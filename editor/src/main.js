import App from './App.svelte';

// HACK: clean the contents of #app
document.getElementById('app').innerHTML = '';

const initialDataEl = document.getElementById('nw-editor-initial-data');
const initialData = JSON.parse(initialDataEl.innerHTML);
initialDataEl.outerHTML = '';

const app = new App({
    target: document.getElementById('app'),
    props: {
        initialData,
    },
});

export default app;
