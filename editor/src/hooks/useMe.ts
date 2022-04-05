import { useQuery } from 'react-query';
import { getMe } from '../api/users';

const useMe = () => useQuery('me', getMe);

export default useMe;
