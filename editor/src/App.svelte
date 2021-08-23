<script>
    import { onMount } from 'svelte';
    import { getNote, setToken } from './api';

    import Header from './components/Header.svelte';
    import { note } from './stores/note';

    export let api_token;
    export let note_uuid;

    onMount(async () => {
        setToken(api_token);
        const data = await getNote(note_uuid);
        $note = data;
    });
</script>

<main>
    <Header />
</main>
