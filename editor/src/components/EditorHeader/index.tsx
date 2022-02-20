import { FC } from 'react';
import { Avatar, Box, Paper, Skeleton, Stack, Typography } from '@mui/material';
import EditorLogo from './EditorLogo';
import { Note } from '../../api/notes';
import NoteLinks from './NoteLinks';
import NoteTitleCategories from './NoteTitleCategories';

type Props = {
    note?: Note;
};

const EditorHeader: FC<Props> = ({ note }) => {
    return (
        <Paper elevation={4}>
            <Stack
                direction="row"
                justifyContent="space-between"
                paddingY={1.5}
            >
                <Stack direction="row" spacing={2}>
                    <EditorLogo />
                    <Stack>
                        <NoteTitleCategories note={note} />
                        {/* TODO: menus */}
                    </Stack>
                </Stack>
                <Stack direction="row" spacing={1.5} alignItems="center">
                    {note && <NoteLinks note={note} />}

                    <Box paddingX={2}>
                        <Avatar />
                    </Box>
                </Stack>
            </Stack>
        </Paper>
    );
};

export default EditorHeader;
