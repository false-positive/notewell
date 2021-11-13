<script>
    import Kitchen from '@smui/snackbar/kitchen';
    import { onDestroy, onMount } from 'svelte';
    import { apiOn, apiOff } from '../api';
    import { messages } from '../stores/messages';

    let kitchen;
    /**
     * @type {Set<Number>}
     */
    let pushedIds = new Set();

    const pushToKitchen = (
        /** @type {import('../stores/messages').Message} */ message
    ) => {
        if (pushedIds.has(message.id)) return;

        const handleDelete = () => {
            deleteMessage(message.id);
            pushedIds.delete(message.id);
        };
        kitchen.push({
            props: {
                variant: 'stacked',
            },
            label: message.text,
            actions: [{ text: 'Got it', onClick: handleDelete }],
            dismissButton: true,
            onDismiss: handleDelete,
            onClose: handleDelete,
        });

        pushedIds.add(message.id);
    };

    const appendMessage = (
        /** @type {import('../stores/messages').Message} */ message
    ) => {
        $messages = [...$messages, message];
    };

    const deleteMessage = (/** @type {Number} */ id) => {
        $messages = $messages.filter((m) => m.id !== id);
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

    $: {
        kitchen && $messages.map(pushToKitchen);
    }
</script>

<Kitchen bind:this={kitchen} dismiss$class="material-icons" />
