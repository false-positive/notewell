import { FC, useState } from 'react';
import HrefRouterLink from '../HrefRouterLink';
import { Note } from '../../api/notes';
import ShareDialog from '../ShareDialog';
import PeopleIcon from '@mui/icons-material/People';
import CommentIcon from '@mui/icons-material/Comment';
import QuizIcon from '@mui/icons-material/Quiz';
import { Box, Button, IconButton, Stack } from '@mui/material';

type Props = {
    note: Note;
};

const NoteLinks: FC<Props> = ({ note }) => {
    const [shareOpen, setShareOpen] = useState(false);

    return (
        <Stack direction="row" spacing={1} alignItems="center">
            <IconButton href={`/notes/${note.id}/`}>
                <CommentIcon />
            </IconButton>

            <IconButton
                href={`/notes/${note.id}/quiz/`}
                LinkComponent={HrefRouterLink}
            >
                <QuizIcon />
            </IconButton>

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
        </Stack>
    );
};

export default NoteLinks;