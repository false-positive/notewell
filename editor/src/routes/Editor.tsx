import { Box, Stack } from '@mui/material';
import EditorHeader from '../components/EditorHeader';
import StatusBar from '../components/StatusBar';

const Editor = () => {
    return (
        <Stack sx={{ height: '100vh' }}>
            <EditorHeader />
            <Box sx={{ height: '100%' }}>content</Box>
            <StatusBar />
        </Stack>
    );
};

export default Editor;
