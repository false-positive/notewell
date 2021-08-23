<script>
    import { note } from '../stores/note';

    async function updateTitle(e) {
        note.update($note.uuid, { title: e.target.value });
    }
</script>

<header class="header">
    <div class="header__container">
        <nav class="nav">
            <a class="nav__link" href="/notes/">
                <!--
                    so the logo is taken from freepik and they
                    insist that I attribute them, but
                    this is a placehoder, sooo...
                -->
                <img src="/static/notes/img/logo.png" alt="Logo" class="logo" />
            </a>
            <input value={$note?.title} on:change={updateTitle} />
            <p>{$note?.title}</p>
        </nav>
    </div>
</header>

<style>
    input {
        background: none;
        border: none;
        font-size: 2rem;
        padding-left: 0.4rem;
        font-weight: 300;
        color: #fff;
    }
</style>
