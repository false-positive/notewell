import React from 'react';

const HeaderContext = React.createContext<{
    title: string | null;
    setTitle: (title: string) => void;
    contentRef?: React.MutableRefObject<Element | undefined>;
}>({ title: null, setTitle: () => {} });

export default HeaderContext;
