<script>
    export let severity = 'info';
</script>

<div class={severity} on:click><slot /></div>

<style>
    div {
        padding: 1em 2em;
        border-radius: 1em;
        font-size: 1.8em;
        max-width: 100%;
        font-weight: 400;
    }
    .info {
        background: rgb(55, 114, 241);
        color: #fff;
    }
    .success {
        background: rgb(52, 182, 52);
        color: #fff;
    }
    .warning {
        background: rgb(236, 236, 69);
    }
    .error {
        background: rgb(255, 49, 77);
        color: #fff;
    }
</style>
