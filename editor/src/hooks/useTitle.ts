import { useContext, useEffect } from 'react';
import HeaderContext from '../components/Header/HeaderContext';

const useTitle = (title: string | null) => {
    const { setTitle } = useContext(HeaderContext);
    useEffect(() => {
        setTitle(title);
        return () => setTitle(null);
    }, [title]);
};

export default useTitle;
