// FDE Field Notes — shared article behaviour: reading progress, share card, tracker.
(function () {
  var bar = document.getElementById('progress');
  if (bar) {
    var onScroll = function () {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
    };
    document.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  var canonical = document.querySelector('link[rel="canonical"]');
  var url = canonical ? canonical.href : location.href;
  var quoteEl = document.querySelector('.share blockquote');
  var quote = quoteEl ? quoteEl.textContent.trim() : document.title;

  var x = document.getElementById('share-x');
  if (x) x.href = 'https://x.com/intent/tweet?text=' + encodeURIComponent(quote) + '&url=' + encodeURIComponent(url);
  var li = document.getElementById('share-li');
  if (li) li.href = 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(url);

  var copy = document.getElementById('share-copy');
  if (copy) {
    copy.addEventListener('click', function () {
      var text = quote + ' ' + url;
      var done = function () {
        copy.textContent = 'Copied ✓';
        setTimeout(function () { copy.textContent = 'Copy text & link'; }, 1800);
      };
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () {});
    });
  }

  // Tracker: remember checked takeaways per article (convenience only).
  var key = 'fdefn:' + location.pathname;
  var boxes = document.querySelectorAll('.tracker input[type=checkbox]');
  var saved = [];
  try { saved = JSON.parse(localStorage.getItem(key) || '[]'); } catch (e) {}
  boxes.forEach(function (b, i) {
    if (saved[i]) b.checked = true;
    b.addEventListener('change', function () {
      var state = Array.prototype.map.call(boxes, function (x) { return x.checked; });
      try { localStorage.setItem(key, JSON.stringify(state)); } catch (e) {}
    });
  });
})();
