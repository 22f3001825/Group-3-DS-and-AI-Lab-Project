/* ══════════════════════════════════════════════════════════════════════
   DS-AI Platform — Main JavaScript
   ══════════════════════════════════════════════════════════════════════ */

// ── SIDEBAR TOGGLE ─────────────────────────────────────────────────────
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar       = document.getElementById('sidebar');

if (sidebarToggle && sidebar) {
  sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });

  // Close sidebar when clicking outside on mobile
  document.addEventListener('click', (e) => {
    if (window.innerWidth < 992 &&
        !sidebar.contains(e.target) &&
        !sidebarToggle.contains(e.target)) {
      sidebar.classList.remove('open');
    }
  });
}

// ── AUTO-DISMISS ALERTS ────────────────────────────────────────────────
document.querySelectorAll('.alert').forEach(alert => {
  setTimeout(() => {
    const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
    if (bsAlert) bsAlert.close();
  }, 5000);
});

// ── ACTIVE NAV HIGHLIGHTING ────────────────────────────────────────────
// Already done via Jinja2 in base.html, but ensure smooth transitions
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', function() {
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    this.classList.add('active');
  });
});

// ── AI BACKEND LABEL ───────────────────────────────────────────────────
// Fetch config backend label to display in sidebar
(function() {
  const label = document.getElementById('backendLabel');
  if (!label) return;
  // Read from meta tag or cookie if set
  const backends = { gemini: 'Gemini AI', claude: 'Claude AI', ollama: 'Ollama (Local)' };
  // Default display (actual value from server could be injected via template)
  label.textContent = 'AI Backend Active';
})();

// ── TOOLTIP INIT ───────────────────────────────────────────────────────
document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
  new bootstrap.Tooltip(el);
});

// ── SMOOTH SCROLL FOR TOC ──────────────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ── COPY TEXT UTILITY ──────────────────────────────────────────────────
function copyToClipboard(text, btnEl) {
  navigator.clipboard.writeText(text).then(() => {
    const orig = btnEl.innerHTML;
    btnEl.innerHTML = '<i class="bi bi-check2"></i> Copied!';
    setTimeout(() => { btnEl.innerHTML = orig; }, 2000);
  });
}

// ── FORM ENHANCEMENT: Add loading state ────────────────────────────────
document.querySelectorAll('form[data-loading]').forEach(form => {
  form.addEventListener('submit', function() {
    const btn = this.querySelector('[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>Loading…`;
    }
  });
});
