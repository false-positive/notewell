import App from './App.svelte';

// HACK: clean the contents of #app
document.getElementById('app').innerHTML = '';

const app = new App({
    target: document.getElementById('app'),
});

export default app;
