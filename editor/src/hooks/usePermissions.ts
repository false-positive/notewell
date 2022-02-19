import { useQuery } from 'react-query';
import { getNotePermissions } from '../api/permissions';

type Options = {
    enabled: boolean;
};

const usePermissions = (uuid: string, options?: Options) =>
    useQuery(['permissions', uuid], () => getNotePermissions(uuid), options);

export default usePermissions;
