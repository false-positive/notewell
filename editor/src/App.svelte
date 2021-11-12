<script>
    import { onMount } from 'svelte';
    import { setTokenPair } from './api';
    import ContentEditor from './components/ContentEditor.svelte';
    import Dialogs from './components/Dialogs.svelte';

    import Header from './components/Header.svelte';
    import MessageList from './components/MessageList.svelte';
    import { note } from './stores/note';

    export let initialData;

    onMount(() => {
        const {
            definitely_not_token_pair: { access, refresh },
            note: noteData,
        } = initialData;
        note.setInitial(noteData);
        setTokenPair(access, refresh);
        // TODO: spinner state?
        // note.load(noteData.uuid);
    });

    $: {
        if ($note) {
            document.title = `${$note.title} // Notewell`;
        }
    }
</script>

{#if !$note}
    <h1>hehe i should be a loading spinner</h1>
{:else}
    <Header />

    <main>
        <ContentEditor />
    </main>

    <MessageList />

    <Dialogs />
{/if}

<style>
    :global(body) {
        margin: 0;
    }
    :global(:root) {
        --mdc-theme-primary: #2b4854;
        --mdc-theme-secondary: #1baeea;
        --mdc-theme-background: #e6eff3;
        --mdc-theme-on-primary: #e6eff3;
        --mdc-theme-on-secondary: #39383b;
    }
</style>
