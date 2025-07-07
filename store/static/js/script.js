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


function toggleSide_bar() {
    const side_bar = document.getElementById('side_bar');

    if (side_bar.style.display === 'none') {
        side_bar.style.display = 'flex';
    } else {
        side_bar.style.display = 'none';
    }
}


//zoekveld logisch
async function zoek() {
    const zoekveld = document.getElementById("zoekveld");
    const resultaten = document.getElementById("resultaten");

    const query = zoekveld.value.trim();

    if (query === "") {
        resultaten.innerHTML = "";
        resultaten.classList.add("hidden");
        return;
    }

    try {
        const response = await fetch(`/api/zoeken/?q=${encodeURIComponent(query)}`);
        const data = await response.json();

        resultaten.innerHTML = "";

        if (data.length === 0) {
            const li = document.createElement("li");
            li.textContent = "Geen resultaten";
            resultaten.appendChild(li);
        } else {
            data.forEach(product => {
                const a = document.createElement("a");
                const li = document.createElement("li");
                li.textContent = `${product.name} – €${product.price}`;
                a.href = `/products/${product.id}`;
                li.classList.add("list_item");
                a.appendChild(li);
                resultaten.appendChild(a);
            });
        }

        resultaten.classList.remove("hidden");
        resultaten.classList.add("store_list");
    } catch (error) {
        console.error("Fout tijdens zoeken:", error);
    }

    // Verberg resultatenlijst als gebruiker ergens anders klikt
    document.addEventListener("click", (e) => {
        if (!zoekveld.contains(e.target) && !resultaten.contains(e.target)) {
            resultaten.classList.add("hidden");
        }
    });

}