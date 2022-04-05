import { Quiz } from '@mui/icons-material';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import { BrowserRouter, Outlet, Route, Routes } from 'react-router-dom';
import NoteLayout from './components/layout/NoteLayout';
import Editor from './routes/Editor';

const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            staleTime: 60 * 1000, // 1 Minute
        },
    },
});

const App = () => {
    return (
        <QueryClientProvider client={queryClient}>
            <BrowserRouter>
                <Routes>
                    <Route path="/notes/:noteId/" element={<NoteLayout />}>
                        <Route path="edit/" element={<Editor />} />
                        <Route path="quiz/" element={<Quiz />} />
                    </Route>
                </Routes>
            </BrowserRouter>
            <ReactQueryDevtools />
        </QueryClientProvider>
    );
};

export default App;
