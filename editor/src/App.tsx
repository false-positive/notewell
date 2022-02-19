import { Button } from '@mui/material';
import { QueryClient, QueryClientProvider } from 'react-query';

const queryClient = new QueryClient();

const App = () => {
    return (
        <QueryClientProvider client={queryClient}>
            <Button variant="contained">button</Button>
        </QueryClientProvider>
    );
};

export default App;
