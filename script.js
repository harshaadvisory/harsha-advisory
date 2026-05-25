/* ============================================
   HARSHA DANA CONSULTING — SCRIPTS
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ---------- Navbar scroll effect ---------- */
  const nav = document.getElementById('nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 50);
    });
  }

  /* ---------- Mobile menu toggle ---------- */
  const mobileBtn = document.querySelector('.nav-mobile');
  const navLinks = document.querySelector('.nav-links');

  if (mobileBtn && navLinks) {
    mobileBtn.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
      });
    });
  }

  /* ---------- Fade-up on scroll ---------- */
  const fadeEls = document.querySelectorAll('.fade-up');
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
  );
  fadeEls.forEach((el) => observer.observe(el));

  /* ---------- Smooth scroll for anchor links ---------- */
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (e) => {
      e.preventDefault();
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* ---------- Portfolio Carousel ---------- */
  const track = document.getElementById('portfolioTrack');
  const prevBtn = document.getElementById('portfolioPrev');
  const nextBtn = document.getElementById('portfolioNext');

  if (track && prevBtn && nextBtn) {
    const cards = Array.from(track.querySelectorAll('.portfolio-card'));
    const totalCards = cards.length;
    let currentIndex = 0;
    let autoplayTimer = null;
    let isTransitioning = false;

    function getCardWidth() {
      return cards[0].offsetWidth + parseFloat(getComputedStyle(track).gap);
    }

    function updateCarousel(animate) {
      const cardWidth = getCardWidth();
      const carouselWidth = track.parentElement.offsetWidth;
      const centerOffset = (carouselWidth / 2) - (cards[0].offsetWidth / 2);
      const translateX = centerOffset - (currentIndex * cardWidth);

      track.style.transition = animate ? 'transform .5s cubic-bezier(.25,.8,.25,1)' : 'none';
      track.style.transform = 'translateX(' + translateX + 'px)';

      cards.forEach((card, i) => {
        card.classList.remove('active', 'adjacent');
        if (i === currentIndex) {
          card.classList.add('active');
        } else if (i === currentIndex - 1 || i === currentIndex + 1) {
          card.classList.add('adjacent');
        }
      });
    }

    function goTo(index, animate) {
      if (isTransitioning) return;
      isTransitioning = true;
      currentIndex = ((index % totalCards) + totalCards) % totalCards;
      updateCarousel(animate !== false);
      setTimeout(function() { isTransitioning = false; }, 550);
    }

    function goNext() { goTo(currentIndex + 1); }
    function goPrev() { goTo(currentIndex - 1); }

    function startAutoplay() {
      stopAutoplay();
      autoplayTimer = setInterval(goNext, 3500);
    }

    function stopAutoplay() {
      if (autoplayTimer) clearInterval(autoplayTimer);
    }

    nextBtn.addEventListener('click', function() { stopAutoplay(); goNext(); startAutoplay(); });
    prevBtn.addEventListener('click', function() { stopAutoplay(); goPrev(); startAutoplay(); });

    // Pause on hover
    track.parentElement.addEventListener('mouseenter', stopAutoplay);
    track.parentElement.addEventListener('mouseleave', startAutoplay);

    // Touch swipe support
    var touchStartX = 0;
    track.addEventListener('touchstart', function(e) { touchStartX = e.changedTouches[0].screenX; stopAutoplay(); }, { passive: true });
    track.addEventListener('touchend', function(e) {
      var diff = touchStartX - e.changedTouches[0].screenX;
      if (Math.abs(diff) > 50) {
        if (diff > 0) goNext(); else goPrev();
      }
      startAutoplay();
    }, { passive: true });

    // Init
    updateCarousel(false);
    window.addEventListener('resize', function() { updateCarousel(false); });

    // Start autoplay only when section is visible
    var portfolioSection = document.getElementById('portfolio');
    var portfolioObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) startAutoplay();
        else stopAutoplay();
      });
    }, { threshold: 0.3 });
    portfolioObserver.observe(portfolioSection);
  }

  /* ---------- Filter Buttons (Case Studies & Insights) ---------- */
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      this.parentElement.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
    });
  });

  /* ---------- FAQ Accordion (only one open at a time) ---------- */
  document.querySelectorAll('.faq-item').forEach(item => {
    item.addEventListener('toggle', function() {
      if (this.open) {
        document.querySelectorAll('.faq-item').forEach(other => {
          if (other !== this && other.open) other.open = false;
        });
      }
    });
  });

  // Redirect /index.html → /
  if (window.location.pathname.endsWith('index.html')) {
     window.location.replace(
       window.location.pathname.replace('index.html', '')
     );
   }
});
