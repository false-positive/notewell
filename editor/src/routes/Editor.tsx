import { Box, Stack } from '@mui/material';
import { useParams } from 'react-router-dom';
import invariant from 'tiny-invariant';
import EditorHeader from '../components/EditorHeader';
import StatusBar from '../components/StatusBar';
import useNote from '../hooks/useNote';

const Editor = () => {
    const { noteId } = useParams<{ noteId: string }>();
    invariant(noteId, 'noteId url param not present');
    const note = useNote(noteId);
    return (
        <Stack sx={{ height: '100vh' }}>
            <EditorHeader
                note={note.data} //
            />
            <Box sx={{ height: '100%' }}>content</Box>
            <StatusBar />
        </Stack>
    );
};

export default Editor;
