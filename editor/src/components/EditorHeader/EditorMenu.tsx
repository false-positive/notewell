import { FC, useState } from 'react';
import type { MouseEvent } from 'react';
import { ButtonBase, Menu, styled } from '@mui/material';

const MenuButton = styled(ButtonBase)(({ theme }) => ({
    ...theme.typography.body2,
    padding: '.3rem .4rem',
}));

type Props = {
    name: string;
    id: string;
};

const EditorMenu: FC<Props> = ({ name, id, children }) => {
    const [anchorEl, setAnchorEl] = useState<HTMLButtonElement | null>(null);
    const open = anchorEl !== null;

    const handleOpen = (e: MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(e.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    return (
        <>
            <MenuButton
                id={`editor-${id}-menu-button`}
                aria-controls={open ? `editor-${id}-menu-button` : undefined}
                aria-haspopup="true"
                aria-expanded={open ? 'true' : undefined}
                onClick={handleOpen}
            >
                {name}
            </MenuButton>
            <Menu
                id={`editor-${id}-menu`}
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
                MenuListProps={{
                    'aria-labelledby': `editor-${id}-menu-button`,
                }}
            >
                {children}
            </Menu>
        </>
    );
};

export default EditorMenu;
