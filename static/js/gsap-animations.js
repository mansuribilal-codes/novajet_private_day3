/**
 * NovaJet Private - GSAP & ScrollTrigger Animation Engine (Fail-Safe)
 * Guaranteed 100% visibility for all cards, tiers, and destinations
 */

document.addEventListener('DOMContentLoaded', () => {
  // Ensure all essential cards and containers are visible immediately!
  document.querySelectorAll('.dest-card, .tier-card, .fleet-card, .empty-leg-card, .timeline-content').forEach(el => {
    el.style.opacity = '1';
    el.style.visibility = 'visible';
  });

  if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  initLenisSmoothScroll();
  initHeroEntranceAnimation();
  initStatsCounterAnimation();
});

// 1. Lenis Smooth Scrolling Integration with ScrollTrigger
function initLenisSmoothScroll() {
  if (typeof Lenis === 'undefined') return;

  const lenis = new Lenis({
    duration: 1.1,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    orientation: 'vertical',
    gestureOrientation: 'vertical',
    smoothWheel: true,
    wheelMultiplier: 0.95,
    touchMultiplier: 1.5,
  });

  lenis.on('scroll', ScrollTrigger.update);

  gsap.ticker.add((time) => {
    lenis.raf(time * 1000);
  });

  gsap.ticker.lagSmoothing(0);
}

// 2. Cinematic Hero Entrance (Non-blocking)
function initHeroEntranceAnimation() {
  const heroTimeline = gsap.timeline({ defaults: { ease: 'power3.out', duration: 0.9 } });

  heroTimeline
    .fromTo('.hero-tagline', { opacity: 0, y: -10 }, { opacity: 1, y: 0, delay: 0.1 })
    .fromTo('.hero-title', { opacity: 0, y: 20 }, { opacity: 1, y: 0 }, '-=0.6')
    .fromTo('.hero-subtext', { opacity: 0, y: 15 }, { opacity: 1, y: 0 }, '-=0.5')
    .fromTo('.hero-cta-group .btn', { opacity: 0, y: 10 }, { opacity: 1, y: 0, stagger: 0.1 }, '-=0.4')
    .fromTo('.hero-hud-preview', { opacity: 0, y: 15 }, { opacity: 1, y: 0 }, '-=0.3');
}

// 3. Animated Statistics Numbers on Scroll
function initStatsCounterAnimation() {
  const statNumbers = document.querySelectorAll('.stat-number');
  if (!statNumbers.length) return;

  statNumbers.forEach((el) => {
    const targetValue = parseFloat(el.getAttribute('data-target') || '0');
    const prefix = el.getAttribute('data-prefix') || '';
    const suffix = el.getAttribute('data-suffix') || '';
    const isDecimal = el.getAttribute('data-decimal') === 'true';

    const countObj = { val: 0 };

    ScrollTrigger.create({
      trigger: el,
      start: 'top 90%',
      once: true,
      onEnter: () => {
        gsap.to(countObj, {
          val: targetValue,
          duration: 1.8,
          ease: 'power2.out',
          onUpdate: () => {
            if (isDecimal) {
              el.innerText = `${prefix}${countObj.val.toFixed(1)}${suffix}`;
            } else {
              el.innerText = `${prefix}${Math.floor(countObj.val)}${suffix}`;
            }
          }
        });
      }
    });
  });
}
