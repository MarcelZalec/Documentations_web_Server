function changeSource() {
    const key = document.getElementById("folderSelect").value;

    fetch("/change_base", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ key })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            console.log("Fehler: " + data.error);
        } else {
            console.log("Ordner gewechselt zu:\n" + data.new_base);
            location.href = "/"; // zurück zur Root
        }
    });
}
