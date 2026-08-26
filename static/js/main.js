/**
 * NovaJet Private - Core JavaScript Engine (Upgraded)
 * "The Sky, Redefined."
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavbarScroll();
  initMobileDrawer();
  initAmbientSound();
  initCabinTabs();
  initFleetFiltering();
  init3DCardTilt();
  initAuthModals();
  initModals();
  initScrollNav();
});

// 1. Sticky Navbar on Scroll
function initNavbarScroll() {
  const navbar = document.querySelector('.navbar-wrapper');
  if (!navbar) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 30) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });
}

// 2. Mobile Drawer Navigation
function initMobileDrawer() {
  const toggleBtn = document.querySelector('.mobile-toggle');
  const closeBtn = document.querySelector('.drawer-close');
  const drawer = document.querySelector('.mobile-drawer');
  const overlay = document.querySelector('.drawer-overlay');
  const drawerLinks = document.querySelectorAll('.drawer-menu a');

  function openDrawer() {
    drawer.classList.add('open');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeDrawer() {
    drawer.classList.remove('open');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (toggleBtn) toggleBtn.addEventListener('click', openDrawer);
  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  if (overlay) overlay.addEventListener('click', closeDrawer);

  drawerLinks.forEach(link => {
    link.addEventListener('click', closeDrawer);
  });
}

// 3. Ambient Luxury Cabin Hum (Web Audio API Synthesizer)
let audioCtx = null;
let humGain = null;
let isSoundActive = false;

function initAmbientSound() {
  const toggleBtn = document.getElementById('ambientSoundToggle');
  if (!toggleBtn) return;

  toggleBtn.addEventListener('click', () => {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AudioContext();

      const osc1 = audioCtx.createOscillator();
      const osc2 = audioCtx.createOscillator();
      const filter = audioCtx.createBiquadFilter();
      humGain = audioCtx.createGain();

      osc1.type = 'sine';
      osc1.frequency.setValueAtTime(88, audioCtx.currentTime);
      osc2.type = 'triangle';
      osc2.frequency.setValueAtTime(132, audioCtx.currentTime);

      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(220, audioCtx.currentTime);

      humGain.gain.setValueAtTime(0.0001, audioCtx.currentTime);

      osc1.connect(filter);
      osc2.connect(filter);
      filter.connect(humGain);
      humGain.connect(audioCtx.destination);

      osc1.start();
      osc2.start();
    }

    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }

    isSoundActive = !isSoundActive;

    if (isSoundActive) {
      humGain.gain.setTargetAtTime(0.045, audioCtx.currentTime, 0.5);
      toggleBtn.classList.add('active');
      showToast('Ambient Cabin Atmosphere: Active', 'success');
    } else {
      humGain.gain.setTargetAtTime(0.0001, audioCtx.currentTime, 0.3);
      toggleBtn.classList.remove('active');
      showToast('Ambient Cabin Atmosphere: Muted', 'info');
    }
  });
}

// 4. Cabin Experience Sanctuary Tabs
function initCabinTabs() {
  const tabBtns = document.querySelectorAll('.cabin-tab-btn');
  const tabContents = document.querySelectorAll('.cabin-tab-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');

      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      const activeContent = document.getElementById(targetTab);
      if (activeContent) activeContent.classList.add('active');
    });
  });
}

// 5. Fleet Category Filtering (Default VISIBLE)
function initFleetFiltering() {
  const pills = document.querySelectorAll('.filter-pill');
  const cards = document.querySelectorAll('.fleet-card');

  // Ensure all cards are visible immediately on load!
  cards.forEach(card => {
    card.style.display = 'flex';
    card.style.opacity = '1';
    card.style.transform = 'none';
  });

  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      pills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');

      const filter = pill.getAttribute('data-filter');

      cards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (filter === 'all' || category === filter) {
          card.style.display = 'flex';
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
          }, 30);
        } else {
          card.style.opacity = '0';
          card.style.transform = 'translateY(10px)';
          setTimeout(() => {
            card.style.display = 'none';
          }, 250);
        }
      });
    });
  });
}

// 6. 3D Perspective Card Tilt on Mouse Move
function init3DCardTilt() {
  const tiltCards = document.querySelectorAll('.fleet-card, .dest-card, .tier-card');

  tiltCards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const rotateX = ((y - centerY) / centerY) * -6;
      const rotateY = ((x - centerX) / centerX) * 6;

      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
    });
  });
}

// 7. Authentication Modals & Handling
function initAuthModals() {
  const loginForm = document.getElementById('ajaxLoginForm');
  const registerForm = document.getElementById('ajaxRegisterForm');

  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = loginForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;

      const username = document.getElementById('loginUsername').value.trim();
      const password = document.getElementById('loginPassword').value;

      try {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Verifying VIP Credentials...';

        const res = await fetch('/api/auth/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
          },
          body: JSON.stringify({ username, password })
        });

        const data = await res.json();
        if (res.ok && data.success) {
          showToast(data.message, 'success');
          setTimeout(() => window.location.reload(), 800);
        } else {
          showToast(data.error || 'Authentication failed.', 'error');
        }
      } catch (err) {
        console.error(err);
        showToast('Login server error.', 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    });
  }

  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = registerForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;

      const username = document.getElementById('regUsername').value.trim();
      const email = document.getElementById('regEmail').value.trim();
      const fullName = document.getElementById('regFullName').value.trim();
      const password = document.getElementById('regPassword').value;

      try {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Creating VIP Membership...';

        const res = await fetch('/api/auth/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
          },
          body: JSON.stringify({ username, email, full_name: fullName, password })
        });

        const data = await res.json();
        if (res.ok && data.success) {
          showToast(data.message, 'success');
          setTimeout(() => window.location.reload(), 800);
        } else {
          showToast(data.error || 'Registration failed.', 'error');
        }
      } catch (err) {
        console.error(err);
        showToast('Registration server error.', 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    });
  }
}

// 8. Smooth Scroll Anchor Navigation
function initScrollNav() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#' || targetId === '') return;
      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        e.preventDefault();
        const offset = 70;
        const bodyRect = document.body.getBoundingClientRect().top;
        const elementRect = targetEl.getBoundingClientRect().top;
        const elementPosition = elementRect - bodyRect;
        const offsetPosition = elementPosition - offset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    });
  });
}

// 9. Modals & Popups
function initModals() {
  const openButtons = document.querySelectorAll('[data-open-modal]');
  const closeButtons = document.querySelectorAll('.modal-close-btn, [data-close-modal]');
  const overlays = document.querySelectorAll('.modal-overlay');

  openButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const modalId = btn.getAttribute('data-open-modal');
      const targetModal = document.getElementById(modalId);
      if (targetModal) {
        // Close any other open modals first
        overlays.forEach(o => o.classList.remove('active'));
        targetModal.classList.add('active');
        document.body.style.overflow = 'hidden';

        const tierName = btn.getAttribute('data-tier-name');
        if (tierName) {
          const tierInput = document.getElementById('modalMembershipTier');
          if (tierInput) tierInput.value = tierName;
        }
      }
    });
  });

  closeButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      overlays.forEach(overlay => overlay.classList.remove('active'));
      document.body.style.overflow = '';
    });
  });

  overlays.forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        overlay.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  });
}

// 10. Global Toast Notification Function
window.showToast = function(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      ${type === 'success' 
        ? '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>' 
        : '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line>'}
    </svg>
    <span>${message}</span>
  `;

  container.appendChild(toast);
  setTimeout(() => toast.classList.add('show'), 50);

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 400);
  }, 4000);
};

// 11. Cabin Video Player Controls
window.toggleCabinVideo = function() {
  const video = document.getElementById('sanctuaryVideo');
  const overlay = document.getElementById('videoOverlay');
  if (!video) return;

  if (video.paused) {
    video.play().then(() => {
      if (overlay) overlay.style.opacity = '0';
    }).catch(err => {
      console.warn('Playback prevented:', err);
    });
  } else {
    video.pause();
    if (overlay) overlay.style.opacity = '1';
  }
};

// Sync video overlay when user interacts directly with native HTML5 controls
document.addEventListener('DOMContentLoaded', () => {
  const video = document.getElementById('sanctuaryVideo');
  const overlay = document.getElementById('videoOverlay');
  if (video && overlay) {
    video.addEventListener('play', () => {
      overlay.style.opacity = '0';
      overlay.style.pointerEvents = 'none';
    });
    video.addEventListener('pause', () => {
      overlay.style.opacity = '1';
      overlay.style.pointerEvents = 'auto';
    });
  }
});
