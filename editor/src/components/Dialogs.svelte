<script>
    import ShareDialog from './dialogs/ShareDialog.svelte';
    import { isShareDialogOpen } from '../stores/isShareDialogOpen';
</script>

<ShareDialog bind:open={$isShareDialogOpen} />
