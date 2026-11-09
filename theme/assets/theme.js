/* Altura theme — vanilla JS, no dependencies */
(() => {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const routes = (window.theme && window.theme.routes) || {};

  const money = (cents) => {
    const fmt = (window.theme && window.theme.moneyFormat) || '${{amount}}';
    const v = (cents / 100).toFixed(2);
    return fmt.replace(/\{\{\s*(\w+)\s*\}\}/, (_, k) =>
      k === 'amount_no_decimals' ? Math.round(cents / 100).toLocaleString('en-US') :
      k === 'amount_with_comma_separator' ? v.replace('.', ',') :
      Number(v).toLocaleString('en-US', { minimumFractionDigits: 2 }));
  };

  const toast = (msg) => {
    const t = $('#Toast'); if (!t) return;
    t.textContent = msg; t.classList.add('is-visible');
    clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove('is-visible'), 2600);
  };

  /* ---------- Reveal on scroll ---------- */
  const revealIO = 'IntersectionObserver' in window ? new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('is-in'); revealIO.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }) : null;
  const initReveal = (root = document) => {
    const on = getComputedStyle(document.documentElement).getPropertyValue('--animations').trim() !== '0';
    $$('[data-reveal]', root).forEach((el) => { if (!on || !revealIO) el.classList.add('is-in'); else revealIO.observe(el); });
  };

  /* ---------- Header ---------- */
  const initHeader = () => {
    const wrap = $('.header-wrapper'); if (!wrap) return;
    let last = window.scrollY;
    const overlay = wrap.classList.contains('header-wrapper--overlay');
    const onScroll = () => {
      const y = window.scrollY;
      wrap.classList.toggle('is-solid', y > (overlay ? 60 : 4));
      if (wrap.dataset.sticky === 'smart') wrap.classList.toggle('is-hidden', y > last && y > 300 && !document.body.classList.contains('no-scroll'));
      last = y;
    };
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  };

  /* ---------- Drawers ---------- */
  const openDrawer = (el) => { if (!el) return; el.classList.add('is-open'); document.body.classList.add('no-scroll'); el.setAttribute('aria-hidden', 'false'); setTimeout(() => { const f = $('[data-autofocus], button, a', $('.drawer__panel', el)); f && f.focus(); }, 60); };
  const closeDrawer = (el) => { if (!el) return; el.classList.remove('is-open'); document.body.classList.remove('no-scroll'); el.setAttribute('aria-hidden', 'true'); };
  document.addEventListener('click', (e) => {
    const opener = e.target.closest('[data-drawer-open]');
    if (opener) { e.preventDefault(); openDrawer(document.getElementById(opener.dataset.drawerOpen)); return; }
    const closer = e.target.closest('[data-drawer-close]');
    if (closer) { e.preventDefault(); closeDrawer(closer.closest('.drawer')); }
  });
  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    $$('.drawer.is-open').forEach(closeDrawer); closeSearch(); closeLightbox();
    $$('.filters-panel.is-open').forEach((p) => p.classList.remove('is-open'));
  });

  /* ---------- Announcement ---------- */
  const initAnnouncement = () => {
    $$('[data-announcement]').forEach((bar) => {
      const slides = $$('.announcement__slide', bar); if (slides.length < 2) return;
      let i = 0; setInterval(() => { slides[i].classList.remove('is-active'); i = (i + 1) % slides.length; slides[i].classList.add('is-active'); }, 4500);
    });
  };

  /* ---------- Hero slideshow ---------- */
  const initHero = (root = document) => {
    $$('[data-hero]', root).forEach((hero) => {
      const slides = $$('.hero__slide', hero), dots = $$('.hero__dot', hero);
      const ms = (parseInt(hero.dataset.autoplay, 10) || 6) * 1000;
      let i = 0, timer;
      const go = (n) => {
        slides[i].classList.remove('is-active'); dots[i] && dots[i].classList.remove('is-active');
        i = (n + slides.length) % slides.length;
        slides[i].classList.add('is-active');
        if (dots[i]) { dots[i].classList.remove('is-active'); void dots[i].offsetWidth; dots[i].classList.add('is-active'); }
        const v = $('video', slides[i]); v && v.play().catch(() => {});
      };
      const play = () => { clearInterval(timer); if (slides.length > 1) timer = setInterval(() => go(i + 1), ms); };
      dots.forEach((d, n) => d.addEventListener('click', () => { go(n); play(); }));
      const toggle = $('[data-hero-toggle]', hero);
      toggle && toggle.addEventListener('click', () => {
        const paused = hero.classList.toggle('is-paused');
        paused ? clearInterval(timer) : play();
        toggle.setAttribute('aria-label', paused ? 'Play slideshow' : 'Pause slideshow');
        toggle.innerHTML = paused ? '<svg class="icon" width="18" height="18" viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>' : '<svg class="icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M8 5v14M16 5v14"/></svg>';
      });
      hero.style.setProperty('--autoplay', ms / 1000 + 's');
      if (slides[0]) { slides[0].classList.add('is-active'); dots[0] && dots[0].classList.add('is-active'); }
      play();
    });
  };

  /* ---------- Rails ---------- */
  const initRails = (root = document) => {
    $$('[data-rail-wrap]', root).forEach((wrap) => {
      const rail = $('.rail', wrap); if (!rail) return;
      const prog = $('.rail-progress span', wrap);
      const step = () => { const c = rail.firstElementChild; return c ? c.getBoundingClientRect().width + parseFloat(getComputedStyle(rail).columnGap || 24) : 300; };
      $$('[data-rail-prev]', wrap).forEach((b) => b.addEventListener('click', () => rail.scrollBy({ left: -step(), behavior: 'smooth' })));
      $$('[data-rail-next]', wrap).forEach((b) => b.addEventListener('click', () => rail.scrollBy({ left: step(), behavior: 'smooth' })));
      const upd = () => { if (!prog) return; const max = rail.scrollWidth - rail.clientWidth; const vis = rail.clientWidth / rail.scrollWidth; prog.parentElement.style.display = max <= 2 ? 'none' : ''; prog.style.setProperty('--p', Math.min(1, vis + (max > 0 ? (rail.scrollLeft / max) * (1 - vis) : 1))); };
      rail.addEventListener('scroll', upd, { passive: true }); window.addEventListener('resize', upd); upd();
    });
  };

  /* ---------- Tabs ---------- */
  const initTabs = (root = document) => {
    $$('[data-tabs]', root).forEach((wrap) => {
      const tabs = $$('[role="tab"]', wrap);
      tabs.forEach((t) => t.addEventListener('click', () => {
        tabs.forEach((x) => { x.setAttribute('aria-selected', x === t); const p = document.getElementById(x.getAttribute('aria-controls')); if (p) p.hidden = x !== t; });
        const p = document.getElementById(t.getAttribute('aria-controls')); p && initReveal(p) && initRails(p);
        p && $$('[data-reveal]', p).forEach((el) => el.classList.add('is-in'));
      }));
    });
  };

  /* ---------- Search ---------- */
  let searchCtl;
  const openSearch = () => { const m = $('#SearchModal'); if (!m) return; m.hidden = false; document.body.classList.add('no-scroll'); setTimeout(() => $('#SearchInput').focus(), 50); };
  function closeSearch() { const m = $('#SearchModal'); if (!m || m.hidden) return; m.hidden = true; document.body.classList.remove('no-scroll'); }
  const initSearch = () => {
    document.addEventListener('click', (e) => {
      if (e.target.closest('[data-search-open]')) { e.preventDefault(); openSearch(); }
      if (e.target.closest('[data-search-close]')) closeSearch();
    });
    const input = $('#SearchInput'), out = $('#PredictiveResults'); if (!input || !out) return;
    const initial = out.innerHTML; let t;
    input.addEventListener('input', () => {
      clearTimeout(t); const q = input.value.trim();
      if (!q) { out.innerHTML = initial; return; }
      t = setTimeout(async () => {
        searchCtl && searchCtl.abort(); searchCtl = new AbortController();
        try {
          const url = `${routes.predictive_search_url}?q=${encodeURIComponent(q)}&resources[type]=product,collection,page,article&resources[limit]=8&section_id=predictive-search`;
          const html = await (await fetch(url, { signal: searchCtl.signal })).text();
          const doc = new DOMParser().parseFromString(html, 'text/html');
          const res = $('#shopify-section-predictive-search', doc) || doc.body;
          out.innerHTML = res.innerHTML;
        } catch (err) { if (err.name !== 'AbortError') console.error(err); }
      }, 220);
    });
  };

  /* ---------- Cart ---------- */
  const cartSections = () => ['cart-drawer'];
  const updateCount = (count) => {
    $$('[data-cart-count]').forEach((el) => { el.textContent = count > 0 ? count : ''; el.dataset.count = count; el.classList.remove('bump'); void el.offsetWidth; el.classList.add('bump'); });
  };
  const renderCartSections = (sections) => {
    if (!sections) return;
    const html = sections['cart-drawer']; if (!html) return;
    const doc = new DOMParser().parseFromString(html, 'text/html');
    const fresh = $('[data-cart-drawer-inner]', doc), cur = $('[data-cart-drawer-inner]');
    if (fresh && cur) cur.replaceWith(fresh);
  };
  const refreshCart = async () => {
    const r = await fetch(`${routes.root}?sections=${cartSections().join(',')}`); renderCartSections(await r.json());
    const c = await (await fetch(`${routes.cart_url}.js`)).json(); updateCount(c.item_count); return c;
  };
  const openCart = () => { if (document.body.classList.contains('template-cart')) { location.reload(); return; } openDrawer($('#CartDrawer')); };

  const addToCart = async (formData, btn) => {
    btn && btn.classList.add('is-loading');
    formData.append('sections', cartSections().join(','));
    formData.append('sections_url', location.pathname);
    try {
      const r = await fetch(`${routes.cart_add_url}.js`, { method: 'POST', headers: { Accept: 'application/javascript', 'X-Requested-With': 'XMLHttpRequest' }, body: formData });
      const data = await r.json();
      if (data.status) { toast(data.description || data.message || 'Could not add to bag'); return; }
      renderCartSections(data.sections);
      const c = await (await fetch(`${routes.cart_url}.js`)).json(); updateCount(c.item_count);
      openCart();
    } catch (e) { console.error(e); toast('Something went wrong, please try again'); }
    finally { btn && btn.classList.remove('is-loading'); }
  };

  document.addEventListener('submit', (e) => {
    const form = e.target.closest('form[data-product-form]'); if (!form) return;
    e.preventDefault();
    addToCart(new FormData(form), e.submitter || $('[type="submit"]', form));
  });
  document.addEventListener('click', (e) => {
    const quick = e.target.closest('[data-quick-add]');
    if (quick) { e.preventDefault(); const fd = new FormData(); fd.append('id', quick.dataset.quickAdd); fd.append('quantity', 1); addToCart(fd, quick); return; }
    const cartOpen = e.target.closest('[data-cart-open]');
    if (cartOpen && $('#CartDrawer')) { e.preventDefault(); openCart(); }
  });

  const changeLine = async (key, quantity, row) => {
    row && row.classList.add('results-loading');
    try {
      const r = await fetch(`${routes.cart_change_url}.js`, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify({ id: key, quantity, sections: cartSections(), sections_url: location.pathname }) });
      const data = await r.json();
      if (data.status) { toast(data.description || data.message); row && row.classList.remove('results-loading'); return; }
      if (document.body.classList.contains('template-cart')) { location.reload(); return; }
      renderCartSections(data.sections); updateCount(data.item_count);
    } catch (e) { console.error(e); }
  };
  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-line-qty]');
    if (b) {
      const row = b.closest('[data-line-key]'); const input = $('input', b.parentElement);
      const q = Math.max(0, parseInt(input.value, 10) + parseInt(b.dataset.lineQty, 10));
      changeLine(row.dataset.lineKey, q, row); return;
    }
    const rm = e.target.closest('[data-line-remove]');
    if (rm) { e.preventDefault(); const row = rm.closest('[data-line-key]'); changeLine(row.dataset.lineKey, 0, row); }
  });
  document.addEventListener('change', (e) => {
    const i = e.target.closest('[data-line-key] input[type="number"]');
    if (i) { const row = i.closest('[data-line-key]'); changeLine(row.dataset.lineKey, Math.max(0, parseInt(i.value, 10) || 0), row); }
    const note = e.target.closest('[data-cart-note]');
    if (note) fetch(`${routes.cart_update_url}.js`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ note: note.value }) });
  });

  /* ---------- Quantity steppers (product forms) ---------- */
  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-qty-step]'); if (!b) return;
    const input = $('input', b.closest('.qty')); const min = parseInt(input.min || 1, 10);
    input.value = Math.max(min, (parseInt(input.value, 10) || min) + parseInt(b.dataset.qtyStep, 10));
    input.dispatchEvent(new Event('change', { bubbles: true }));
  });

  /* ---------- Product page ---------- */
  const initProduct = (root = document) => {
    $$('[data-product]', root).forEach((wrap) => {
      const json = $('[data-product-json]', wrap); if (!json) return;
      const product = JSON.parse(json.textContent);
      const form = $('form[data-product-form]', wrap);
      const idInput = form && $('input[name="id"]', form);
      const priceEl = $('[data-price]', wrap), btn = $('[data-add-button]', wrap), stock = $('[data-stock]', wrap);
      const sticky = $('[data-sticky-atc]');
      const selected = () => $$('[data-option-index]', wrap).map((fs) => { const c = $('input:checked', fs); return c ? c.value : null; });

      const renderPrice = (v) => {
        if (!priceEl) return;
        const sale = v.compare_at_price && v.compare_at_price > v.price;
        priceEl.className = 'price' + (sale ? ' price--sale' : '');
        priceEl.innerHTML = `<span class="price__current">${money(v.price)}</span>${sale ? `<s>${money(v.compare_at_price)}</s><span class="badge badge--sale">Save ${Math.round((1 - v.price / v.compare_at_price) * 100)}%</span>` : ''}`;
      };
      const markAvailability = (opts) => {
        $$('[data-option-index]', wrap).forEach((fs) => {
          const idx = parseInt(fs.dataset.optionIndex, 10);
          $$('input', fs).forEach((inp) => {
            const test = opts.slice(); test[idx] = inp.value;
            const ok = product.variants.some((v) => v.available && v.options.every((o, k) => o === test[k]));
            inp.classList.toggle('is-unavailable', !ok);
          });
          const lab = $('[data-option-value]', fs); const c = $('input:checked', fs); if (lab && c) lab.textContent = c.value;
        });
      };
      const update = () => {
        const opts = selected();
        const v = product.variants.find((x) => x.options.every((o, k) => o === opts[k]));
        markAvailability(opts);
        if (!v) { if (btn) { btn.disabled = true; btn.querySelector('span').textContent = 'Unavailable'; } return; }
        if (idInput) idInput.value = v.id;
        renderPrice(v);
        if (btn) { btn.disabled = !v.available; btn.querySelector('span').textContent = v.available ? (btn.dataset.label || 'Add to bag') : 'Sold out'; }
        if (stock) {
          const q = parseInt((wrap.querySelector(`[data-inv="${v.id}"]`) || {}).value, 10);
          stock.className = 'stock' + (!v.available ? ' stock--out' : (q > 0 && q < 15 ? ' stock--low' : ''));
          $('span:last-child', stock).textContent = !v.available ? 'Sold out — back soon' : (q > 0 && q < 15 ? `Only ${q} left — roasted this week` : 'In stock — roasted to order, ships in 24h');
        }
        if (v.featured_media) {
          const m = wrap.querySelector(`[data-media-id="${v.featured_media.id}"]`);
          $$('.gallery__item', wrap).forEach((g) => g.classList.remove('is-variant-match'));
          if (m && m.closest('.gallery')) {
            m.classList.add('is-variant-match');
            const first = $('.gallery__item', wrap); const img = $('img', m);
            if (first && img && first !== m) { const fi = $('img', first); fi.src = img.currentSrc || img.src; fi.srcset = img.srcset; }
          }
          const mm = wrap.querySelector(`.gallery-mobile [data-media-id="${v.featured_media.id}"]`);
          mm && mm.parentElement.scrollTo({ left: mm.offsetLeft - mm.parentElement.offsetLeft - 16, behavior: 'smooth' });
        }
        if (sticky) {
          const sv = $('[data-sticky-variant]', sticky); sv && (sv.textContent = v.title === 'Default Title' ? '' : v.title);
          const sp = $('[data-sticky-price]', sticky); sp && (sp.textContent = money(v.price));
          const sb = $('button', sticky); if (sb) { sb.disabled = !v.available; sb.dataset.quickAdd = v.id; }
        }
        if (wrap.dataset.updateUrl !== 'false') history.replaceState({}, '', `${location.pathname}?variant=${v.id}`);
      };
      wrap.addEventListener('change', (e) => { if (e.target.closest('[data-option-index]')) update(); });
      markAvailability(selected());

      // Sticky ATC visibility
      if (sticky && btn && 'IntersectionObserver' in window) {
        new IntersectionObserver(([en]) => sticky.classList.toggle('is-visible', !en.isIntersecting && en.boundingClientRect.top < 0), { threshold: 0 }).observe(btn);
      }
      // Lightbox
      $$('.gallery__item', wrap).forEach((g, n) => g.addEventListener('click', () => openLightbox($$('.gallery__item img', wrap).map((i) => i.dataset.full || i.src), n)));
      // Mobile dots
      const mr = $('.gallery-mobile .rail', wrap), dots = $$('.gallery-mobile__dots i', wrap);
      mr && mr.addEventListener('scroll', () => { const n = Math.round(mr.scrollLeft / (mr.firstElementChild.getBoundingClientRect().width + 10)); dots.forEach((d, k) => d.classList.toggle('on', k === n)); }, { passive: true });
    });
  };

  /* ---------- Lightbox ---------- */
  let lb, lbImgs = [], lbI = 0;
  const openLightbox = (imgs, i) => {
    if (!lb) {
      lb = document.createElement('div'); lb.className = 'lightbox'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-label', 'Image viewer');
      lb.innerHTML = '<img alt=""><button class="lightbox__close" aria-label="Close">✕</button><button class="lightbox__prev" aria-label="Previous">←</button><button class="lightbox__next" aria-label="Next">→</button>';
      document.body.appendChild(lb);
      lb.addEventListener('click', (e) => {
        if (e.target.closest('.lightbox__prev')) show(lbI - 1); else if (e.target.closest('.lightbox__next')) show(lbI + 1); else if (e.target.tagName !== 'IMG') closeLightbox();
      });
    }
    lbImgs = imgs; show(i); lb.classList.add('is-open'); document.body.classList.add('no-scroll');
  };
  const show = (i) => { lbI = (i + lbImgs.length) % lbImgs.length; $('img', lb).src = lbImgs[lbI]; };
  function closeLightbox() { if (lb && lb.classList.contains('is-open')) { lb.classList.remove('is-open'); document.body.classList.remove('no-scroll'); } }

  /* ---------- Recommendations ---------- */
  const initRecs = (root = document) => {
    $$('[data-recommendations]', root).forEach(async (el) => {
      if (el.dataset.loaded) return; el.dataset.loaded = 1;
      try {
        const html = await (await fetch(el.dataset.url)).text();
        const doc = new DOMParser().parseFromString(html, 'text/html');
        const fresh = $('[data-recommendations]', doc);
        if (fresh && fresh.innerHTML.trim().length) { el.innerHTML = fresh.innerHTML; initReveal(el); initRails(el); $$('[data-reveal]', el).forEach((x) => x.classList.add('is-in')); }
      } catch (e) { console.error(e); }
    });
  };

  /* ---------- Collection filters (AJAX) ---------- */
  const initFilters = () => {
    const sec = $('[data-collection-section]'); if (!sec) return;
    const sectionId = sec.dataset.sectionId;
    const load = async (url, push = true) => {
      const res = $('#CollectionResults'); res && res.classList.add('results-loading');
      const u = new URL(url, location.origin); u.searchParams.set('section_id', sectionId);
      const html = await (await fetch(u)).text();
      const doc = new DOMParser().parseFromString(html, 'text/html');
      ['#CollectionResults', '#FiltersForm', '#TagFilters', '#ActiveFilters', '#ProductCount'].forEach((s) => { const a = $(s), b = $(s, doc); if (a && b) a.replaceWith(b); });
      // keep open filter groups open
      initReveal($('#CollectionResults')); $$('#CollectionResults [data-reveal]').forEach((x) => x.classList.add('is-in'));
      if (push) { u.searchParams.delete('section_id'); history.pushState({}, '', u); }
    };
    const fromForm = () => {
      const form = $('#FiltersForm'); const fd = new FormData(form);
      const sort = $('#SortBy'); if (sort) fd.set('sort_by', sort.value);
      const params = new URLSearchParams();
      for (const [k, v] of fd.entries()) if (v !== '') params.append(k, v);
      return `${location.pathname}?${params.toString()}`;
    };
    let t;
    document.addEventListener('change', (e) => {
      if (e.target.closest('#FiltersForm') || e.target.id === 'SortBy') { clearTimeout(t); t = setTimeout(() => load(fromForm()), e.target.type === 'number' ? 600 : 0); }
    });
    document.addEventListener('click', (e) => {
      const a = e.target.closest('#ActiveFilters a, [data-filter-link], .pagination a');
      if (a && a.closest('[data-collection-section]')) { e.preventDefault(); load(a.href); if (a.closest('.pagination')) sec.scrollIntoView({ behavior: 'smooth' }); }
      if (e.target.closest('[data-filters-open]')) $('.filters-panel').classList.add('is-open');
      if (e.target.closest('[data-filters-close]')) $('.filters-panel').classList.remove('is-open');
    });
    window.addEventListener('popstate', () => load(location.href, false));
  };

  /* ---------- Origins ---------- */
  const initOrigins = (root = document) => {
    $$('[data-origins]', root).forEach((wrap) => {
      const items = $$('.origins__item', wrap), imgs = $$('.origins__img', wrap);
      const set = (n) => { items.forEach((x, k) => { x.classList.toggle('is-active', k === n); $('button', x).setAttribute('aria-expanded', k === n); }); imgs.forEach((x, k) => x.classList.toggle('is-active', k === n)); };
      items.forEach((it, n) => { const b = $('button', it); b.addEventListener('click', () => set(n)); b.addEventListener('mouseenter', () => matchMedia('(hover:hover)').matches && set(n)); });
    });
  };

  /* ---------- Brew calculator ---------- */
  const initBrew = (root = document) => {
    $$('[data-brew]', root).forEach((wrap) => {
      const methods = JSON.parse($('[data-brew-methods]', wrap).textContent);
      const cups = $('[name="cups"]', wrap), strength = $('[name="strength"]', wrap);
      let m = methods[0];
      const fill = (r) => r.style.setProperty('--fill', ((r.value - r.min) / (r.max - r.min)) * 100 + '%');
      const calc = () => {
        const ml = cups.value * m.cup;
        const ratio = m.ratio - (strength.value - 3) * 1;
        const g = ml / ratio;
        $('[data-out="cups"]', wrap).textContent = `${cups.value} × ${m.cup} ml`;
        $('[data-out="strength"]', wrap).textContent = ['Light', 'Mellow', 'Balanced', 'Bold', 'Intense'][strength.value - 1];
        $('[data-out="coffee"]', wrap).textContent = g.toFixed(1);
        $('[data-out="water"]', wrap).textContent = Math.round(ml);
        $('[data-out="ratio"]', wrap).textContent = `1:${ratio}`;
        $('[data-out="grind"]', wrap).textContent = m.grind;
        $('[data-out="time"]', wrap).textContent = m.time;
        $('[data-out="temp"]', wrap).textContent = m.temp;
        $('[data-out="steps"]', wrap).innerHTML = m.steps.map((s) => `<li>${s.replace('{g}', g.toFixed(0)).replace('{ml}', Math.round(ml)).replace('{bloom}', Math.round(g * 2))}</li>`).join('');
        fill(cups); fill(strength);
      };
      $$('[data-method]', wrap).forEach((b) => b.addEventListener('click', () => {
        $$('[data-method]', wrap).forEach((x) => x.setAttribute('aria-pressed', x === b)); m = methods.find((x) => x.id === b.dataset.method); calc();
      }));
      cups.addEventListener('input', calc); strength.addEventListener('input', calc); calc();
    });
  };

  /* ---------- Hotspots ---------- */
  document.addEventListener('click', (e) => {
    const dot = e.target.closest('.hotspot__dot');
    $$('.hotspot.is-open').forEach((h) => { if (!dot || h !== dot.parentElement) h.classList.remove('is-open'); });
    if (dot) dot.parentElement.classList.toggle('is-open');
  });

  /* ---------- Testimonials ---------- */
  const initQuotes = (root = document) => {
    $$('[data-quotes]', root).forEach((wrap) => {
      const qs = $$('.quote', wrap), nav = $$('.quotes__nav button', wrap); let i = 0, t;
      const go = (n) => { qs[i].classList.remove('is-active'); nav[i] && nav[i].setAttribute('aria-current', 'false'); i = n % qs.length; qs[i].classList.add('is-active'); nav[i] && nav[i].setAttribute('aria-current', 'true'); };
      nav.forEach((b, n) => b.addEventListener('click', () => { go(n); clearInterval(t); }));
      if (qs.length > 1) t = setInterval(() => go(i + 1), 7000);
    });
  };

  /* ---------- Countdown ---------- */
  const initCountdown = (root = document) => {
    $$('[data-countdown]', root).forEach((el) => {
      let end = new Date((el.dataset.countdown || '').replace(' ', 'T')).getTime();
      if (isNaN(end) || end < Date.now()) { end = Date.now() + (3 * 86400 + 14 * 3600 + 22 * 60) * 1000; }
      const set = (k, v) => { const n = $(`[data-cd="${k}"]`, el); if (n) n.textContent = String(v).padStart(2, '0'); };
      const tick = () => { let s = Math.max(0, Math.floor((end - Date.now()) / 1000)); set('d', Math.floor(s / 86400)); s %= 86400; set('h', Math.floor(s / 3600)); s %= 3600; set('m', Math.floor(s / 60)); set('s', s % 60); };
      tick(); setInterval(tick, 1000);
    });
  };

  /* ---------- Init ---------- */
  const initAll = (root = document) => { initReveal(root); initHero(root); initRails(root); initTabs(root); initProduct(root); initRecs(root); initOrigins(root); initBrew(root); initQuotes(root); initCountdown(root); };
  document.addEventListener('DOMContentLoaded', () => { initHeader(); initAnnouncement(); initSearch(); initFilters(); initAll(); });
  document.addEventListener('shopify:section:load', (e) => initAll(e.target));
  document.addEventListener('shopify:block:select', (e) => {
    const slide = e.target.closest('.hero__slide'); if (slide) { $$('.hero__slide', slide.parentElement).forEach((s) => s.classList.toggle('is-active', s === slide)); }
  });
  window.AlturaCart = { refresh: refreshCart, open: openCart };
})();
