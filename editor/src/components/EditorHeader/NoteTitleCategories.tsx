import { Box, ButtonBase, Skeleton, Stack, Typography } from '@mui/material';
import { FC } from 'react';
import { Note } from '../../api/notes';
import NoteTitle from './NoteTitle';

type Props = {
    note?: Note;
};

const NoteTitleCategories: FC<Props> = ({ note }) => {
    return (
        <Stack direction="row" spacing={2} alignItems="center">
            {note ? (
                <NoteTitle title={note.title} />
            ) : (
                <Skeleton animation="wave">
                    <NoteTitle title="jdfghujsgfhoiwueroighuobjsdfklg" />
                </Skeleton>
            )}
        </Stack>
    );
};

export default NoteTitleCategories;
