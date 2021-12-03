<script>
    import { createEventDispatcher } from 'svelte';
    import TopAppBar, { Row, Section, Title } from '@smui/top-app-bar';
    import IconButton from '@smui/icon-button';

    import { note } from '../stores/note';
    import { isShareDialogOpen } from '../stores/isShareDialogOpen';

    export let backlink = '..';

    const dispatch = createEventDispatcher();

    async function updateTitle(e) {
        note.update($note.uuid, { title: e.target.value });
    }
</script>

<TopAppBar variant="static">
    <Row>
        <Section>
            <IconButton class="material-icons" href={backlink}>
                arrow_backward
            </IconButton>
            <Title>
                <input
                    class="title-input"
                    value={$note?.title}
                    on:change={updateTitle}
                />
            </Title>
        </Section>
        <Section align="end">
            <IconButton
                class="material-icons"
                on:click={() => dispatch('quiz')}
            >
                quiz
            </IconButton>
            <IconButton
                class="material-icons"
                on:click={() => ($isShareDialogOpen = true)}
            >
                share
            </IconButton>
        </Section>
    </Row>
</TopAppBar>

<style>
    .title-input {
        background: none;
        border: none;
        font: inherit;
        color: inherit;
        outline: none;
    }
</style>
