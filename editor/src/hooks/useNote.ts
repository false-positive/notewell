import { useQuery } from 'react-query';
import { getNote } from '../api/notes';

const useNote = (noteId: string) =>
    useQuery(['note', noteId], () => getNote(noteId), {
        staleTime: 60 * 1000, // 1 minute
    });

export default useNote;
