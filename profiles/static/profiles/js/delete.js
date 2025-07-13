document.addEventListener("DOMContentLoaded", function () {
    const deleteButton = document.getElementById("delete-button");

    deleteButton.addEventListener("click", function () {
        const confirmation = confirm("Are you sure you want to delete your account? This action cannot be undone.");

        if (confirmation) {
            fetch("/profiles/delete/", {  // Obavezno provjeriti url 
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(), // Uzima CSRF token
                    "Content-Type": "application/json"
                }
            })
            .then(response => {
                if (response.ok) {
                    alert("Your account has been deleted.");
                    window.location.href = "/"; // Preusmeri na login stranicu
                } else {
                    alert("An error occurred. Try again.");
                }
            })
            .catch(error => console.error("Error:", error));
        }
    });

    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }
});

