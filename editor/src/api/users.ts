import { makeRequest } from './request';

type APIUser = {
    username: string;
    email: string;
    first_name: string;
    last_name: string;
};

// TODO: return actual users, so we can store them in react query
export const searchUsers = async (username: string) => {
    const encUsername = encodeURI(username);
    const response = await makeRequest(
        `user_search/?search_query=${encUsername}`
    );
    const { data } = await response.json();
    return (data as APIUser[]).map(({ username }) => username);
};
