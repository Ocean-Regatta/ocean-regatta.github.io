document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("studentSearch");
    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            const query = e.target.value.toLowerCase().trim();
            const rows = document.querySelectorAll("#leaderboardBody tr");

            rows.forEach((row) => {
                const handle = row.getAttribute("data-handle") || "";
                if (handle.toLowerCase().includes(query)) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }
            });
        });
    }

    let refreshInterval = 30;
    const refreshTimerEl = document.getElementById("refreshTimer");
    if (refreshTimerEl) {
        setInterval(() => {
            refreshInterval -= 1;
            if (refreshInterval <= 0) {
                window.location.reload();
            } else {
                refreshTimerEl.textContent = `${refreshInterval}s`;
            }
        }, 1000);
    }
});
