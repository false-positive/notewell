import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { InitialDataContext, loadInitialData } from './api/initialData';

// HACK: clean the contents of #app
const root = document.getElementById('app')!;
root.innerHTML = '';

const initialData = loadInitialData();

ReactDOM.render(
    <React.StrictMode>
        <InitialDataContext.Provider value={initialData}>
            <App />
        </InitialDataContext.Provider>
    </React.StrictMode>,
    root
);
