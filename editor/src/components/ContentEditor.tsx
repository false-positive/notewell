import { QuizOutlined } from '@mui/icons-material';
import 'quill/dist/quill.snow.css';
import { FC, useEffect } from 'react';
import { useQuill } from 'react-quilljs';
import { Note } from '../api/notes';
import { mdToHtml } from '../utils/markdown';

type Props = {
    note: Note;
};

const ContentEditor: FC<Props> = ({ note }) => {
    const { quill, quillRef } = useQuill();

    useEffect(() => {
        if (quill) {
            quill.on('text-change', (_delta, _oldDelta, src) => {
                if (src === 'user') {
                    // update note here, debounced
                }
            });
        }
    }, [quill]);

    useEffect(() => {
        if (quill) {
            const safeHtml = mdToHtml(note.content);
            if (quill.root.innerHTML.trim() !== safeHtml.trim()) {
                quill.clipboard.dangerouslyPasteHTML(safeHtml);
                console.log(quill.root.innerHTML.trim() === safeHtml.trim());
            }
        }
    }, [quill, note.content]);

    return <div ref={quillRef} />;
};

export default ContentEditor;
