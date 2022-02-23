<script>
    import IconButton from '@smui/icon-button/IconButton.svelte';
    import { Editor } from 'typewriter-editor';
    import Dialog, { Title, Content } from '@smui/dialog';
    import CircularProgress from '@smui/circular-progress';
    import Toolbar from 'typewriter-editor/lib/Toolbar.svelte';
    import { note } from '../stores/note';
    import { onMount } from 'svelte';
    import { summarizeText } from '../api';
    import TurndownService from 'turndown';
    import { Parser, HtmlRenderer } from 'commonmark';
    import asRoot from 'typewriter-editor/lib/asRoot';

    const editor = new Editor();

    export let saveMs = 500;

    let shorteningText = false;
    let lastSaveTimeout = null;

    let initialText = '';

    onMount(() => {
        // const ops = toDelta($note.content);
        // editor.setDelta(new Delta(ops));
        const reader = new Parser();
        const writer = new HtmlRenderer();
        const parsed = reader.parse($note.content);
        initialText = writer.render(parsed);
    });

    /**
     * @param {Event} event
     */
    function save(event) {
        // @ts-ignore
        if (!event?.changedLines?.length) return;

        // const content = fromDelta(editor.getDelta().ops);
        const tds = new TurndownService();
        const content = tds.turndown(editor.root);

        note.update($note.uuid, { content });
    }

    editor.on('change', (e) => {
        if (lastSaveTimeout !== null) {
            clearTimeout(lastSaveTimeout);
        }
        lastSaveTimeout = setTimeout(() => save(e), saveMs);
    });

    async function summarizeSelection() {
        if (!editor.doc.selection) return;

        shorteningText = true;
        const selection = editor.doc.getText(editor.doc.selection);
        const result = await summarizeText(selection);

        const lines = Object.values(result)
            .map((ps) => ps.map((p) => p.trim()).join('\n'))
            .join('\n\n');
        editor.insert(lines);
        shorteningText = false;
    }
</script>

<Toolbar {editor} let:commands let:active>
    <div class="toolbar">
        <IconButton class="material-icons" on:click={commands.bold}>
            format_bold
        </IconButton>
        <IconButton class="material-icons" on:click={commands.italic}>
            format_italic
        </IconButton>
        <IconButton class="material-icons" on:click={commands.paragraph}>
            format_size
        </IconButton>

        <div class="toolbar-section">
            <IconButton class="material-icons" on:click={commands.header1}>
                looks_one
            </IconButton>
            <IconButton class="material-icons" on:click={commands.header2}>
                looks_two
            </IconButton>
            <IconButton class="material-icons" on:click={commands.header3}>
                looks_3
            </IconButton>
            <IconButton class="material-icons" on:click={commands.orderedList}>
                format_list_numbered
            </IconButton>
            <IconButton class="material-icons" on:click={commands.bulletList}>
                format_list_bulleted
            </IconButton>
            <IconButton class="material-icons" on:click={commands.blockquote}>
                format_quote
            </IconButton>
            <IconButton
                class="material-icons"
                on:click={commands['code-block']}
            >
                code
            </IconButton>
        </div>

        <div>
            <IconButton class="material-icons" on:click={summarizeSelection}>
                summarize
            </IconButton>
        </div>

        <div class="toolbar-section">
            <IconButton class="material-icons" on:click={commands.undo}>
                undo
            </IconButton>
            <IconButton class="material-icons" on:click={commands.redo}>
                redo
            </IconButton>
        </div>
    </div>
</Toolbar>

<!-- TODO: change -->
<div class="asd">
    <div class="mdc-elevation--z3 asd__sheet">
        <!-- <Root {editor} /> -->
        <div use:asRoot={editor}>{@html initialText}</div>
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
        background: white;
        position: sticky;
        display: flex;
        align-items: center;
        padding: 0.3em 2em;
    }
    .asd {
        background: #e6eff3;
        padding: 0.3em;
        overflow-x: wrap;
        overflow-y: scroll;
        height: 66.5em;
    }

    .asd__sheet {
        background: #fff;
        width: 80em;
        min-height: 85em;
        padding: 1em 3em;
        margin: 1.5em auto 1.5em auto;
        font-family: Roboto;
    }

    .toolbar-section {
        padding-left: 0.75em;
        margin-left: 0.75em;
        border-left: 0.5px solid hsl(198, 35%, 76%);
    }

    :global(.focus) {
        outline: none;
    }
</style>
