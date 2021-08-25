<script>
    import { onMount } from 'svelte';
    import { setTokenPair } from './api';

    import Header from './components/Header.svelte';
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

<main>
    <Header />
</main>
