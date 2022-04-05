import { Box, Stack } from '@mui/material';
import { useEffect } from 'react';
import { Navigate, useNavigate, useParams } from 'react-router-dom';
import invariant from 'tiny-invariant';
import ContentEditor from '../components/ContentEditor';
import EditorHeader from '../components/EditorHeader';
import StatusBar from '../components/StatusBar';
import useMe from '../hooks/useMe';
import useNote from '../hooks/useNote';

const Editor = () => {
    const navigate = useNavigate();

    const { noteId } = useParams<{ noteId: string }>();
    invariant(noteId, 'noteId url param not present');
    const note = useNote(noteId);
    const me = useMe();

    useEffect(() => {
        if (me.data && me.data.username !== note.data?.author) {
            navigate(`/notes/${noteId}/`);
        }
    }, [me.data, note]);

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
