<script>
    import FormField from '@smui/form-field';
    import Menu from '@smui/menu';
    import List, { Item } from '@smui/list';
    import Textfield from '@smui/textfield';
    import Icon from '@smui/textfield/icon';
    import { createEventDispatcher } from 'svelte';
    import { searchUsers } from '../api';

    const dispatch = createEventDispatcher();

    /**
     * @type {string[]}
     */
    export let ignoreUsernames = [];

    /**
     * @type {string}
     */
    let username = '';
    /**
     * @type {Promise<import('../api').User[]>}
     */
    let autocompleteUsers = null;
    let invalid = false;
    let autocompleteMenu;

    async function handleSubmit(username) {
        const users = autocompleteUsers ? await autocompleteUsers : [];
        const user = users.find((u) => u.username === username);
        invalid = false;
        if (user) {
            dispatch('submit', user);
            username = '';
            return;
        }
        if (users.length) {
            username = users[0].username;
            return;
        }
        invalid = true;
    }

    function autocomplete(user) {
        autocompleteUsers = null;
        dispatch('submit', user);
        username = '';
    }

    /**
     * @param {string} username
     * @returns {Promise<import('../api').User[]>}
     */
    async function performSearch(username) {
        username = username.trim();
        if (!username) {
            invalid = false;
            return [];
        }
        return (await searchUsers(username)).filter(
            (u) => !ignoreUsernames.includes(u.username)
        );
    }

    $: autocompleteUsers = performSearch(username);
</script>

<form on:submit|preventDefault={handleSubmit}>
    <FormField>
        <Textfield label="Share with user" bind:value={username} {invalid}>
            <Icon class="material-icons" slot="leadingIcon">person</Icon>
        </Textfield>
    </FormField>
</form>

{#if autocompleteUsers}
    {#await autocompleteUsers then users}
        {#if users.length}
            <Menu open bind:this={autocompleteMenu}>
                <List>
                    {#each users as user (user.username)}
                        <Item on:SMUI:action={() => autocomplete(user)}
                            >{user.username}</Item
                        >
                    {/each}
                </List>
            </Menu>
        {/if}
    {/await}
{/if}
