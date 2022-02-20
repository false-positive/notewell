import { Button, IconButton, Stack } from '@mui/material';
import ExpandMore from '@mui/icons-material/ExpandMore';
import RemoveIcon from '@mui/icons-material/Remove';
import AddIcon from '@mui/icons-material/Add';

const EditorZoom = () => {
    return (
        <Stack direction="row" spacing={0.5}>
            <IconButton size="small">
                <RemoveIcon />
            </IconButton>
            <Button color="secondary" endIcon={<ExpandMore />}>
                100%
            </Button>
            <IconButton size="small">
                <AddIcon />
            </IconButton>
        </Stack>
    );
};

export default EditorZoom;
