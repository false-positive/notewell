import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

// HACK: clean the contents of #app
const root = document.getElementById('app')!;
root.innerHTML = '';

// const initialDataEl = document.getElementById('nw-editor-initial-data')!;
// const initialData = JSON.parse(initialDataEl.innerHTML);
// initialDataEl.outerHTML = '';

ReactDOM.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
    root
);
