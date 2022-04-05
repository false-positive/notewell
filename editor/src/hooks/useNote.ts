import { useQuery, useQueryClient } from 'react-query';
import { getNote, Note } from '../api/notes';

const useNote = (noteId: string) => {
    const client = useQueryClient();
    return useQuery(['note', noteId], () => getNote(noteId), {
        initialData: () =>
            (client.getQueryData('notes') as Note[] | undefined)?.find(
                (n) => n.id === noteId
            ),
        initialDataUpdatedAt: client.getQueryState('notes')?.dataUpdatedAt,
    });
};

export default useNote;
