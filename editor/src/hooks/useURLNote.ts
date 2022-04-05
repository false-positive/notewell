import { useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import invariant from 'tiny-invariant';
import useMe from './useMe';
import useNote from './useNote';

type Options = {
    canEdit?: boolean;
};

const useURLNote = ({ canEdit = false }: Options = {}) => {
    const navigate = useNavigate();

    const { noteId } = useParams<{ noteId: string }>();
    invariant(noteId, 'noteId url param not present');
    const note = useNote(noteId);
    const me = useMe({ redirect: canEdit });

    useEffect(() => {
        if (
            canEdit &&
            me.data?.user &&
            note.data &&
            me.data.user.username !== note.data.author
        ) {
            navigate(`/notes/${noteId}/`, { replace: true });
        }
    }, [canEdit, me.data, note]);

    return note;
};

export default useURLNote;
