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

export {};
