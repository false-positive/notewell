import { Stack } from '@mui/material';
import EditorMenu from './EditorMenu';

const HeaderMenus = () => {
    return (
        <Stack direction="row">
            <EditorMenu name="File" id="file"></EditorMenu>
            <EditorMenu name="Edit" id="edit"></EditorMenu>
            <EditorMenu name="View" id="view"></EditorMenu>
            <EditorMenu name="Insert" id="insert"></EditorMenu>
            <EditorMenu name="Format" id="format"></EditorMenu>
            <EditorMenu name="Extras" id="extras"></EditorMenu>
            <EditorMenu name="Help" id="help"></EditorMenu>
        </Stack>
    );
};

export default HeaderMenus;
