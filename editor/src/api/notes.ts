import invariant from 'tiny-invariant';
import { makeAuthRequest } from './request';

export type Note = {
    id: string;
    title: string;
    content: string;
    categories: string[];
};

type APINote = {
    uuid: string;
    title: string;
    content: string;
    categories: string[];
};

const fromAPINote = ({ uuid, ...attrs }: APINote): Note => ({
    id: uuid,
    ...attrs,
});

export const getNote = async (noteId: string): Promise<Note> => {
    const response = await makeAuthRequest(`notes/${noteId}/`);
    invariant(response.status === 200, 'note request failed');
    const { data } = await response.json();
    return fromAPINote(data as APINote);
};
