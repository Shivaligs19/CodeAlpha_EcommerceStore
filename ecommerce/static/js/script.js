 function searchProducts() {
        let input = document.getElementById("searchInput")
            .value.toLowerCase().trim();

        let products = document.querySelectorAll(".product-card");

        products.forEach(function(product) {
            let name = product.querySelector("h3").innerText.toLowerCase();
            let description = product.querySelector(".description").innerText.toLowerCase();

            if (name.includes(input) || description.includes(input)) {
                product.style.display = "";
            } else {
                product.style.display = "none";
            }
        });
    }

    function filterCategory(category) {
        let products = document.querySelectorAll(".product-card");

        document.getElementById("searchInput").value = "";

        products.forEach(function(product) {
            let productCategory = product.dataset.category.trim().toLowerCase();

            if (category.toLowerCase() === "all" ||
                productCategory === category.toLowerCase()) {
                product.style.display = "";
            } else {
                product.style.display = "none";
            }
        });
    }