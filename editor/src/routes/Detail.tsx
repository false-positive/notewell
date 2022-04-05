import { Link } from 'react-router-dom';
import useURLNote from '../hooks/useURLNote';

const DetailRoute = () => {
    const note = useURLNote();
    return (
        <div>
            <h1>{note.data?.title}</h1>
            <Link to="/notes/">back</Link>
        </div>
    );
};

export default DetailRoute;
