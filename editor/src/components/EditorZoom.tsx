import { useState } from 'react';
import type { MouseEvent } from 'react';
import { Button, IconButton, Menu, MenuItem, Stack } from '@mui/material';
import ExpandMore from '@mui/icons-material/ExpandMore';
import RemoveIcon from '@mui/icons-material/Remove';
import AddIcon from '@mui/icons-material/Add';

const EditorZoom = () => {
    const [anchorEl, setAnchorEl] = useState<HTMLButtonElement | null>(null);
    const menuOpen = anchorEl !== null;

    const handleMenuOpen = (e: MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(e.currentTarget);
    };
    const handleMenuClose = () => {
        setAnchorEl(null);
    };

    return (
        <Stack direction="row" spacing={0.5}>
            <IconButton size="small">
                <RemoveIcon />
            </IconButton>
            <Menu
                id="editor-zoom-menu"
                open={menuOpen}
                anchorEl={anchorEl}
                anchorOrigin={{ horizontal: 'center', vertical: 'top' }}
                transformOrigin={{ horizontal: 'center', vertical: 'bottom' }}
                elevation={1}
                onClose={handleMenuClose}
                MenuListProps={{
                    'aria-labelledby': 'editor-zoom-menu-button',
                }}
            >
                <MenuItem onClick={handleMenuClose}>Zoom to Content</MenuItem>
                <MenuItem onClick={handleMenuClose}>Zoom to Width</MenuItem>
                <MenuItem onClick={handleMenuClose}>Zoom to Page</MenuItem>
            </Menu>
            <Button
                color="secondary"
                id="editor-zoom-menu-button"
                aria-controls={anchorEl ? 'editor-zoom-menu-button' : undefined}
                aria-haspopup="true"
                aria-expanded={anchorEl ? 'true' : undefined}
                onClick={handleMenuOpen}
                endIcon={<ExpandMore />}
            >
                100%
            </Button>
            <IconButton size="small">
                <AddIcon />
            </IconButton>
        </Stack>
    );
};

export default EditorZoom;
