import { Autocomplete, TextField } from '@mui/material';
import { FC, useEffect, useMemo, useState } from 'react';
import throttle from 'lodash-es/throttle';
import { searchUsers } from '../api/users';

type Props = {
    label: string;
    disabled?: boolean;
    onSelect: (username: string) => void;
};

const UsernameAutocomplete: FC<Props> = ({ label, disabled, onSelect }) => {
    const [inputValue, setInputValue] = useState<string>('');
    const [username, setUsername] = useState<string | null>(null);
    const [options, setOptions] = useState<string[]>([]);

    const fetchUserOptions = useMemo(() => throttle(searchUsers, 200), []);

    useEffect(() => {
        if (inputValue && inputValue !== username) {
            fetchUserOptions(inputValue)?.then(setOptions);
        } else {
            setOptions([]);
        }
    }, [inputValue]); // XXX: do I have to add fetchUserOptions here?

    useEffect(() => {
        if (username) {
            onSelect(username);
            setUsername(null);
            setInputValue('');
        }
    }, [username]);

    return (
        <Autocomplete
            disablePortal
            clearOnBlur
            clearOnEscape
            autoComplete
            autoHighlight
            autoSelect
            options={options}
            filterOptions={(x) => x}
            value={username}
            onChange={(_, v) => setUsername(v)}
            inputValue={inputValue}
            onInputChange={(_, v) => setInputValue(v)}
            sx={{ width: '100%' }}
            disabled={disabled}
            renderInput={(params) => (
                <TextField
                    {...params}
                    label={label}
                    variant="standard"
                    InputProps={{
                        ...params.InputProps,
                        type: 'search',
                    }}
                />
            )}
        />
    );
};

export default UsernameAutocomplete;
