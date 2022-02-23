import Quill from 'quill';
import 'quill/dist/quill.snow.css';
import { useCallback, useState } from 'react';

const ContentEditor = () => {
    const [quill, setQuill] = useState<Quill | null>(null);

    const wrapperRef = useCallback((wrapper) => {
        if (wrapper == null) return;

        wrapper.innerHTML = '';
        const editor = document.createElement('div');
        wrapper.append(editor);
        const q = new Quill(editor, {
            theme: 'snow',
            // modules: { toolbar: TOOLBAR_OPTIONS },
        });
        // q.disable();
        // q.setText('Loading...');
        setQuill(q);
    }, []);
    return <div ref={wrapperRef} />;
};

export default ContentEditor;
