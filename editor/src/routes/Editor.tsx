import { Box, Stack } from '@mui/material';
import { useParams } from 'react-router-dom';
import invariant from 'tiny-invariant';
import ContentEditor from '../components/ContentEditor';
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
            <Box sx={{ height: '100%' }}>
                {note.data && <ContentEditor note={note.data} />}
            </Box>
            <StatusBar />
        </Stack>
    );
};

export default Editor;
