import { FC } from 'react';
import { Avatar, Box, Paper, Skeleton, Stack, Typography } from '@mui/material';
import EditorLogo from './EditorLogo';
import { Note } from '../../api/notes';
import NoteLinks from './NoteLinks';

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
