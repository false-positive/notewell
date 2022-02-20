import { FC } from 'react';
import {
    Avatar,
    Box,
    Button,
    IconButton,
    Paper,
    Skeleton,
    Stack,
    Typography,
} from '@mui/material';
import PeopleIcon from '@mui/icons-material/People';
import CommentIcon from '@mui/icons-material/Comment';
import QuizIcon from '@mui/icons-material/Quiz';
import ShareDialog from '../ShareDialog';
import { useState } from 'react';
import RouterLinkComponent from '../RouterLinkComponent';
import EditorLogo from './EditorLogo';
import { Note } from '../../api/notes';

type Props = {
    note?: Note;
};

const EditorHeader: FC<Props> = ({ note }) => {
    const [shareOpen, setShareOpen] = useState(false);

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
                <Stack direction="row" spacing={2} alignItems="center">
                    <IconButton href="..">
                        <CommentIcon />
                    </IconButton>

                    <IconButton
                        href="../quiz/"
                        LinkComponent={RouterLinkComponent}
                    >
                        <QuizIcon />
                    </IconButton>

                    {note && (
                        <>
                            <Box display="flex" alignItems="center">
                                <Button
                                    variant="contained"
                                    startIcon={<PeopleIcon />}
                                    onClick={() => setShareOpen(true)}
                                >
                                    Share
                                </Button>
                            </Box>
                            <ShareDialog
                                noteID={note.id}
                                open={shareOpen}
                                onClose={() => setShareOpen(false)}
                            />
                        </>
                    )}

                    <Box paddingX={2} marginLeft={1}>
                        <Avatar />
                    </Box>
                </Stack>
            </Stack>
        </Paper>
    );
};

export default EditorHeader;
