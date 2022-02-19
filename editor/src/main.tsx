import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { loadInitialData } from './api/initialData';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

// HACK: clean the contents of #app
const root = document.getElementById('app')!;
root.innerHTML = '';

loadInitialData();

ReactDOM.render(
    <React.StrictMode>
        <BrowserRouter>
            <Routes>
                <Route path="/notes/:noteId/" element={<App />}>
                    <Route path="edit/" element={<p>edit notes</p>} />
                    <Route path="quiz/" element={<p>QUIZ!!1</p>} />
                </Route>
            </Routes>
        </BrowserRouter>
    </React.StrictMode>,
    root
);
