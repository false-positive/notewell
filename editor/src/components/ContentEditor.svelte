<script>
    import IconButton from '@smui/icon-button/IconButton.svelte';
    import { Delta, Editor } from 'typewriter-editor';
    import Dialog, { Title, Content } from '@smui/dialog';
    import CircularProgress from '@smui/circular-progress';
    import Root from 'typewriter-editor/lib/Root.svelte';
    import Toolbar from 'typewriter-editor/lib/Toolbar.svelte';
    import { toDelta, fromDelta } from '@slite/quill-delta-markdown';
    import { note } from '../stores/note';
    import { onMount } from 'svelte';

    const editor = new Editor();

    export let saveMs = 1000;

    let shorteningText = false;
    let lastSaveTimeout = null;

    onMount(() => {
        const ops = toDelta($note.content);
        editor.setDelta(new Delta(ops));
    });

    /**
     * @param {Event} event
     */
    function save(event) {
        // @ts-ignore
        if (!event.changedLines.length) return;

        // console.log('asd');
        const content = fromDelta(editor.getDelta().ops);
        note.update($note.uuid, { content });
    }

    editor.on('change', (e) => {
        if (lastSaveTimeout !== null) {
            clearTimeout(lastSaveTimeout);
        }
        lastSaveTimeout = setTimeout(() => save(e), saveMs);
    });

    async function shortenText() {
        shorteningText = true;
        const text = await new Promise((resolve) => setTimeout(resolve, 1000));
        editor.insert(text);
        shorteningText = false;
    }
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

        <IconButton class="material-icons" on:click={shortenText}>
            straighten
        </IconButton>
    </div>
</Toolbar>

<!-- TODO: change -->
<div class="asd">
    <div class="mdc-elevation--z3 asd__sheet">
        <Root {editor} />
    </div>
</div>

<Dialog scrimClickAction="" escapeKeyAction="" open={shorteningText}>
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
