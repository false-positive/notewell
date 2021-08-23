<script>
    import { onMount } from 'svelte';
    import { getNote } from './api';

    import Header from './components/Header.svelte';
    import { note } from './stores/note';

    export let api_token;
    export let note_uuid;

    onMount(async () => {
        const data = await getNote(api_token, note_uuid);
        $note = data;
    });
</script>

<main>
    <Header {api_token} />
</main>
