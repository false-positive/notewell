import { styled } from '@mui/system';

const EditorLogo = styled(({ ...props }) => (
    <a href="/notes/my/">
        <img {...props} src="/static/notes/img/logo.svg" alt="Notewell" />
    </a>
))({
    width: '3em',
    height: '3em',
    paddingLeft: '1em',
    paddingRight: '1em',
    filter: 'invert(100%)',
    cursor: 'pointer',
});

export default EditorLogo;
