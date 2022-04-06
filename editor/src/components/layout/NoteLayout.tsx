import { useEffect, useRef, useState } from 'react';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import { Outlet } from 'react-router-dom';
import Drawer from '../Drawer/Drawer';
import DrawerHeader from '../Drawer/DrawerHeader';
import Header from '../Header';
import HeaderContext from '../Header/HeaderContext';
import Main from '../Main';

const drawerWidth = 240;

const NoteLayout = () => {
    const [open, setOpen] = useState(false);
    const [title, setTitle] = useState<string | null>(null);
    const contentRef = useRef<Element>();

    useEffect(() => {
        document.title = `${title ?? 'Loading...'} // Notewell`;
    }, [title]);

    const handleDrawerOpen = () => {
        setOpen(true);
    };

    const handleDrawerClose = () => {
        setOpen(false);
    };

    return (
        <HeaderContext.Provider value={{ title, setTitle, contentRef }}>
            <Box sx={{ display: 'flex' }}>
                <CssBaseline />
                <Header
                    open={open}
                    onDrawerOpen={handleDrawerOpen}
                    drawerWidth={drawerWidth}
                />

                <Drawer
                    open={open}
                    onClose={handleDrawerClose}
                    width={drawerWidth}
                />

                <Main open={open} drawerWidth={drawerWidth}>
                    <DrawerHeader />
                    <Outlet />
                </Main>
            </Box>
        </HeaderContext.Provider>
    );
};

export default NoteLayout;
