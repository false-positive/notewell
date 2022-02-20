import { FC, useState } from 'react';
import type { MouseEvent } from 'react';
import {
    Button,
    Divider,
    List,
    ListItem,
    ListItemIcon,
    ListItemSecondaryAction,
    ListItemText,
    Menu,
    MenuItem,
    Skeleton,
} from '@mui/material';
import type { PermissionLevel } from '../../api/permissions';
import ExpandMore from '@mui/icons-material/ExpandMore';
import VisibilityIcon from '@mui/icons-material/Visibility';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

// TODO: figure out how to make it so onChange and onDelete are required if permLevel !== null
// type Props =
//   | {
//       username: string;
//       permLevel: PermissionLevel;
//       onChange: (premLevel: PermissionLevel) => void;
//       onDelete: () => void;
//     }
//   | {
//       username: string;
//       permLevel: 'author';
//     };
type Props = {
    username: string | null;
    permLevel: PermissionLevel | 'author';
    disabled?: boolean;
    onChange?: (premLevel: PermissionLevel) => void;
    onDelete?: () => void;
};

const PERM_LEVEL_READABLE: Record<PermissionLevel | 'author', string> = {
    author: 'Author',
    R: 'Viewer',
    W: 'Editor',
};

const PermissionListItem: FC<Props> = ({
    username,
    permLevel,
    disabled,
    onChange,
    onDelete,
}) => {
    const [anchorEl, setAnchorEl] = useState<HTMLButtonElement | null>(null);
    const menuOpen = anchorEl !== null;

    const handleMenuOpen = (e: MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(e.currentTarget);
    };
    const handleMenuClose = () => {
        setAnchorEl(null);
    };

    const handleChange = (permLevel: PermissionLevel) => {
        onChange!(permLevel);
        handleMenuClose();
    };
    const handleDelete = () => {
        onDelete!();
        handleMenuClose();
    };

    return (
        <ListItem>
            {username ? (
                <ListItemText>{username}</ListItemText>
            ) : (
                <Skeleton animation="wave">
                    <ListItemText>xhhsdf</ListItemText>
                </Skeleton>
            )}
            <ListItemSecondaryAction>
                <Button
                    id={`${username}-permissions-button`}
                    aria-controls={menuOpen ? 'basic-menu' : undefined}
                    aria-haspopup="true"
                    aria-expanded={menuOpen ? 'true' : undefined}
                    disabled={permLevel === 'author' || disabled}
                    endIcon={permLevel !== 'author' && <ExpandMore />}
                    onClick={handleMenuOpen}
                >
                    {PERM_LEVEL_READABLE[permLevel]}
                </Button>
                <Menu
                    id={`${username}-permissions-menu`}
                    anchorEl={anchorEl}
                    open={menuOpen}
                    onClose={handleMenuClose}
                    MenuListProps={{
                        'aria-labelledby': `${username}-permissions-button`,
                    }}
                >
                    <MenuItem onClick={() => handleChange('R')}>
                        <ListItemIcon>
                            <VisibilityIcon fontSize="small" />
                        </ListItemIcon>
                        <ListItemText>Viewer</ListItemText>
                    </MenuItem>
                    <MenuItem onClick={() => handleChange('W')}>
                        <ListItemIcon>
                            <EditIcon fontSize="small" />
                        </ListItemIcon>
                        <ListItemText>Editor</ListItemText>
                    </MenuItem>
                    <Divider />
                    <MenuItem onClick={handleDelete}>
                        <ListItemIcon>
                            <DeleteIcon fontSize="small" />
                        </ListItemIcon>
                        <ListItemText>Remove</ListItemText>
                    </MenuItem>
                </Menu>
            </ListItemSecondaryAction>
        </ListItem>
    );
};

export default PermissionListItem;
