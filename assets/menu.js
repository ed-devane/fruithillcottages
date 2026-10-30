// Mobile menu toggle
(function () {
  var btn = document.querySelector('.menu-toggle');
  var nav = document.getElementById('site-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
      btn.textContent = open ? 'Close' : 'Menu';
    });
  }

  // Email links: build.py leaves the address in two parts to hide it from spam harvesters
  Array.prototype.forEach.call(document.querySelectorAll('a.email'), function (a) {
    var addr = a.getAttribute('data-u') + '@' + a.getAttribute('data-d');
    a.href = 'mailto:' + addr;
    if (a.hasAttribute('data-show')) a.textContent = addr;
  });

  // Simple lightbox for the cottage galleries
  var items = Array.prototype.slice.call(document.querySelectorAll('.gallery-item'));
  if (!items.length) return;
  var box, imgEl, index = 0;

  function show(i) {
    index = (i + items.length) % items.length;
    imgEl.src = items[index].getAttribute('href');
    imgEl.alt = items[index].querySelector('img').alt;
  }
  function close() {
    if (box) { box.remove(); box = null; document.removeEventListener('keydown', onKey); }
  }
  function onKey(e) {
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowRight') show(index + 1);
    if (e.key === 'ArrowLeft') show(index - 1);
  }
  function open(i) {
    box = document.createElement('div');
    box.className = 'lightbox';
    box.innerHTML = '<img alt=""><button class="lb-close" aria-label="Close">×</button>' +
      '<button class="lb-prev" aria-label="Previous">‹</button><button class="lb-next" aria-label="Next">›</button>';
    imgEl = box.querySelector('img');
    box.querySelector('.lb-close').onclick = close;
    box.querySelector('.lb-prev').onclick = function (e) { e.stopPropagation(); show(index - 1); };
    box.querySelector('.lb-next').onclick = function (e) { e.stopPropagation(); show(index + 1); };
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    document.body.appendChild(box);
    document.addEventListener('keydown', onKey);
    show(i);
  }
  items.forEach(function (a, i) {
    a.addEventListener('click', function (e) { e.preventDefault(); open(i); });
  });
})();
