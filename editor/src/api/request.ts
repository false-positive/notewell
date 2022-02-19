/**
 * Functions for fetching data from notewell_web's API
 *
 */

import invariant from 'tiny-invariant';

const API_URL = '/api';

/**
 * The API access token of the current interaction.
 * Must be set before any calls to the API are made
 * Must get refreshed withe the refresh token
 *
 */
let accessToken: string | null = null;

/**
 * The API refresh token of the current interaction.
 * Must be set before refresh calls to the API are made
 *
 */
let refreshToken: string | null = null;

export const setTokenPair = (accessValue: string, refreshValue: string) => {
    accessToken = accessValue;
    refreshToken = refreshValue;
};

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

/**
 * The last response Promise from the `/api/token/refresh/` endpoint
 *
 * If not null, it must be awaited to avoid race conditions
 * and sending requests with outdated, expired access tokens
 * while the new access token is being generated.
 *
 */
let refreshTokenPairResponse: Promise<Response> | null = null;

const refreshTokenPair = async () => {
    refreshTokenPairResponse = makeRequest(`token/refresh/`, {
        method: 'POST',
        body: JSON.stringify({
            refresh: refreshToken,
        }),
    });
    const response = await refreshTokenPairResponse;
    refreshTokenPairResponse = null;
    const { access, refresh } = await response.json();
    if (access && refresh) {
        accessToken = access;
        refreshToken = refresh;
        return true;
    }
    return false;
};

export const makeAuthenticatedRequest = async (
    url: string,
    opts: RequestInit
): Promise<Response> => {
    if (refreshTokenPairResponse) {
        await refreshTokenPairResponse;
    }
    invariant(accessToken, 'API Token is not set');
    const requestOpts = () => ({
        ...opts,
        headers: {
            ...opts.headers,
            Authorization: `Bearer ${accessToken}`,
        },
    });
    const response = await makeRequest(url, requestOpts());
    if (response.status === 401) {
        const isRefreshed = await refreshTokenPair();
        if (isRefreshed) {
            return makeRequest(url, requestOpts());
        }
    }
    return response;
};
