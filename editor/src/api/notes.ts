import invariant from 'tiny-invariant';
import { makeAuthRequest } from './request';

export type Note = {
    id: string;
    title: string;
    author: string;
    content: string;
    categories: string[];
    creationDate: Date;
};

type APINote = {
    uuid: string;
    title: string;
    author: string;
    content: string;
    categories: string[];
    creation_date: string;
};

const fromAPINote = ({ uuid, creation_date, ...attrs }: APINote): Note => ({
    id: uuid,
    creationDate: new Date(creation_date),
    ...attrs,
});

export const getNote = async (noteId: string): Promise<Note> => {
    const response = await makeAuthRequest(`notes/${noteId}/`);
    invariant(response.status === 200, 'note request failed');
    const { data } = await response.json();
    return fromAPINote(data as APINote);
};
