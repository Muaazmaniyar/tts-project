// Timer setup (60 minutes = 3600 seconds)
let timeLeft = 60 * 60;

function startTimer() {
  const timerDisplay = document.getElementById("timer");

  const timer = setInterval(() => {
    let minutes = Math.floor(timeLeft / 60);
    let seconds = timeLeft % 60;

    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    timerDisplay.innerText = `${minutes}:${seconds}`;

    if (timeLeft <= 60) {
      timerDisplay.classList.add("danger");
      timerDisplay.classList.remove("warning");
    } else if (timeLeft <= 600) {
      timerDisplay.classList.add("warning");
      timerDisplay.classList.remove("danger");
    } else {
      timerDisplay.classList.remove("warning", "danger");
    }

    if (timeLeft <= 0) {
      clearInterval(timer);
      if (confirm("⏰ Time is up!\nDo you want to submit your test now?")) {
        submitTest();
      } else {
        alert("⚠️ Test will be auto-submitted anyway.");
        submitTest();
      }
    }

    timeLeft--;
  }, 1000);
}

window.onload = () => {
  startTimer();
};
