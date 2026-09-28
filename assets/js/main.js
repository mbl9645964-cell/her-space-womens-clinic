(function () {
  'use strict';
  var d = document, root = d.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Year
  d.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Header state
  var header = d.querySelector('.site-header');
  function onScroll() { header && header.classList.toggle('scrolled', window.scrollY > 24); }
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile nav
  var burger = d.getElementById('burger'), nav = d.getElementById('nav');
  function setNav(open) {
    if (!burger || !nav) return;
    nav.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.querySelector('use').setAttribute('href', open ? '#i-close' : '#i-menu');
    d.body.classList.toggle('nav-open', open);
  }
  if (burger) {
    burger.addEventListener('click', function () { setNav(!nav.classList.contains('open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setNav(false); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') setNav(false); });
  }

  // Reveal on scroll
  var items = d.querySelectorAll('.reveal');
  if (reduce || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    items.forEach(function (el) { io.observe(el); });
  }

  // FAQ: one open at a time
  var faqs = d.querySelectorAll('.faq-list details');
  faqs.forEach(function (el) {
    el.addEventListener('toggle', function () {
      if (el.open) faqs.forEach(function (o) { if (o !== el) o.open = false; });
    });
  });

  // Hero parallax
  var art = d.querySelector('.hero-art');
  if (art && !reduce && window.matchMedia('(pointer: fine)').matches) {
    var hero = d.querySelector('.hero');
    hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
      art.style.setProperty('--px', (x * 14).toFixed(2) + 'px');
      art.style.setProperty('--py', (y * 12).toFixed(2) + 'px');
    });
  }

  // Appointment form -> WhatsApp
  var form = d.getElementById('apptForm');
  if (form) {
    var err = d.getElementById('formErr');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = form.name.value.trim(), phone = form.phone.value.replace(/[^\d+]/g, '');
      if (name.length < 2) { return show('Please enter your name.', form.name); }
      if (phone.replace(/\D/g, '').length < 10) { return show('Please enter a valid 10-digit phone number.', form.phone); }
      err.hidden = true;
      var msg = 'Hello Dr. Ruchi, I would like to book an appointment.\n\n' +
        'Name: ' + name + '\nPhone: ' + phone + '\nInterested in: ' + form.topic.value +
        (form.when.value.trim() ? '\nPreferred time: ' + form.when.value.trim() : '');
      window.open('https://wa.me/919265259256?text=' + encodeURIComponent(msg), '_blank', 'noopener');
    });
    function show(text, field) { err.textContent = text; err.hidden = false; field.focus(); }
  }
})();
