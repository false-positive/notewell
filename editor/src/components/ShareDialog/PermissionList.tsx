import { LinearProgress, List } from '@mui/material';
import { FC } from 'react';
import PermissionListItem from './PermissionListItem';
import type { Permission, PermissionLevel } from '../../api/permissions';

type PL = PermissionLevel; // just to prevent prettier from wrapping

type Props = {
    isLoading: boolean;
    author: string | null;
    permissions: Permission[];
    onPermissionChange: (username: string) => (permLevel: PL) => void;
    onPermissionDelete: (username: string) => () => void;
};

const PermissionList: FC<Props> = ({
    author,
    isLoading,
    permissions,
    onPermissionChange,
    onPermissionDelete,
}) => {
    return (
        <List sx={{ marginTop: 3 }}>
            {isLoading && <LinearProgress />}
            <PermissionListItem username={author} permLevel="author" />
            {permissions.map(({ username, permLevel }) => (
                <PermissionListItem
                    key={username}
                    username={username}
                    permLevel={permLevel}
                    disabled={isLoading}
                    onChange={onPermissionChange(username)}
                    onDelete={onPermissionDelete(username)}
                />
            ))}
        </List>
    );
};

export default PermissionList;
