import { QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import NoteLayout from './components/layout/NoteLayout';
import EditorRoute from './routes/Editor';
import QuizRoute from './routes/Quiz';

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
                    <Route path="/notes/" element={<NoteLayout />}>
                        <Route path="" element={<p>note list</p>} />
                        <Route path=":noteId/">
                            <Route path="edit/" element={<EditorRoute />} />
                            <Route path="quiz/" element={<QuizRoute />} />
                        </Route>
                    </Route>
                </Routes>
            </BrowserRouter>
            <ReactQueryDevtools />
        </QueryClientProvider>
    );
};

export default App;
