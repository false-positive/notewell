import 'quill/dist/quill.snow.css';
import { useQuill } from 'react-quilljs';

const ContentEditor = () => {
    const { quill, quillRef } = useQuill();

    return <div ref={quillRef} />;
};

export default ContentEditor;
