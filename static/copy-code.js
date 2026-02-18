document.addEventListener("DOMContentLoaded", () => {
    const codeBlocks = document.querySelectorAll("pre > code");

    codeBlocks.forEach(code => {
        const pre = code.parentElement;

        // Wrapper für Positionierung
        const wrapper = document.createElement("div");
        wrapper.classList.add("code-block");
        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.appendChild(pre);

        // Button erstellen
        const button = document.createElement("button");
        button.classList.add("copy-button");
        button.innerHTML = `
            <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M16 1H4C2.9 1 2 1.9 2 3v14h2V3h12V1zm3 4H8C6.9 5 6 5.9 6 7v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
            </svg>
            <span>Copy</span>
        `;

        wrapper.appendChild(button);

        button.addEventListener("click", async () => {
            const text = code.innerText; // erhält Text MIT Zeilenumbrüchen
            try {
                await navigator.clipboard.writeText(text);
                const old = button.querySelector("span").textContent;
                button.querySelector("span").textContent = "Copied!";
                setTimeout(() => {
                    button.querySelector("span").textContent = old;
                }, 1500);
            } catch (err) {
                console.error("Copy failed", err);
            }
        });
    });
});