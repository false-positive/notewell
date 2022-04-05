import { Link } from 'react-router-dom';
import useNotes from '../hooks/useNotes';

const ListRoute = () => {
    const notes = useNotes();

    return (
        <ol>
            {notes.data?.map((note) => (
                <li key={note.id}>
                    <Link to={`/notes/${note.id}/`}>{note.title}</Link>
                </li>
            ))}
        </ol>
    );
};

export default ListRoute;
