import { Button } from '@mui/material';
import { useState } from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import ShareDialog from './components/ShareDialog';

const queryClient = new QueryClient();

const App = () => {
    const [open, setOpen] = useState(true);

    return (
        <QueryClientProvider client={queryClient}>
            <Button variant="contained" onClick={() => setOpen(true)}>
                Share
            </Button>
            <ShareDialog
                noteID="e5da113b-50e6-418f-9dff-0ebef608ab39"
                open={open}
                onClose={() => setOpen(false)}
            />
            <ReactQueryDevtools />
        </QueryClientProvider>
    );
};

export default App;
