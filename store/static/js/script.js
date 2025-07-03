
//update total price dynamic in cart with aantal changes
document.addEventListener('DOMContentLoaded', function () {
    const quantityInputs = document.querySelectorAll('.quantity-input');

    quantityInputs.forEach(input => {
        input.addEventListener('change', function () {
            const form = input.closest('form');
            if (form) {
                form.submit();
            }
        });
    });
});

function bevestigToevoegen() {
    const antwoord = confirm("Product toegevoegd aan je winkelwagen. Wil je naar je winkelwagen?");
    sessionStorage.setItem("goToCart",JSON.stringify(antwoord))
}