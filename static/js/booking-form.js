/**
 * NovaJet Private - Charter Booking Engine & Membership Form Submission
 * Handles AJAX requests, validation, dynamic CSRF token extraction, and luxury confirmation modals.
 */

document.addEventListener('DOMContentLoaded', () => {
  initBookingEngine();
  initMembershipForm();
  initEmptyLegQuickBook();
});

// Helper: Get CSRF Token from cookies or meta
function getCsrfToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (meta) return meta.getAttribute('content');

  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, 10) === 'csrftoken=') {
        cookieValue = decodeURIComponent(cookie.substring(10));
        break;
      }
    }
  }
  return cookieValue;
}

// 1. Charter Booking Engine
function initBookingEngine() {
  const form = document.getElementById('charterBookingForm');
  const tripTypeButtons = document.querySelectorAll('.trip-type-btn');
  const returnDateGroup = document.getElementById('returnDateGroup');
  const tripTypeInput = document.getElementById('tripTypeInput');

  // Trip Type Switching (One-Way, Round-Trip, Multi-City)
  tripTypeButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      tripTypeButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const tripType = btn.getAttribute('data-trip');
      if (tripTypeInput) tripTypeInput.value = tripType;

      if (returnDateGroup) {
        if (tripType === 'round_trip') {
          returnDateGroup.style.display = 'flex';
        } else {
          returnDateGroup.style.display = 'none';
        }
      }
    });
  });

  // Handle Form Submission
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const submitBtn = form.querySelector('button[type="submit"]');
      const originalBtnText = submitBtn.innerHTML;

      // Basic Client Validation
      const fullName = document.getElementById('clientFullName').value.trim();
      const email = document.getElementById('clientEmail').value.trim();
      const phone = document.getElementById('clientPhone').value.trim();
      const departure = document.getElementById('departureCity').value.trim();
      const arrival = document.getElementById('arrivalCity').value.trim();
      const departureDate = document.getElementById('departureDate').value.trim();

      if (!fullName || !email || !phone || !departure || !arrival || !departureDate) {
        window.showToast('Please complete all mandatory flight parameters.', 'error');
        return;
      }

      // Prepare payload
      const payload = {
        trip_type: tripTypeInput ? tripTypeInput.value : 'one_way',
        departure_city: departure,
        arrival_city: arrival,
        departure_date: departureDate,
        departure_time: document.getElementById('departureTime') ? document.getElementById('departureTime').value : 'Flexible',
        return_date: document.getElementById('returnDate') ? document.getElementById('returnDate').value : '',
        passenger_count: document.getElementById('passengerCount') ? document.getElementById('passengerCount').value : 4,
        preferred_category: document.getElementById('preferredAircraft') ? document.getElementById('preferredAircraft').value : 'Ultra Long Range',
        full_name: fullName,
        email: email,
        phone: phone,
        catering_preferences: document.getElementById('cateringPreferences') ? document.getElementById('cateringPreferences').value : '',
        special_requests: document.getElementById('specialRequests') ? document.getElementById('specialRequests').value : '',
      };

      try {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
          <svg class="animate-spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="12"></circle>
          </svg>
          <span>Securing Flight Clearance...</span>
        `;

        const response = await fetch('/api/charter/submit/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
          },
          body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok && result.success) {
          // Show Success Modal
          displayBookingConfirmation(result);
          form.reset();
          window.showToast(`Flight dossier ${result.reference_code} generated successfully!`, 'success');
        } else {
          window.showToast(result.error || 'Unable to submit charter brief. Please check details.', 'error');
        }
      } catch (err) {
        console.error(err);
        window.showToast('Network error connecting to flight operations server.', 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
      }
    });
  }
}

// 2. Display Confirmation Reference Modal
function displayBookingConfirmation(data) {
  const modal = document.getElementById('charterSuccessModal');
  if (!modal) return;

  const codeEl = document.getElementById('confirmedRefCode');
  const routeEl = document.getElementById('confirmedRoute');
  const nameEl = document.getElementById('confirmedName');
  const dateEl = document.getElementById('confirmedDate');

  if (codeEl) codeEl.innerText = data.reference_code;
  if (routeEl) routeEl.innerText = data.route;
  if (nameEl) nameEl.innerText = data.client_name;
  if (dateEl) dateEl.innerText = data.date;

  modal.classList.add('active');
  document.body.style.overflow = 'hidden';
}

// 3. Membership Inquiry Form Submission
function initMembershipForm() {
  const memberForm = document.getElementById('membershipInquiryForm');
  if (!memberForm) return;

  memberForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitBtn = memberForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;

    const payload = {
      full_name: document.getElementById('memberFullName').value.trim(),
      email: document.getElementById('memberEmail').value.trim(),
      phone: document.getElementById('memberPhone').value.trim(),
      company: document.getElementById('memberCompany') ? document.getElementById('memberCompany').value.trim() : '',
      preferred_tier: document.getElementById('modalMembershipTier') ? document.getElementById('modalMembershipTier').value : 'Prestige Tier',
      annual_flight_hours: document.getElementById('memberHours') ? document.getElementById('memberHours').value : '50-100 Hours',
      notes: document.getElementById('memberNotes') ? document.getElementById('memberNotes').value.trim() : '',
    };

    try {
      submitBtn.disabled = true;
      submitBtn.innerHTML = 'Submitting Dossier...';

      const response = await fetch('/api/membership/submit/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(payload)
      });

      const result = await response.json();
      if (response.ok && result.success) {
        // Close modal
        const modal = document.getElementById('membershipModal');
        if (modal) modal.classList.remove('active');
        document.body.style.overflow = '';
        memberForm.reset();
        window.showToast(result.message, 'success');
      } else {
        window.showToast(result.error || 'Submission failed.', 'error');
      }
    } catch (err) {
      console.error(err);
      window.showToast('Network error submitting membership inquiry.', 'error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalText;
    }
  });
}

// 4. Empty Leg Quick Book Integration
function initEmptyLegQuickBook() {
  document.querySelectorAll('.book-empty-leg-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const origin = btn.getAttribute('data-origin');
      const destination = btn.getAttribute('data-destination');
      const aircraft = btn.getAttribute('data-aircraft');

      // Scroll to booking form and prefill
      const departureInput = document.getElementById('departureCity');
      const arrivalInput = document.getElementById('arrivalCity');
      const preferredAircraft = document.getElementById('preferredAircraft');

      if (departureInput) departureInput.value = origin;
      if (arrivalInput) arrivalInput.value = destination;
      if (preferredAircraft) preferredAircraft.value = aircraft;

      const bookingSection = document.getElementById('charter-request');
      if (bookingSection) {
        bookingSection.scrollIntoView({ behavior: 'smooth' });
        window.showToast(`Selected Empty Leg: ${origin} ➔ ${destination}`, 'info');
      }
    });
  });
}
