//Create function to select elements
const selectElement = (element) => document.querySelector(element);

//Open and close nav on click
// XXX: some browsers don't support `?.`
selectElement('.menu-icons')?.addEventListener('click', () => {
    selectElement('nav').classList.toggle('active');
});
