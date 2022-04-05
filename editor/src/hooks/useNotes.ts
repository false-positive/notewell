import { useQuery } from 'react-query';
import { getNotes } from '../api/notes';

const useNotes = () => useQuery('notes', getNotes);

export default useNotes;
