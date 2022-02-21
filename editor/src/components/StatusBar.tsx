import {
    Link as MuiLink,
    IconButton,
    Paper,
    Stack,
    Typography,
    Divider,
    Tooltip,
} from '@mui/material';
import FullscreenIcon from '@mui/icons-material/Fullscreen';
import EditorZoom from './EditorZoom';

const StatusBar = () => {
    return (
        <Paper elevation={4}>
            <Stack
                direction="row"
                justifyContent="space-between"
                paddingX={0.25}
            >
                <Stack
                    direction="row"
                    alignItems="center"
                    divider={<Divider orientation="vertical" flexItem />}
                    paddingX={2}
                    spacing={2}
                >
                    <Typography variant="overline">v1.0.0</Typography>
                    <MuiLink
                        href="https://github.com/false-positive/notewell"
                        about="_blank"
                        rel="noopener noreferer nofollow"
                        variant="button"
                        underline="hover"
                    >
                        Source Code
                    </MuiLink>
                    <span />
                </Stack>
                <Stack
                    direction="row"
                    alignItems="center"
                    divider={<Divider orientation="vertical" flexItem />}
                    paddingX={0.5}
                    spacing={0.5}
                >
                    <span />
                    <EditorZoom />
                    <Tooltip title="Full Screen Mode">
                        <IconButton
                            size="small"
                            onClick={() =>
                                document.documentElement.requestFullscreen()
                            }
                        >
                            <FullscreenIcon />
                        </IconButton>
                    </Tooltip>
                </Stack>
            </Stack>
        </Paper>
    );
};

export default StatusBar;
