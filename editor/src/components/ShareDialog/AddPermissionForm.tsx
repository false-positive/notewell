import { Box } from '@mui/system';
import { FC } from 'react';
import PersonIcon from '@mui/icons-material/Person';
import UsernameAutocomplete from '../UsernameAutocomplete';

type Props = {
    disabled?: boolean;
    onAdd: (username: string) => void;
};

const AddPermissionForm: FC<Props> = ({ disabled, onAdd }) => {
    return (
        <Box sx={{ display: 'flex', alignItems: 'flex-end' }}>
            <PersonIcon sx={{ color: 'action.active', mr: 1, my: 0.5 }} />
            <UsernameAutocomplete
                label="Share with user"
                disabled={disabled}
                onSelect={onAdd}
            />
        </Box>
    );
};

export default AddPermissionForm;
