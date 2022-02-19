// HACK: clean the contents of #app
document.getElementById('app').innerHTML = '';

const initialDataEl = document.getElementById('nw-editor-initial-data');
const initialData = JSON.parse(initialDataEl.innerHTML);
initialDataEl.outerHTML = '';

document.getElementById('app').innerHTML = `<pre>${JSON.stringify(
    initialData,
    null,
    4
)}</pre>`;
