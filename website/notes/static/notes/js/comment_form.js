const commentField = new mdc.textField.MDCTextField(document.querySelector(".create-comment-form .mdc-text-field"));

document.querySelector('.search__button').addEventListener('click', () => {
    document.querySelector('.create-comment-form').submit();
});

const search = () => {
    document.querySelector('.create-comment-form').submit();
}