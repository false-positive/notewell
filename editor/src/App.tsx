import { QueryClient, QueryClientProvider } from 'react-query';

const queryClient = new QueryClient();

const App = () => {
    return (
        <QueryClientProvider client={queryClient}>
            <p>App works yay!!!</p>
        </QueryClientProvider>
    );
};

export default App;
