type Note = {
    isLocal: true;
    uuid: string;
    author: string;
    title: string;
    content: string;
    categories: string[];
    creation_date: Date;
};

type NoteData = {
    uuid: string;
    title: string;
    content: string;
    categories: string[];
};

/**
 * a.k.a. SharedItem in the Django source ;-;
 */
type Permission = {
    user: string;
    perm_level: 'R' | 'W';
};

type User = {
    username: string;
    email: string;
    first_name: string;
    last_name: string;
};

export {};
