import { Avatar, Box, Button, IconButton, Paper, Stack } from '@mui/material';
import PeopleIcon from '@mui/icons-material/People';
import CommentIcon from '@mui/icons-material/Comment';
import QuizIcon from '@mui/icons-material/Quiz';
import ShareDialog from '../ShareDialog';
import { useState } from 'react';
import RouterLinkComponent from '../RouterLinkComponent';

const EditorHeader = () => {
    const [shareOpen, setShareOpen] = useState(false);

    return (
        <Paper elevation={4}>
            <Stack
                direction="row"
                justifyContent="space-between"
                paddingY={1.5}
            >
                <span>things</span>
                <Stack direction="row" spacing={2}>
                    <IconButton href="..">
                        <CommentIcon />
                    </IconButton>

                    <IconButton
                        href="../quiz/"
                        LinkComponent={RouterLinkComponent}
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
                        noteID="925e33e0-477a-4cca-b2cf-bff94c6d7ecc"
                        open={shareOpen}
                        onClose={() => setShareOpen(false)}
                    />
                    <Box paddingX={2} marginLeft={1}>
                        <Avatar />
                    </Box>
                </Stack>
            </Stack>
        </Paper>
    );
};

export default EditorHeader;
