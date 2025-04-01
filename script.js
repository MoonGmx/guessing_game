document.addEventListener("DOMContentLoaded", function () {
    const deleteBtns = document.querySelectorAll(".delete-btn");
    const searchInput = document.getElementById("search");
    const contactList = document.getElementById("contact-list");

    deleteBtns.forEach((btn) => {
        btn.addEventListener("click", function (event) {
            if (!confirm("Are you sure you want to delete this contact?")) {
                event.preventDefault();
            }
        });
    });

    searchInput.addEventListener("input", function () {
        const query = this.value.toLowerCase();
        fetch(`/search?q=${query}`)
            .then(response => response.json())
            .then(data => {
                contactList.innerHTML = "";
                data.forEach(contact => {
                    contactList.innerHTML += `
                        <li>
                            <strong>${contact.name}</strong> - ${contact.phone} - ${contact.email}
                            <a href="/delete/${contact.id}" class="delete-btn">❌</a>
                            <button class="share-btn" onclick="shareContact('${contact.name}', '${contact.phone}', '${contact.email}')">📤 Share</button>
                        </li>`;
                });
            });
    });
});

function shareContact(name, phone, email) {
    const text = `Contact: ${name}\nPhone: ${phone}\nEmail: ${email}`;
    if (navigator.share) {
        navigator.share({ title: "Contact Details", text });
    } else {
        alert("Sharing not supported on this browser.");
    }
}
