import { IconButton, Skeleton, Stack } from '@mui/material';
import { FC } from 'react';
import { Note } from '../../api/notes';
import NoteTitle from './NoteTitle';
import LibraryBooksOutlinedIcon from '@mui/icons-material/LibraryBooksOutlined';

type Props = {
    note?: Note;
};

const NoteTitleCategories: FC<Props> = ({ note }) => {
    return (
        <Stack direction="row" spacing={2} alignItems="center">
            {!note ? (
                <Skeleton animation="wave">
                    <NoteTitle title="jdfghujsgfhoiwueroighuobjsdfklg" />
                </Skeleton>
            ) : (
                <>
                    <NoteTitle title={note.title} />
                    <IconButton>
                        <LibraryBooksOutlinedIcon />
                    </IconButton>
                </>
            )}
        </Stack>
    );
};

export default NoteTitleCategories;
