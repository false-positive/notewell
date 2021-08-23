<script>
    import { onMount } from 'svelte';
    import { setToken } from './api';

    import Header from './components/Header.svelte';
    import { note } from './stores/note';

    export let api_token;
    export let note_uuid;

    onMount(async () => {
        setToken(api_token);
        note.load(note_uuid);
    });
</script>

<main>
    <Header />
</main>
