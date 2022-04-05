import { Outlet } from 'react-router-dom';

const NoteLayout = () => {
    return (
        <>
            <p>Layout works yay!!!</p>
            <Outlet />
        </>
    );
};

export default NoteLayout;
