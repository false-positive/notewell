import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Quiz from './routes/Quiz';
import Editor from './routes/Editor';

// HACK: clean the contents of #app
const root = document.getElementById('app')!;
root.innerHTML = '';

ReactDOM.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
    root
);
