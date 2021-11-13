let hasFocused = false;

document.querySelectorAll(".input-field").forEach((e) => {
    const textField = new mdc.textField.MDCTextField(e.querySelector(".mdc-text-field"));
    const inputField = e.querySelector("input");
    const helperText = e.querySelector(".mdc-text-field-helper-text");

    let errorMessage = inputField.dataset.nwError;
    let hasError = false;

    if (errorMessage) {
        if (!hasFocused) {
            textField.focus();
            hasFocused = true;
        }

        hasError = true;
        textField.valid = false;
        textField.helperTextContent = errorMessage;
        helperText.classList.add("error");
    }

    inputField.onblur = () => {
        console.log("Yes");
        textField.valid ? helperText.classList.remove("error") : helperText.classList.add("error");

        if (hasError) {
            textField.valid = false;
        }
    };

    inputField.oninput = () => {
        if (errorMessage) {
            textField.valid = true;
            hasError = false;
        }
    };
});

const buttonRipple = new MDCRipple(document.querySelector(".mdc-button"));