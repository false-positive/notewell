<script>
    import { note } from '../stores/note';

    export let saveTimeout = 1000;

    let timeout = null;
    function handleInput(e) {
        if (timeout !== null) {
            clearTimeout(timeout);
        }
        timeout = setTimeout(() => updateContent(e.target.value), saveTimeout);
    }

    function updateContent(content) {
        note.update($note.uuid, { content });
    }
</script>

<textarea on:input={handleInput}>{$note?.content}</textarea>
