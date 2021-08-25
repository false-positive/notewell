<script>
    import { fly } from 'svelte/transition';
    import { flip } from 'svelte/animate';
    import { quintOut } from 'svelte/easing';

    import { messages } from '../stores/messages';
    import Alert from './ui/Alert.svelte';
    import { onDestroy, onMount } from 'svelte';
    import { apiOn, apiOff } from '../api';

    const appendMessage = (
        /** @type {import("../stores/messages").Message} */ message
    ) => {
        $messages = [...$messages, message];
    };

    const deleteMessage = (/** @type {number} */ id) => () => {
        $messages = $messages.filter((msg) => msg.id !== id);
    };

    function handleAPIError(err) {
        appendMessage({
            id: new Date().getTime(),
            severity: 'error',
            text: String(err),
        });
    }

    onMount(() => {
        apiOn('error', handleAPIError);
    });
    onDestroy(() => {
        apiOff('error', handleAPIError);
    });
</script>

<div class="floating">
    {#each $messages as message (message.id)}
        <div
            class="container"
            in:fly={{ x: -500, duration: 600, easing: quintOut }}
            out:fly={{ x: 500, duration: 600, easing: quintOut }}
            animate:flip={{ duration: 500, easing: quintOut }}
        >
            <Alert
                severity={message.severity}
                on:click={deleteMessage(message.id)}
            >
                {message.text}
            </Alert>
        </div>
    {/each}
</div>

<style>
    .floating {
        z-index: 1000;
        width: 30%;
        position: fixed;
        bottom: 0;
        right: 0;
    }
</style>
