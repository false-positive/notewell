import {
    AppBar,
    Box,
    Button,
    IconButton,
    Stack,
    Toolbar,
    Typography,
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import useMe from '../../hooks/useMe';
import AvatarMenu from './AvatarMenu';
import { useLocation } from 'react-router-dom';

const Header = () => {
    const me = useMe();
    const location = useLocation();

    return (
        <AppBar>
            <Toolbar>
                <IconButton
                    size="large"
                    edge="start"
                    color="inherit"
                    aria-label="menu"
                    sx={{ mr: 2 }}
                >
                    <MenuIcon />
                </IconButton>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    News
                </Typography>
                <Box paddingX={2}>
                    {me.data?.user ? (
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
