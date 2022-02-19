import { useMutation, useQueryClient } from 'react-query';
import { Permission, updateNotePermissions } from '../api/permissions';

const useSavePermissions = (uuid: string) => {
    const queryClient = useQueryClient();
    return useMutation(
        (permissions: Permission[]) => updateNotePermissions(uuid, permissions),
        {
            onSuccess: (permissions: Permission[]) => {
                queryClient.setQueryData(['permissions', uuid], permissions);
            },
        }
    );
};

export default useSavePermissions;
