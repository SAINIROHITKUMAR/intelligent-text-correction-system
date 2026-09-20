const input = document.getElementById("textInput");
const count = document.getElementById("count");
const button = document.getElementById("correctBtn");
const resultCard = document.getElementById("resultCard");
const correctedText = document.getElementById("correctedText");
const changes = document.getElementById("changes");
const changeCount = document.getElementById("changeCount");

input.addEventListener("input", () => {
  count.textContent = `${input.value.length} / 5000`;
});

button.addEventListener("click", async () => {
  const text = input.value.trim();

  if (!text) {
    alert("Please enter some text.");
    return;
  }

  button.disabled = true;
  button.textContent = "Correcting...";

  try {
    const response = await fetch("/api/correct", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Unable to correct text.");
    }

    correctedText.textContent = data.corrected_text;
    changeCount.textContent = `${data.change_count} change${data.change_count === 1 ? "" : "s"}`;
    changes.innerHTML = "";

    if (!data.changes.length) {
      changes.innerHTML = "<li>No spelling or grammar changes detected.</li>";
    } else {
      data.changes.forEach(change => {
        const li = document.createElement("li");
        li.textContent = `${change.original} → ${change.corrected}`;
        changes.appendChild(li);
      });
    }

    resultCard.classList.remove("hidden");
  } catch (error) {
    alert(error.message);
  } finally {
    button.disabled = false;
    button.textContent = "Correct Text";
  }
});
