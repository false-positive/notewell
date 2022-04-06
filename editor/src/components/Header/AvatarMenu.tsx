import { Avatar, IconButton, Menu, MenuItem, Skeleton } from '@mui/material';
import { useState } from 'react';
import useMe from '../../hooks/useMe';

function stringToColor(string: string) {
    let hash = 0;
    let i;

    /* eslint-disable no-bitwise */
    for (i = 0; i < string.length; i += 1) {
        hash = string.charCodeAt(i) + ((hash << 5) - hash);
    }

    let color = '#';

    for (i = 0; i < 3; i += 1) {
        const value = (hash >> (i * 8)) & 0xff;
        color += `00${value.toString(16)}`.slice(-2);
    }
    /* eslint-enable no-bitwise */

    return color;
}

function stringAvatar(name: string) {
    return {
        sx: {
            bgcolor: stringToColor(name),
        },
        children: name[0].toUpperCase(),
    };
}

const AvatarMenu = () => {
    const me = useMe();
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

    const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    return (
        <div>
            {me.data ? (
                <>
                    <IconButton
                        size="large"
                        aria-label="account of current user"
                        aria-controls="menu-appbar"
                        aria-haspopup="true"
                        onClick={handleMenu}
                        color="inherit"
                    >
                        <Avatar {...stringAvatar(me.data.user!.username)} />
                    </IconButton>
                    <Menu
                        id="menu-appbar"
                        anchorEl={anchorEl}
                        anchorOrigin={{
                            vertical: 'bottom',
                            horizontal: 'center',
                        }}
                        keepMounted
                        transformOrigin={{
                            vertical: 'top',
                            horizontal: 'center',
                        }}
                        open={Boolean(anchorEl)}
                        onClose={handleClose}
                    >
                        <MenuItem
                            href={`/user/${me.data.user!.username}/`}
                            component="a"
                            onClick={handleClose}
                        >
                            Profile
                        </MenuItem>
                        <MenuItem
                            href="/logout/"
                            component="a"
                            onClick={handleClose}
                        >
                            Log Out
                        </MenuItem>
                    </Menu>
                </>
            ) : (
                <IconButton size="large">
                    <Skeleton variant="circular">
                        <Avatar />
                    </Skeleton>
                </IconButton>
            )}
        </div>
    );
};

export default AvatarMenu;
