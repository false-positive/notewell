<script>
    import IconButton from '@smui/icon-button/IconButton.svelte';
    import { Editor } from 'typewriter-editor';
    import Dialog, { Title, Content } from '@smui/dialog';
    import CircularProgress from '@smui/circular-progress';
    import Root from 'typewriter-editor/lib/Root.svelte';
    import Toolbar from 'typewriter-editor/lib/Toolbar.svelte';
    import { onMount } from 'svelte';

    const editor = new Editor();

    let open = false;

    onMount(() => {
        setTimeout(() => {
            open = true;
            setTimeout(() => (open = false), 5673);
        }, 600);
    });
</script>

<Toolbar {editor} let:commands>
    <div class="toolbar">
        <IconButton class="material-icons" on:click={commands.header1}>
            title
        </IconButton>

        <IconButton class="material-icons" on:click={commands.header2}>
            title
        </IconButton>

        <IconButton class="material-icons" on:click={commands.bold}>
            format_bold
        </IconButton>

        <IconButton class="material-icons" on:click={commands.italic}>
            format_italic
        </IconButton>

        <IconButton class="material-icons" on:click={commands.undo}>
            undo
        </IconButton>

        <IconButton class="material-icons" on:click={commands.redo}>
            redo
        </IconButton>
    </div>
</Toolbar>

<!-- TODO: change -->
<div class="asd">
    <div class="mdc-elevation--z3 asd__sheet">
        <Root {editor} />
    </div>
</div>

<Dialog bind:open>
    <Title>Shortening Text...</Title>
    <Content>
        Please wait as your selection is being shortened...
        <br />
        <div style="display: flex; justify-content: center; margin: 1em">
            <CircularProgress
                style="height: 32px; width: 32px;"
                indeterminate
            />
        </div>
    </Content>
</Dialog>

<style>
    .toolbar {
        position: sticky;
    }
    .asd {
        background: #e6eff3;
        padding: 0.3em;
        overflow-x: wrap;
        overflow-y: scroll;
        /* height: 51.5em; */
        height: 48.5em;
    }

    .asd__sheet {
        background: #fff;
        width: 80em;
        min-height: 85em;
        padding: 1em 3em;
        margin: 1.5em auto 1.5em auto;
        font-family: Roboto;
    }

    :global(.focus) {
        outline: none;
    }
</style>
