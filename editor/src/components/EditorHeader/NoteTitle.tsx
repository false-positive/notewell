import { FC } from 'react';
import { ButtonBase, Box, Typography } from '@mui/material';

type Props = {
    title: string;
    onClick?: () => void;
};

const NoteTitle: FC<Props> = ({ title, onClick }) => {
    return (
        <ButtonBase onClick={onClick}>
            <Box padding={0.75}>
                <Typography variant="h6">{title}</Typography>
            </Box>
        </ButtonBase>
    );
};

export default NoteTitle;
