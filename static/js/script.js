
// TAKEN FROM BOOTSTRAP: https://getbootstrap.com/docs/5.1/forms/validation/#how-it-works
// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict';
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation');
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }

                form.classList.add('was-validated');
            }, false);
        });
})();

//  CUSTOM CODE:
// for cost rating slider
function highlightIcon(num, iconType, limit) {
    for (let i = 1; i <= limit; i++) {
        let icon = document.querySelector(`#${iconType}-${i}`);
        let iconClasses = icon.classList;
        if (i <= num) {
            if (iconClasses.contains(`unfilled-${iconType}`)) {
                icon.classList.remove(`unfilled-${iconType}`);
            }
            icon.classList.add(`filled-${iconType}`);
        } else {
            if (iconClasses.contains(`filled-${iconType}`)) {
                icon.classList.remove(`filled-${iconType}`);
            }
            icon.classList.add(`unfilled-${iconType}`);
        }
    }
}

// for delete button modal
function passIdToModal(obj, actions) {
    let reviewId = obj.getAttribute('data-review-id');
    for (let i = 0; i <= actions.length; i++) {
        console.log(i);
        // find the modal on the page
        let modalButton = document.querySelector(`#${actions[i]}ModalButton`);
        // set its href to pass the review id to backend for the particular action needed
        modalButton.setAttribute('href', `/${actions[i]}_review/${reviewId}`);
    }
}