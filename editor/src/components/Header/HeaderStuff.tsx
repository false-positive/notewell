import { Portal } from '@mui/material';
import { FC, useContext } from 'react';
import HeaderContext from './HeaderContext';

const HeaderStuff: FC = ({ children }) => {
    const { contentRef } = useContext(HeaderContext);
    return !!contentRef ? (
        <Portal container={contentRef.current}>{children}</Portal>
    ) : null;
};

export default HeaderStuff;
