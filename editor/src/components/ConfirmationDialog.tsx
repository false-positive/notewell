import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
} from '@mui/material';
import { FC } from 'react';

type Props = {
    open: boolean;
    content: string;
    confirmText: string;
    denyText: string;
    onConfirm: () => void;
    onDeny: () => void;
};

const ConfirmationDialog: FC<Props> = ({
    open,
    content,
    confirmText,
    denyText,
    onConfirm,
    onDeny,
}) => {
    return (
        <Dialog open={open} onClose={onDeny}>
            <DialogContent>
                <DialogContentText>{content}</DialogContentText>
            </DialogContent>
            <DialogActions>
                <Button onClick={onDeny}>{denyText}</Button>
                <Button variant="outlined" onClick={onConfirm}>
                    {confirmText}
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default ConfirmationDialog;
