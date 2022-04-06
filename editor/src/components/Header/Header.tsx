import MenuIcon from '@mui/icons-material/Menu';
import {
    Box,
    Button,
    IconButton,
    Skeleton,
    Stack,
    Toolbar,
    Typography,
} from '@mui/material';
import { log } from 'console';
import { FC, useContext } from 'react';
import { useLocation } from 'react-router-dom';
import useMe from '../../hooks/useMe';
import AppBar from './AppBar';
import AvatarMenu from './AvatarMenu';
import HeaderContext from './HeaderContext';

type Props = {
    open: boolean;
    onDrawerOpen: () => void;
    drawerWidth: number;
};

const Header: FC<Props> = ({ open, onDrawerOpen, drawerWidth }) => {
    const { title, contentRef } = useContext(HeaderContext);
    const me = useMe();
    const location = useLocation();

    return (
        <AppBar position="fixed" open={open} drawerWidth={drawerWidth}>
            <Toolbar>
                <IconButton
                    color="inherit"
                    aria-label="open drawer"
                    onClick={onDrawerOpen}
                    edge="start"
                    sx={{ mr: 2, ...(open && { display: 'none' }) }}
                >
                    <MenuIcon />
                </IconButton>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    {title !== null ? title : <Skeleton />}
                </Typography>
                <Box mx={2} sx={{ flexGrow: 1 }} ref={contentRef} />
                <Box paddingX={2}>
                    {!me.data || me.data?.user ? (
                        <AvatarMenu />
                    ) : (
                        <Stack direction="row" gap={3}>
                            <Button
                                href={`/login/?next=${encodeURIComponent(
                                    location.pathname
                                )}`}
                                color="inherit"
                            >
                                Log In
                            </Button>
                        </Stack>
                    )}
                </Box>
            </Toolbar>
        </AppBar>
    );
};

export default Header;
