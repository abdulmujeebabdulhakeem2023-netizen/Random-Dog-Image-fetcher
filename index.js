let fetchBtn = document.getElementById("fetchBtn");
let loading = document.getElementById("loading");
let dogImage = document.getElementById("dogImage");
let breedSelect = document.getElementById("breedSelect");

fetchBtn.addEventListener("click", () => {
    let breed = breedSelect.value;
    let url = breed === "random" 
        ? "https://dog.ceo/api/breeds/image/random"
        : `https://dog.ceo/api/breed/${breed}/images/random`;

    loading.style.display = "block";
    dogImage.style.display = "none";

    fetch(url)
        .then(response => response.json())
        .then(data => {
            dogImage.src = data.message;
            loading.style.display = "none";
            dogImage.style.display = "block";
        })
        .catch(error => {
            console.error("Error:", error);
            loading.style.display = "none";
        });
});