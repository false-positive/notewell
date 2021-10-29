<script>
    import Button, { Icon, Label } from '@smui/button';
    import Dialog, { Actions, Content, Title } from '@smui/dialog';
    import LinearProgress from '@smui/linear-progress';
    import Menu from '@smui/menu';
    import List, { Item, Text, Graphic, Meta } from '@smui/list';
    import PermissionForm from '../PermissionForm.svelte';
    import Separator from '@smui/list/Separator.svelte';
    import { getNotePermissions, updateNotePermissions } from '../../api';
    import { note } from '../../stores/note';

    export let open = true;

    /**
     * @type {import('../../api').Permission[]}
     */
    let permissions = [];
    let isDirty = false;
    let isLoading = true;
    let menus = [];

    async function loadPermissions() {
        isLoading = true;
        permissions = await getNotePermissions($note.uuid);
        isLoading = false;
        isDirty = false;
    }

    /**
     * @param {string} user
     */
    function handleRemove(user) {
        permissions = permissions.filter((p) => p.user !== user);
        isDirty = true;
    }

    /**
     * @param {number} idx
     * @param {('R'|'W')} permLevel
     */
    function handlePermLevelChange(idx, permLevel) {
        permissions[idx].perm_level = permLevel;
        isDirty = true;
    }

    async function save() {
        isLoading = true;
        await updateNotePermissions($note.uuid, permissions);
        isLoading = false;
        isDirty = false;
    }

    $: {
        if (open) {
            loadPermissions();
        }
    }
</script>

<!-- TODO: add aria's -->
<Dialog bind:open>
    <Title>Share</Title>
    <Content>
        <LinearProgress indeterminate closed={!isLoading} />
        {#each permissions as permission, i (permission.user)}
            <Menu bind:this={menus[i]}>
                <List>
                    <Item on:SMUI:action={() => handlePermLevelChange(i, 'R')}>
                        <Graphic class="material-icons">visibility</Graphic>
                        <Text>Viewer</Text>
                    </Item>
                    <Item on:SMUI:action={() => handlePermLevelChange(i, 'W')}>
                        <Graphic class="material-icons">edit</Graphic>
                        <Text>Editor</Text>
                    </Item>

                    <Separator />

                    <Item on:SMUI:action={() => handleRemove(permission.user)}>
                        <Graphic class="material-icons">delete</Graphic>
                        <Text>Remove</Text>
                    </Item>
                </List>
            </Menu>
        {/each}
        <PermissionForm />
        <List>
            <Item>
                <Text>{$note.author}</Text>
                <Meta>Author</Meta>
            </Item>
            {#each permissions as permission, i (permission.user)}
                <Item>
                    <Text>
                        {permission.user}
                    </Text>
                    <Meta>
                        <Button
                            on:click={menus[i].setOpen(true)}
                            disabled={isLoading}
                        >
                            <Label>
                                {#if permission.perm_level === 'R'}
                                    Viewer
                                {:else if permission.perm_level === 'W'}
                                    Editor
                                {/if}
                            </Label>
                            <Icon class="material-icons">expand_more</Icon>
                        </Button>
                    </Meta>
                </Item>
            {/each}
        </List>
    </Content>
    <Actions>
        {#if isDirty}
            <span class="mdc-typography--overline">Unsaved changes</span>
        {/if}
        <Button variant="unelevated" on:click={save} disabled={isLoading}>
            Done
        </Button>
    </Actions>
</Dialog>
