import React from 'react';
import invariant from 'tiny-invariant';
import { setTokenPair } from './request';

type TokenPair = { access: string; refresh: string };

type InitialData = {
    tokenPair: TokenPair;
    note?: any;
    openDialog: string;
};

type APIInitialData = {
    definitely_not_token_pair: TokenPair;
    note?: any;
    open_dialog?: string;
};

const fromAPIInitialData = (apiData: APIInitialData): InitialData => ({
    tokenPair: apiData.definitely_not_token_pair,
    note: apiData.note,
    openDialog: apiData.open_dialog || '',
});

export const loadInitialData = (): InitialData => {
    const initialDataEl = document.getElementById('nw-editor-initial-data');
    invariant(initialDataEl, 'Initial data not found');

    const apiInitialData = JSON.parse(initialDataEl.innerHTML);
    initialDataEl.outerHTML = '';
    invariant(
        apiInitialData.definitely_not_token_pair,
        'Token pair not found in initial data.'
    );

    const initialData = fromAPIInitialData(apiInitialData);
    setTokenPair(initialData.tokenPair.access, initialData.tokenPair.refresh);
    return apiInitialData;
};

export const InitialDataContext = React.createContext<InitialData | null>(null);
