/**
 * NovaJet Private - Interactive Route & Flight Estimator Engine
 * Real-time Great Circle calculation, flight time estimate, and jet recommendations
 */

document.addEventListener('DOMContentLoaded', () => {
  initRouteCalculator();
});

function initRouteCalculator() {
  const originSelect = document.getElementById('calcOrigin');
  const destSelect = document.getElementById('calcDestination');
  const calculateBtn = document.getElementById('calcSubmitBtn');

  if (!originSelect || !destSelect || !calculateBtn) return;

  async function updateFlightEstimate() {
    const origin = originSelect.value;
    const dest = destSelect.value;

    if (origin === dest) {
      window.showToast('Please select two distinct global hubs for calculation.', 'error');
      return;
    }

    calculateBtn.innerHTML = 'Calculating Vector...';
    calculateBtn.disabled = true;

    try {
      const res = await fetch(`/api/route-calculator/?origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(dest)}`);
      const data = await res.json();

      // Update UI displays
      const distEl = document.getElementById('calcResultDistance');
      const timeEl = document.getElementById('calcResultTime');
      const jetEl = document.getElementById('calcResultJet');
      const altEl = document.getElementById('calcResultAltitude');

      if (distEl) distEl.innerText = `${data.distance_nm.toLocaleString()} NM (${data.distance_km.toLocaleString()} KM)`;
      if (timeEl) timeEl.innerText = data.flight_time;
      if (jetEl) jetEl.innerText = data.recommended_jet;
      if (altEl) altEl.innerText = data.cruise_alt;

    } catch (err) {
      console.error(err);
      window.showToast('Calculation error. Please try again.', 'error');
    } finally {
      calculateBtn.innerHTML = 'Estimate Flight Vector';
      calculateBtn.disabled = false;
    }
  }

  calculateBtn.addEventListener('click', (e) => {
    e.preventDefault();
    updateFlightEstimate();
  });

  // Also calculate on change
  originSelect.addEventListener('change', () => {
    if (originSelect.value !== destSelect.value) updateFlightEstimate();
  });
  destSelect.addEventListener('change', () => {
    if (originSelect.value !== destSelect.value) updateFlightEstimate();
  });
}
