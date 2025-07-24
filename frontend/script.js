let user_id = "";

document.getElementById("loginForm").onsubmit = async function (e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const res = await fetch("/login", { method: "POST", body: formData });
    const data = await res.json();
    if (res.ok) {
        user_id = data.user_id;
        document.getElementById("chat").disabled = false;
    } else {
        alert("Erro no login");
    }
};

document.getElementById("messageInput").onkeydown = async function (e) {
    if (e.key === "Enter" && user_id) {
        const msg = e.target.value;
        e.target.value = "";
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: user_id, message: msg })
        });
        const data = await res.json();
        document.getElementById("chat").value += `\nVocê: ${msg}\nTars: ${data.response}`;
    }
};