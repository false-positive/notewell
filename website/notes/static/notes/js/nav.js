//Create function to select elements
const selectElement = (element) => document.querySelector(element);

//Open and close nav on click
<<<<<<< HEAD
// XXX: some browsers don't support `?.`
selectElement('.menu-icons')?.addEventListener('click', () => {
    selectElement('nav').classList.toggle('active');
=======
selectElement('.nav__hamburger').addEventListener('click', () => {
    selectElement('.nav').classList.toggle('active');
>>>>>>> development
});
