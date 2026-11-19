/**
 * EduSmart AI - Client Interaction Utilities
 */

document.addEventListener("DOMContentLoaded", () => {
  // Initialize Bootstrap Tooltips if any exist
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.map((el) => new bootstrap.Tooltip(el));

  // Auto-dismiss standard alerts after 5 seconds
  const autoDismissAlerts = document.querySelectorAll(".alert-dismissible");
  autoDismissAlerts.forEach((alert) => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      try {
        bsAlert.close();
      } catch (e) {
        // Ignored if already closed
      }
    }, 5000);
  });
});
