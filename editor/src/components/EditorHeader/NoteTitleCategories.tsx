import { Skeleton, Stack, Typography } from '@mui/material';
import { FC } from 'react';
import { Note } from '../../api/notes';

type Props = {
    note?: Note;
};

const NoteTitleCategories: FC<Props> = ({ note }) => {
    return (
        <Stack direction="row" spacing={2} alignItems="center">
            {note ? (
                <Typography variant="h6">{note?.title}</Typography>
            ) : (
                <Skeleton animation="wave">
                    <Typography variant="h6">
                        jdfghujsgfhoiwueroighuobjsdfklg
                    </Typography>
                </Skeleton>
            )}
        </Stack>
    );
};

export default NoteTitleCategories;
