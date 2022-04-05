import { Box, Stack } from '@mui/material';
import ContentEditor from '../components/ContentEditor';
import EditorHeader from '../components/EditorHeader';
import StatusBar from '../components/StatusBar';
import useURLNote from '../hooks/useURLNote';

const EditorRoute = () => {
    const note = useURLNote({ canEdit: true });

    return (
        <Stack sx={{ height: '100vh' }}>
            <EditorHeader
                note={note.data} //
            />
            <Box sx={{ height: '100%' }}>
                {note.data && <ContentEditor note={note.data} />}
            </Box>
            <StatusBar />
        </Stack>
    );
};

export default EditorRoute;
