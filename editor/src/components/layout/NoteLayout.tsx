import { Stack } from '@mui/material';
import { Outlet } from 'react-router-dom';
import Header from '../Header';

const NoteLayout = () => {
    return (
        <Stack sx={{ height: '100vh' }}>
            <Header />
            <p>Layout works yay!!!</p>
            <Outlet />
        </Stack>
    );
};

export default NoteLayout;
