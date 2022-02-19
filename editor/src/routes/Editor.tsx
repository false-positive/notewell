import { Box, Stack, Theme } from '@mui/material';
import StatusBar from '../components/StatusBar';

const Editor = () => {
    return (
        <Stack sx={{ height: '100vh' }}>
            <Box sx={{ height: '100%' }}>content</Box>
            <StatusBar />
        </Stack>
    );
};

export default Editor;
