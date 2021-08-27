<script>
    import TopAppBar, { Row, Section, Title } from '@smui/top-app-bar';
    import IconButton from '@smui/icon-button';
    import Header from '@smui/common/Header.svelte';

    import { note } from '../stores/note';

    let titleEl;

    async function updateTitle(e) {
        note.update($note.uuid, { title: e.target.value });
    }

    $: {
        console.log(titleEl?.getElement()?.getElement());
    }
</script>

<TopAppBar variant="static" color="secondary">
    <Row>
        <Section>
            <IconButton class="material-icons" href="/notes/">menu</IconButton>
            <Title contenteditable bind:this={titleEl}>{$note?.title}</Title>
        </Section>
    </Row>
</TopAppBar>

<style>
</style>
