import { useQuery } from 'react-query';
import { getMe } from '../api/users';

type Options = {
    redirect?: boolean;
};

const useMe = ({ redirect = false }: Options = {}) =>
    useQuery('me', async () => ({ user: await getMe() }), {
        onError: () => {
            if (redirect) {
                console.log('redirect');
                const route = encodeURIComponent(window.location.pathname);
                window.location.replace(`/login/?next=${route}`);
            }
        },
    });

export default useMe;
