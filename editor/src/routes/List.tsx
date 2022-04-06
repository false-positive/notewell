import { Link } from 'react-router-dom';
import HeaderStuff from '../components/Header/HeaderStuff';
import useNotes from '../hooks/useNotes';
import useTitle from '../hooks/useTitle';

const ListRoute = () => {
    const notes = useNotes();
    useTitle('All Notes');

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
