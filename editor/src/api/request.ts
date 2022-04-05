/**
 * Functions for fetching data from notewell_web's API
 *
 */

const API_URL = 'http://localhost:8000/api';

export const makeRequest = (
    url: string,
    opts?: RequestInit
): Promise<Response> =>
    fetch(`${API_URL}/${url}`, {
        ...opts,
        headers: {
            ...opts?.headers,
            'Content-Type': 'application/json',
        },
    });

export const makeAuthRequest = (
    url: string,
    opts?: RequestInit
): Promise<Response> =>
    makeRequest(url, {
        ...opts,
        credentials: 'include',
    });
