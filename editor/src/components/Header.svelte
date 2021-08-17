<script>
    export let title = '';
</script>

<header>
    <div class="container">
        <nav>
            <a href="/notes/">
                <!--
                    so the logo is taken from freepik and they
                    insist that I attribute them, but
                    this is a placehoder, sooo...
                -->
                <img src="/static/notes/img/logo.png" alt="Logo" class="logo" />
            </a>
            <p contenteditable={true}>{title}</p>
        </nav>
    </div>
</header>

<style>
    p {
        font-size: 2rem;
        padding-left: 0.4rem;
        font-weight: 300;
        color: #fff;
    }
</style>
