import { Link } from 'react-router-dom';
import useURLNote from '../hooks/useURLNote';

const QuizRoute = () => {
    const note = useURLNote();

    return (
        <>
            <p>Quiz for {note.data?.title} works yay!!!</p>
            <Link to={`/notes/${note.data?.id}/edit/`}>Edit</Link>
        </>
    );
};

export default QuizRoute;
