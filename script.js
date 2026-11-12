/* HARSHA ADVISORY: interaksi ringan (menu, header, animasi masuk) */
(function () {
  var header = document.querySelector('.site-header');
  var nav = document.getElementById('site-nav');
  var toggle = document.querySelector('.nav-toggle');
  var mobileCta = document.querySelector('.mobile-cta');

  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('scrolled', y > 10);
    if (mobileCta) mobileCta.classList.toggle('show', y > 600);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Galeri produk: geser (swipe), tombol panah, dan thumbnail.
  document.querySelectorAll('[data-gallery]').forEach(function (g) {
    var track = g.querySelector('.gallery-track');
    var thumbs = g.querySelectorAll('.gallery-thumbs button');
    var prev = g.querySelector('.gallery-nav.prev');
    var next = g.querySelector('.gallery-nav.next');
    var count = thumbs.length;
    function current() { return Math.round(track.scrollLeft / track.clientWidth); }
    function go(i) { track.scrollTo({ left: Math.max(0, Math.min(count - 1, i)) * track.clientWidth }); }
    function sync() {
      var i = current();
      thumbs.forEach(function (b, k) { if (k === i) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current'); });
      prev.disabled = i <= 0;
      next.disabled = i >= count - 1;
    }
    thumbs.forEach(function (b, k) { b.addEventListener('click', function () { go(k); }); });
    prev.addEventListener('click', function () { go(current() - 1); });
    next.addEventListener('click', function () { go(current() + 1); });
    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(current() - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); go(current() + 1); }
    });
    track.addEventListener('scroll', function () { window.requestAnimationFrame(sync); }, { passive: true });
    sync();
  });

  var els = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {
    els.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  els.forEach(function (el) { io.observe(el); });
})();
