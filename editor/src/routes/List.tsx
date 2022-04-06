import { Link } from 'react-router-dom';
import HeaderStuff from '../components/Header/HeaderStuff';
import useNotes from '../hooks/useNotes';

const ListRoute = () => {
    const notes = useNotes();

    return (
        <ol>
            <HeaderStuff>stuff</HeaderStuff>
            {notes.data?.map((note) => (
                <li key={note.id}>
                    <Link to={`/notes/${note.id}/`}>{note.title}</Link>
                </li>
            ))}
        </ol>
    );
};

export default ListRoute;
