import { useQuery } from 'react-query';
import { getNote } from '../api/notes';

const useNote = (noteId: string) =>
    useQuery(['note', noteId], () => getNote(noteId));

export default useNote;
