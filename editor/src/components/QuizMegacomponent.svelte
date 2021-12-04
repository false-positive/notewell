<script>
    import CircularProgress from '@smui/circular-progress';
    import Card from '@smui/card';
    import FormField from '@smui/form-field';
    import { onMount } from 'svelte';
    import Radio from '@smui/radio';
    import { note } from '../stores/note';

    let questionsQuery = null;
    let actives = [];

    async function loadQuestions() {
        const response = await fetch('/api/ai/questgen/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: $note.content,
                type: 'MCQ',
            }),
        });

        const questions = await response.json();
        actives = Array(questions.length).fill('');
        return questions;
    }

    onMount(() => {
        questionsQuery = loadQuestions();
    });
</script>

<div class="top-app-bar-container">
    <!-- Stuff -->
    <div class="asd">
        {#await questionsQuery}
            <div class="asd__sheet asd__sheet--white mdc-elevation--z9">
                <div class="loading_spinner_thing mdc-typography--body2">
                    <h4
                        class="mdc-typography--headline6"
                        style="margin-bottom: 0.2em;"
                    >
                        Generating quiz
                    </h4>
                    <p class="mdc-typograph--subtitle3">Querying Questgen...</p>
                    <div class="progress">
                        <CircularProgress
                            style="height: 32px; width: 32px;"
                            indeterminate
                        />
                    </div>
                </div>
            </div>
        {:then questions}
            <div class="asd__sheet mdc-typography--body2">
                {#if questions}
                    {#each questions as question, i}
                        {#if question.question.length}
                            <div class="question">
                                <Card padded>
                                    <h1
                                        class="mdc-typography--heading1"
                                        style="line-height: 1.5em"
                                    >
                                        {question.question}
                                    </h1>
                                    {#each question.options as option}
                                        <FormField>
                                            <Radio
                                                bind:group={actives[i]}
                                                value={option}
                                            />
                                            <span slot="label">{option}</span>
                                        </FormField>
                                    {/each}
                                </Card>
                            </div>
                        {/if}
                    {/each}
                {/if}
            </div>
        {/await}
    </div>
</div>

<style>
    :global(:root) {
        --mdc-theme-primary: #2b4854;
        --mdc-theme-secondary: #1baeea;
        --mdc-theme-background: #e6eff3;
        --mdc-theme-on-primary: #e6eff3;
        --mdc-theme-on-secondary: #39383b;
    }
    :global(body) {
        margin: 0;
        padding: 0;
        background: var(--mdc-theme-background);
    }
    .asd {
        background: #e6eff3;
        padding: 0.3em;
        overflow-x: wrap;
        overflow-y: scroll;
        /* height: 51.5em; */
        height: 52.7em;
    }

    .asd__sheet {
        width: 60em;
        /* min-height: 85em; */
        padding: 1em 3em;
        margin: 1.5em auto 1.5em auto;
        font-family: Roboto;
    }

    .asd__sheet--white {
        background: #fff;
    }

    .loading_spinner_thing {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .progress {
        display: flex;
        justify-content: center;
        padding: 1em;
    }

    .question {
        padding: 0 0 2em 0;
    }
</style>
