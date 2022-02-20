import { FC, useState } from 'react';
import {
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Typography,
} from '@mui/material';
import { LoadingButton } from '@mui/lab';
import type { Permission, PermissionLevel } from '../../api/permissions';
import AddPermissionForm from './AddPermissionForm';
import PermissionList from './PermissionList';
import usePermissions from '../../hooks/usePermissions';
import ConfirmationDialog from '../ConfirmationDialog';
import useSavePermissions from '../../hooks/useSavePermissions';
import useNote from '../../hooks/useNote';

type Props = {
    noteID: string;
    open: boolean;
    onClose: () => void;
};

const ShareDialog: FC<Props> = ({ noteID, open, onClose }) => {
    type MaybePermissions = Permission[] | null;
    const [newPermissions, setNewPermissions] =
        useState<MaybePermissions>(null);
    const permissions = usePermissions(noteID, {
        enabled: open && !newPermissions,
    });
    const savePermissions = useSavePermissions(noteID);
    const [confirmationOpen, setConfirmationOpen] = useState(false);

    const note = useNote(noteID);

    const isLoading =
        note.isLoading || permissions.isLoading || savePermissions.isLoading;

    const getPerms = (inPermissions: Permission[] | null): Permission[] => {
        return inPermissions || permissions.data || [];
    };

    const addPermission = (username: string) => {
        setNewPermissions((permissions) => [
            ...getPerms(permissions).filter((p) => p.username !== username),
            { username, permLevel: 'R' },
        ]);
    };
    const handlePermissionChange =
        (username: string) => (permLevel: PermissionLevel) => {
            setNewPermissions((permissions) =>
                getPerms(permissions).map((p) =>
                    p.username === username ? { username, permLevel } : p
                )
            );
        };
    const handlePermissionDelete = (username: string) => () => {
        setNewPermissions((permissions) =>
            getPerms(permissions).filter((p) => p.username !== username)
        );
    };

    const handleDone = async () => {
        if (newPermissions !== null) {
            await savePermissions.mutateAsync(newPermissions);
        }
        onClose();
        setNewPermissions(null);
    };
    const handleClose = () => {
        if (newPermissions !== null) {
            setConfirmationOpen(true);
        } else {
            onClose();
        }
    };
    const handleDiscard = () => {
        onClose();
        setConfirmationOpen(false);
        setNewPermissions(null);
    };

    return (
        <Dialog open={open} onClose={handleClose} fullWidth maxWidth="xs">
            <DialogTitle>Share</DialogTitle>

            <DialogContent>
                <AddPermissionForm disabled={isLoading} onAdd={addPermission} />
                <PermissionList
                    author={note.data?.author ?? null}
                    isLoading={isLoading}
                    permissions={getPerms(newPermissions)}
                    onPermissionChange={handlePermissionChange}
                    onPermissionDelete={handlePermissionDelete}
                />
            </DialogContent>

            <DialogActions>
                {newPermissions !== null && (
                    <Typography variant="overline" sx={{ paddingX: 2 }}>
                        Unsaved Changes
                    </Typography>
                )}
                <LoadingButton
                    loading={savePermissions.isLoading}
                    variant="contained"
                    onClick={handleDone}
                >
                    Done
                </LoadingButton>
                <ConfirmationDialog
                    open={confirmationOpen}
                    onConfirm={handleDiscard}
                    onDeny={() => setConfirmationOpen(false)}
                    content="Discard unsaved changes?"
                    confirmText="Discard"
                    denyText="Cancel"
                />
            </DialogActions>
        </Dialog>
    );
};

export default ShareDialog;
