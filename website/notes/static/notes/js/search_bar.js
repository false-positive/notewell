const searchField = new mdc.textField.MDCTextField(document.querySelector(".search-form .mdc-text-field"));

document.querySelector('.search__button').addEventListener('click', () => {
    document.querySelector('.search-form').submit();
});

const search = () => {
    document.querySelector('.search-form').submit();
}