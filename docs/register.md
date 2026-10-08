# Competitor Registration

Welcome to the **Ocean Regatta Competitor Registration Portal** 🚤

---

## 📋 Registration Procedure & Policies

To ensure fair competition, conserve dedicated simulation server resources, and prevent spam, Ocean Regatta operates a participant verification registry on the competition template repository ([Ocean-Regatta/ocean-regatta-2026-template](https://github.com/Ocean-Regatta/ocean-regatta-2026-template)).

!!! important "Registration Required for Automated PR Grading"
    Automated evaluation runs **only** for competitors registered in `participants.json` approved by the organizer (**@Teusner**). Pull Requests opened by unverified accounts will not trigger simulation server jobs or post scores to the leaderboard.

### ⏱️ Key Guidelines

* **24-Hour Review SLA:** Approvals are handled personally by the regatta committee (**@Teusner**) within **24 hours**. Once your registration issue is reviewed and your username is merged into `participants.json`, your automated PR grading pipeline activates immediately.
* **60-Minute Cooldown Policy:** Submissions adhere to a strict **60-minute cooldown** between runs to prevent seed overfitting against randomized ocean currents, wave disturbances, and thruster degradation. Teams are encouraged to test and tune their controllers locally via Docker before submitting official runs.
* **Open & Free:** Any student, academic researcher, or robotics enthusiast is welcome to participate!

---

## 🧭 Step-by-Step Registration Flow

Follow these four steps to register and begin competing:

```mermaid
flowchart LR
    A["1. Fill Form"] --> B["2. Submit GitHub Issue"]
    B --> C["3. Committee Review"]
    C --> D["4. Start Competing"]
```

<div class="registration-steps-indicator">
  <div class="reg-step-card">
    <div class="reg-step-num">1</div>
    <div class="reg-step-content">
      <strong>1. Fill Form</strong>
      <span>Enter your GitHub handle and team information below.</span>
    </div>
  </div>
  <div class="reg-step-card">
    <div class="reg-step-num">2</div>
    <div class="reg-step-content">
      <strong>2. Submit GitHub Issue</strong>
      <span>Review prefilled registration form and submit on GitHub.</span>
    </div>
  </div>
  <div class="reg-step-card">
    <div class="reg-step-num">3</div>
    <div class="reg-step-content">
      <strong>3. Committee Review</strong>
      <span>Reviewed & merged into participants.json by @Teusner (≤ 24h).</span>
    </div>
  </div>
  <div class="reg-step-card">
    <div class="reg-step-num">4</div>
    <div class="reg-step-content">
      <strong>4. Start Competing</strong>
      <span>Open Pull Requests to trigger Gazebo evaluation & rankings!</span>
    </div>
  </div>
</div>

---

## ✍️ Registration Form

<noscript>
  <div class="admonition warning" style="margin-bottom: 1.5rem;">
    <p class="admonition-title">JavaScript Disabled</p>
    <p>JavaScript is disabled in your browser. You can still register directly by manually opening the <a href="https://github.com/Ocean-Regatta/ocean-regatta-2026-template/issues/new?template=registration_request.yml" target="_blank" rel="noopener noreferrer"><strong>GitHub Issue Registration Template ↗</strong></a> and filling out your team details.</p>
  </div>
</noscript>

<div class="registration-card" id="registration-portal">
  <h3>
    <span>🚤</span>
    <span>Competitor Registration Request</span>
  </h3>
  <p class="subtitle">Complete the fields below to generate and submit your official registration request on GitHub.</p>

  <form id="reg-form" novalidate onsubmit="return handleRegistrationSubmit(event)">
    <!-- GitHub Username -->
    <div class="reg-form-group">
      <label class="reg-label" for="reg-github-username">
        GitHub Username <span class="required-star">*</span>
      </label>
      <input
        type="text"
        id="reg-github-username"
        name="github_username"
        class="reg-input"
        placeholder="e.g. octocat (or @octocat)"
        autocomplete="username"
        spellcheck="false"
        required
      />
      <div class="reg-help">Your GitHub handle used to author commits and Pull Requests.</div>
      <div id="err-github-username" class="reg-error-msg">Please enter a valid GitHub username (alphanumeric and single hyphens, 1–39 characters).</div>
    </div>

    <!-- Team / Competitor Display Name -->
    <div class="reg-form-group">
      <label class="reg-label" for="reg-team-name">
        Team / Competitor Display Name <span class="required-star">*</span>
      </label>
      <input
        type="text"
        id="reg-team-name"
        name="team_name"
        class="reg-input"
        placeholder="e.g. Team Nautilus"
        required
      />
      <div class="reg-help">How your team will appear on the Live Scoreboard.</div>
      <div id="err-team-name" class="reg-error-msg">Please enter your team or competitor display name.</div>
    </div>

    <!-- Affiliation / Institution -->
    <div class="reg-form-group">
      <label class="reg-label" for="reg-affiliation">
        Affiliation / Institution <span style="font-weight: normal; font-size: 0.8rem; color: var(--md-default-fg-color--light);">(optional)</span>
      </label>
      <input
        type="text"
        id="reg-affiliation"
        name="affiliation"
        class="reg-input"
        placeholder="e.g. Stanford University / Acme Robotics / Independent"
      />
      <div class="reg-help">University, company, research lab, or independent competitor.</div>
    </div>

    <!-- Brief Strategy / Background -->
    <div class="reg-form-group">
      <label class="reg-label" for="reg-strategy">
        Brief Strategy / Background <span style="font-weight: normal; font-size: 0.8rem; color: var(--md-default-fg-color--light);">(optional)</span>
      </label>
      <textarea
        id="reg-strategy"
        name="strategy"
        class="reg-textarea"
        placeholder="e.g. Implementing adaptive MPC with Ping2 sonar wall following and Kalman filter sensor fusion."
        rows="3"
      ></textarea>
      <div class="reg-help">Optional notes about your planned control architecture or robotics background.</div>
    </div>

    <!-- Agreement Checkbox -->
    <div class="reg-checkbox-group">
      <label class="reg-checkbox-label" for="reg-agreement">
        <input
          type="checkbox"
          id="reg-agreement"
          name="agreement"
          required
        />
        <span>I agree to the Ocean Regatta rules and cooldown policy</span>
      </label>
      <div id="err-agreement" class="reg-error-msg" style="margin-left: 1.7rem;">You must agree to the Ocean Regatta rules and cooldown policy to register.</div>
    </div>

    <!-- Submit Button -->
    <button type="submit" id="reg-submit-btn" class="reg-btn-submit">
      <svg viewBox="0 0 16 16" aria-hidden="true">
        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
      </svg>
      <span>Submit Registration via GitHub</span>
    </button>

    <!-- Success Feedback Box -->
    <div id="reg-feedback" class="reg-feedback-box">
      <strong>🚀 Opening GitHub Issue in a new tab...</strong>
      <div style="margin-top: 0.35rem; font-size: 0.84rem;">
        If your browser blocked the popup window, <a id="reg-fallback-anchor" href="#" target="_blank" rel="noopener noreferrer">click here to open your prefilled GitHub Issue Form</a>.
      </div>
    </div>
  </form>

  <!-- Fallback footer link -->
  <div class="reg-fallback-footer">
    Prefer manual submission without auto-fill?
    <a href="https://github.com/Ocean-Regatta/ocean-regatta-2026-template/issues/new?template=registration_request.yml" target="_blank" rel="noopener noreferrer">
      Open the blank GitHub Issue Template &rarr;
    </a>
  </div>
</div>

<script>
// GitHub username validation: alphanumeric + single hyphens, 1-39 chars, no start/end hyphen
const GITHUB_USERNAME_REGEX = /^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$/;

function cleanUsernameValue(val) {
  if (!val) return "";
  return val.replace(/^@+/, "").trim();
}

function validateGithubUsername(val) {
  const cleaned = cleanUsernameValue(val);
  return GITHUB_USERNAME_REGEX.test(cleaned);
}

function handleRegistrationSubmit(e) {
  if (e && e.preventDefault) {
    e.preventDefault();
  }

  const usernameInput = document.getElementById("reg-github-username");
  const teamNameInput = document.getElementById("reg-team-name");
  const affiliationInput = document.getElementById("reg-affiliation");
  const strategyInput = document.getElementById("reg-strategy");
  const agreementInput = document.getElementById("reg-agreement");

  const errUsername = document.getElementById("err-github-username");
  const errTeamName = document.getElementById("err-team-name");
  const errAgreement = document.getElementById("err-agreement");
  const feedbackBox = document.getElementById("reg-feedback");
  const fallbackAnchor = document.getElementById("reg-fallback-anchor");

  let isValid = true;
  let firstInvalid = null;

  // 1. Validate GitHub Username
  const rawUsername = usernameInput.value.trim();
  const cleanUsername = cleanUsernameValue(rawUsername);
  if (!cleanUsername || !validateGithubUsername(cleanUsername)) {
    usernameInput.classList.add("is-invalid");
    errUsername.classList.add("visible");
    isValid = false;
    if (!firstInvalid) firstInvalid = usernameInput;
  } else {
    usernameInput.classList.remove("is-invalid");
    errUsername.classList.remove("visible");
    // Normalize input field to cleaned handle without leading @
    usernameInput.value = cleanUsername;
  }

  // 2. Validate Team Name
  const teamName = teamNameInput.value.trim();
  if (!teamName) {
    teamNameInput.classList.add("is-invalid");
    errTeamName.classList.add("visible");
    isValid = false;
    if (!firstInvalid) firstInvalid = teamNameInput;
  } else {
    teamNameInput.classList.remove("is-invalid");
    errTeamName.classList.remove("visible");
  }

  // 3. Validate Agreement Checkbox
  if (!agreementInput.checked) {
    errAgreement.classList.add("visible");
    isValid = false;
    if (!firstInvalid) firstInvalid = agreementInput;
  } else {
    errAgreement.classList.remove("visible");
  }

  if (!isValid) {
    if (firstInvalid && firstInvalid.focus) {
      firstInvalid.focus();
    }
    return false;
  }

  // 4. Assemble the GitHub Issue Form URL
  const username = cleanUsername;
  const affiliation = affiliationInput.value ? affiliationInput.value.trim() : "";

  const issueUrl = `https://github.com/Ocean-Regatta/ocean-regatta-2026-template/issues/new?template=registration_request.yml&title=%5BRegistration%5D%3A+%40${username}&github_username=${username}&team_name=${encodeURIComponent(teamName)}&affiliation=${encodeURIComponent(affiliation)}`;

  // Show dynamic feedback & update fallback anchor
  fallbackAnchor.href = issueUrl;
  feedbackBox.classList.add("visible");

  // Open the prefilled GitHub Issue Form in a new tab
  window.open(issueUrl, "_blank", "noopener,noreferrer");

  return false;
}

// Attach real-time input validation cleanups
document.addEventListener("DOMContentLoaded", function() {
  const usernameInput = document.getElementById("reg-github-username");
  const teamNameInput = document.getElementById("reg-team-name");
  const agreementInput = document.getElementById("reg-agreement");

  if (usernameInput) {
    usernameInput.addEventListener("input", function() {
      const clean = cleanUsernameValue(this.value);
      if (clean && validateGithubUsername(clean)) {
        this.classList.remove("is-invalid");
        const err = document.getElementById("err-github-username");
        if (err) err.classList.remove("visible");
      }
    });
  }

  if (teamNameInput) {
    teamNameInput.addEventListener("input", function() {
      if (this.value.trim()) {
        this.classList.remove("is-invalid");
        const err = document.getElementById("err-team-name");
        if (err) err.classList.remove("visible");
      }
    });
  }

  if (agreementInput) {
    agreementInput.addEventListener("change", function() {
      if (this.checked) {
        const err = document.getElementById("err-agreement");
        if (err) err.classList.remove("visible");
      }
    });
  }
});
</script>
