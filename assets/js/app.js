/* Maison Aelyra — рендер страницы из content.js.
   Чтобы добавить новый тип блока: напишите функцию в объекте `sections`
   (она получает объект секции и возвращает HTML-строку). */
(function () {
  'use strict';

  const SITE = window.SITE;
  if (!SITE) return;
  const C = SITE.contacts || {};

  /* ---------- helpers ---------- */
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));
  const attr = (v) => String(v ?? '').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
  const strip = (v) => String(v ?? '').replace(/<[^>]*>/g, '');
  const list = (v) => (Array.isArray(v) ? v : v ? [v] : []);
  const pad = (n) => String(n).padStart(2, '0');

  const igUrl = () => (C.instagram ? `https://instagram.com/${C.instagram}` : '');
  const igDm = () => (C.instagram ? `https://ig.me/m/${C.instagram}` : '');
  const waUrl = (text) =>
    C.whatsapp ? `https://wa.me/${String(C.whatsapp).replace(/\D/g, '')}${text ? `?text=${encodeURIComponent(text)}` : ''}` : '';
  const orderText = (item) => (SITE.orderMessage || '{item}').replace('{item}', item);

  /* href в content.js может быть: '#якорь', ссылкой, 'instagram', 'whatsapp' или 'order:Название' */
  function link(href) {
    if (!href) return { href: '#' };
    if (href === 'instagram') return { href: igUrl(), ext: true };
    if (href === 'whatsapp') return { href: waUrl() || igDm(), ext: true };
    if (href.startsWith('order:')) return { href: waUrl(orderText(href.slice(6))) || igDm(), ext: true, order: href.slice(6) };
    return { href, ext: /^https?:/.test(href) };
  }
  function button(b, extra = '') {
    const l = link(b.href);
    const cls = b.style === 'ghost' ? 'btn btn--ghost' : b.style === 'light' ? 'btn btn--light' : 'btn';
    return `<a class="${cls} ${extra}" href="${attr(l.href)}"${l.ext ? ' target="_blank" rel="noopener"' : ''}${
      l.order ? ` data-order="${attr(l.order)}"` : ''
    }>${b.label}</a>`;
  }
  function img(src, alt, opts = {}) {
    const { cls = '', eager = false, pos = '', posMobile = '' } = opts;
    const style = [pos && `--pos:${pos}`, posMobile && `--pos-m:${posMobile}`].filter(Boolean).join(';');
    return `<img class="${cls}" src="${attr(src)}" alt="${attr(alt || '')}" ${
      eager ? 'fetchpriority="high"' : 'loading="lazy"'
    } decoding="async"${style ? ` style="${attr(style)}"` : ''}>`;
  }
  let counter = 0;
  function head(s, opts = {}) {
    const num = opts.num === false ? '' : `<span class="eyebrow__num">${pad(++counter)}</span>`;
    return `
      <div class="head ${opts.center ? 'head--center' : ''}" data-reveal>
        ${s.eyebrow ? `<p class="eyebrow">${num}${s.eyebrow}</p>` : ''}
        ${s.title ? `<h2 class="title">${s.title}</h2>` : ''}
        ${s.text && opts.text !== false ? `<p class="lead">${s.text}</p>` : ''}
      </div>`;
  }

  /* ---------- icons ---------- */
  const I = {
    instagram: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r=".6" fill="currentColor"/></svg>',
    whatsapp: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3.5 20.5l1.3-4.2A8.5 8.5 0 1 1 8 19.3z"/><path d="M9 8.5c.3 2.7 3.6 6 6.5 6.5l1-1.3-1.8-1-1 .8c-1-.4-2.3-1.7-2.7-2.7l.8-1-1-1.8z" stroke-width="1.1"/></svg>',
    phone: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h3.5l1.5 4-2 1.3a10 10 0 0 0 6.7 6.7L16 14l4 1.5V19a1.5 1.5 0 0 1-1.6 1.5A16 16 0 0 1 3.5 5.6 1.5 1.5 0 0 1 5 4z"/></svg>',
    mail: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="M3.5 6l8.5 7 8.5-7"/></svg>',
    pin: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-6.5-6-6.5-11a6.5 6.5 0 0 1 13 0c0 5-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/></svg>',
    clock: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></svg>',
    arrow: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M14 7l5 5-5 5"/></svg>',
    table: '<svg viewBox="0 0 48 48" aria-hidden="true"><ellipse cx="24" cy="26" rx="17" ry="9"/><ellipse cx="24" cy="25" rx="9" ry="4.5"/><path d="M5 18v14M43 18v14M3 18h4M41 18h4"/></svg>',
    gift: '<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="8" y="18" width="32" height="24"/><rect x="5" y="12" width="38" height="7"/><path d="M24 12v30M24 12c-3-7-11-7-10-2s10 2 10 2zM24 12c3-7 11-7 10-2s-10 2-10 2z"/></svg>',
    truck: '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M3 12h26v22H3zM29 19h9l7 8v7H29z"/><circle cx="12" cy="36" r="4"/><circle cx="36" cy="36" r="4"/></svg>',
    chat: '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M6 9h36v24H20l-9 7v-7H6z"/><path d="M14 18h20M14 24h13"/></svg>',
    close: '&times;',
  };

  /* ---------- section renderers ---------- */
  const sections = {
    hero(s) {
      const slides = list(s.slides);
      return `
      <section class="hero" id="${attr(s.id)}" aria-label="Главный экран">
        <div class="hero__media">
          ${slides
            .map(
              (sl, i) =>
                `<div class="hero__slide ${i === 0 ? 'is-active' : ''}">${img(sl.image, sl.alt, { eager: i === 0, pos: sl.focus, posMobile: sl.focusMobile })}</div>`
            )
            .join('')}
        </div>
        <div class="hero__veil"></div>
        <div class="hero__content container">
          <div class="hero__copy">
            ${s.eyebrow ? `<p class="eyebrow eyebrow--hero">${s.eyebrow}</p>` : ''}
            <h1 class="hero__title">${s.title || ''}</h1>
            <span class="rule"></span>
            ${s.text ? `<p class="hero__text">${s.text}</p>` : ''}
            <div class="btn-row">${list(s.buttons).map((b) => button(b)).join('')}</div>
          </div>
        </div>
        ${
          slides.length > 1
            ? `<div class="hero__counter" aria-hidden="true"><span class="hero__current">01</span> / ${pad(slides.length)}</div>`
            : ''
        }
        <a class="hero__scroll" href="#main-next" aria-label="Листать вниз"><span></span></a>
      </section>`;
    },

    intro(s) {
      return `
      <section class="section intro" id="${attr(s.id)}">
        <div class="container intro__grid">
          ${head({ ...s, text: '' })}
          <div class="intro__body" data-reveal>
            ${list(s.text).map((p) => `<p>${p}</p>`).join('')}
            ${
              s.stats
                ? `<dl class="stats">${s.stats
                    .map((st) => `<div class="stat"><dt>${st.value}</dt><dd>${st.label}</dd></div>`)
                    .join('')}</dl>`
                : ''
            }
          </div>
        </div>
      </section>`;
    },

    collections(s) {
      return `
      <section class="section collections" id="${attr(s.id)}">
        <div class="container">
          ${head(s, { center: true })}
          ${list(s.items)
            .map(
              (c, i) => `
            <article class="collection ${i % 2 ? 'collection--rev' : ''}">
              <div class="collection__media" data-reveal>${img(c.image, c.alt || c.name)}</div>
              <div class="collection__body" data-reveal>
                <span class="collection__index">${pad(i + 1)}</span>
                <p class="eyebrow">${c.subtitle || ''}</p>
                <h3 class="collection__name">${c.name}</h3>
                <span class="rule"></span>
                <p>${c.text || ''}</p>
                <a class="link-arrow" href="#catalog" data-filter="${attr(c.filter || c.name)}">Смотреть коллекцию ${I.arrow}</a>
              </div>
            </article>`
            )
            .join('')}
        </div>
      </section>`;
    },

    features(s) {
      return `
      <section class="section section--alt features" id="${attr(s.id)}">
        <div class="container features__grid">
          <div class="features__media" data-reveal>${img(s.image, s.alt)}</div>
          <div class="features__body">
            ${head(s)}
            <ol class="features__list">
              ${list(s.items)
                .map(
                  (f, i) => `
                <li class="feature" data-reveal>
                  <span class="feature__num">${pad(i + 1)}</span>
                  <div><h3>${f.title}</h3><p>${f.text}</p></div>
                </li>`
                )
                .join('')}
            </ol>
          </div>
        </div>
      </section>`;
    },

    banner(s) {
      return `
      <section class="banner" id="${attr(s.id)}">
        ${img(s.image, s.alt, { cls: 'banner__img' })}
        <div class="banner__veil"></div>
        <div class="banner__content container" data-reveal>
          ${s.eyebrow ? `<p class="eyebrow eyebrow--light">${s.eyebrow}</p>` : ''}
          <h2 class="banner__title">${s.title || ''}</h2>
          <span class="rule"></span>
          ${s.text ? `<p class="banner__text">${s.text}</p>` : ''}
          ${s.button ? button({ ...s.button, style: 'light' }) : ''}
        </div>
      </section>`;
    },

    catalog(s) {
      const items = list(s.items);
      const cols = [...new Set(items.map((p) => p.collection).filter(Boolean))];
      catalogItems = items;
      return `
      <section class="section catalog" id="${attr(s.id)}">
        <div class="container">
          ${head(s, { center: true })}
          ${
            s.filters && cols.length > 1
              ? `<div class="filters" role="group" aria-label="Фильтр по коллекциям" data-reveal>
                  <button class="chip is-active" data-chip="*">Все</button>
                  ${cols.map((c) => `<button class="chip" data-chip="${attr(c)}">${c}</button>`).join('')}
                </div>`
              : ''
          }
          <div class="grid-products">
            ${items
              .map(
                (p, i) => `
              <article class="product" data-collection="${attr(p.collection)}" data-reveal>
                <button class="product__media" data-product="${i}" aria-label="Подробнее: ${attr(strip(p.name))}">
                  ${img(p.image, p.name)}
                  ${p.badge ? `<span class="badge">${p.badge}</span>` : ''}
                  <span class="product__more">Подробнее</span>
                </button>
                <div class="product__info">
                  ${p.collection ? `<p class="product__col">${p.collection}</p>` : ''}
                  <h3 class="product__name">${p.name}</h3>
                  <div class="product__foot">
                    <span class="price">${p.price || ''}</span>
                    <a class="link-arrow" href="${attr(link('order:' + strip(p.name)).href)}" target="_blank" rel="noopener" data-order="${attr(
                      strip(p.name)
                    )}">Заказать ${I.arrow}</a>
                  </div>
                </div>
              </article>`
              )
              .join('')}
          </div>
        </div>
      </section>`;
    },

    gallery(s) {
      galleryItems = list(s.images);
      return `
      <section class="section section--alt gallery" id="${attr(s.id)}">
        <div class="container">
          ${head(s, { center: true })}
          <div class="masonry">
            ${galleryItems
              .map(
                (g, i) => `
              <button class="masonry__item ${g.size ? 'is-' + g.size : ''}" data-gallery="${i}" aria-label="Открыть фото: ${attr(g.alt)}" data-reveal>
                ${img(g.src, g.alt)}
              </button>`
              )
              .join('')}
          </div>
        </div>
      </section>`;
    },

    services(s) {
      return `
      <section class="section services" id="${attr(s.id)}">
        <div class="container">
          ${head(s, { center: true })}
          <div class="services__grid">
            ${list(s.items)
              .map(
                (it) => `
              <div class="service" data-reveal>
                <span class="service__icon">${I[it.icon] || ''}</span>
                <h3>${it.title}</h3>
                <p>${it.text}</p>
              </div>`
              )
              .join('')}
          </div>
        </div>
      </section>`;
    },

    instagram(s) {
      if (!C.instagram) return '';
      return `
      <section class="section insta" id="${attr(s.id)}">
        <div class="container">
          ${head(s, { center: true })}
          <a class="insta__handle" href="${igUrl()}" target="_blank" rel="noopener" data-reveal>@${C.instagram}</a>
          <div class="insta__grid">
            ${list(s.images)
              .map(
                (src) => `<a class="insta__item" href="${igUrl()}" target="_blank" rel="noopener" aria-label="Открыть Instagram" data-reveal>
                    ${img(src, '')}<span class="insta__hover">${I.instagram}</span></a>`
              )
              .join('')}
          </div>
          <div class="btn-row btn-row--center" data-reveal>
            <a class="btn" href="${igUrl()}" target="_blank" rel="noopener">Подписаться</a>
          </div>
        </div>
      </section>`;
    },

    contact(s) {
      const rows = [];
      if (C.address || C.city)
        rows.push([I.pin, 'Адрес', [C.city, C.address].filter(Boolean).join(', '), C.mapUrl]);
      if (C.hours) rows.push([I.clock, 'Часы работы', C.hours]);
      if (C.phone) rows.push([I.phone, 'Телефон', C.phone, `tel:${C.phone.replace(/[^\d+]/g, '')}`]);
      if (C.whatsapp) rows.push([I.whatsapp, 'WhatsApp', 'Написать в WhatsApp', waUrl()]);
      if (C.instagram) rows.push([I.instagram, 'Instagram', '@' + C.instagram, igUrl()]);
      if (C.email) rows.push([I.mail, 'E-mail', C.email, `mailto:${C.email}`]);
      return `
      <section class="section section--alt contact" id="${attr(s.id)}">
        <div class="container contact__grid">
          <div class="contact__body">
            ${head(s)}
            <ul class="contact__list" data-reveal>
              ${rows
                .map(
                  ([ic, label, val, href]) => `
                <li><span class="contact__icon">${ic}</span>
                  <div><span class="contact__label">${label}</span>
                  ${
                    href
                      ? `<a href="${attr(href)}"${/^https?:/.test(href) ? ' target="_blank" rel="noopener"' : ''}>${val}</a>`
                      : `<span>${val}</span>`
                  }</div></li>`
                )
                .join('')}
            </ul>
            <div class="btn-row" data-reveal>
              ${C.whatsapp ? `<a class="btn" href="${waUrl()}" target="_blank" rel="noopener">Написать в WhatsApp</a>` : ''}
              ${C.instagram ? `<a class="btn ${C.whatsapp ? 'btn--ghost' : ''}" href="${igDm()}" target="_blank" rel="noopener">Написать в Direct</a>` : ''}
            </div>
          </div>
          ${s.image ? `<div class="contact__media" data-reveal>${img(s.image, s.alt)}</div>` : ''}
        </div>
        ${
          s.map && C.address
            ? `<div class="container"><div class="contact__map" data-reveal>
                <iframe src="https://maps.google.com/maps?q=${encodeURIComponent(
                  [C.city, C.address].filter(Boolean).join(', ')
                )}&z=16&output=embed" loading="lazy" title="Карта: ${attr(C.address)}" referrerpolicy="no-referrer-when-downgrade"></iframe>
              </div></div>`
            : ''
        }
      </section>`;
    },

    html(s) {
      return s.html || '';
    },
  };

  let catalogItems = [];
  let galleryItems = [];

  /* ---------- build page ---------- */
  function build() {
    const main = $('#main');
    const visible = list(SITE.sections).filter((s) => !s.hidden);
    main.innerHTML = visible
      .map((s, i) => {
        const r = sections[s.type];
        if (!r) {
          console.warn('Неизвестный тип секции:', s.type);
          return '';
        }
        const html = r(s);
        // якорь для стрелки «листать вниз» — первая секция после hero
        return i === 1 ? `<div id="main-next"></div>${html}` : html;
      })
      .join('');

    // навигация
    const navHtml = list(SITE.nav).map((n) => `<a href="${attr(n.href)}">${n.label}</a>`).join('');
    $('#nav').innerHTML = navHtml;
    $('#mobile-menu').innerHTML = `
      <nav class="mobile-menu__nav" aria-label="Мобильное меню">${navHtml}</nav>
      <div class="mobile-menu__foot">
        ${C.instagram ? `<a href="${igUrl()}" target="_blank" rel="noopener">${I.instagram}<span>@${C.instagram}</span></a>` : ''}
        ${C.whatsapp ? `<a href="${waUrl()}" target="_blank" rel="noopener">${I.whatsapp}<span>WhatsApp</span></a>` : ''}
      </div>`;
    $$('[data-instagram]').forEach((a) => {
      if (C.instagram) {
        a.href = igUrl();
        a.innerHTML = I.instagram;
      } else a.remove();
    });

    // футер
    const year = new Date().getFullYear();
    $('#footer').innerHTML = `
      <div class="container footer__inner">
        <div class="footer__brand">
          <a class="logo logo--footer" href="#top">${SITE.brand.name}</a>
          <span class="rule"></span>
          <p class="eyebrow">${SITE.brand.tagline || ''}</p>
          ${SITE.footer && SITE.footer.text ? `<p class="footer__text">${SITE.footer.text}</p>` : ''}
        </div>
        <nav class="footer__nav" aria-label="Меню в подвале">${navHtml}</nav>
        <div class="footer__contacts">
          ${C.instagram ? `<a href="${igUrl()}" target="_blank" rel="noopener">${I.instagram} @${C.instagram}</a>` : ''}
          ${C.whatsapp ? `<a href="${waUrl()}" target="_blank" rel="noopener">${I.whatsapp} WhatsApp</a>` : ''}
          ${C.phone ? `<a href="tel:${attr(C.phone.replace(/[^\d+]/g, ''))}">${I.phone} ${C.phone}</a>` : ''}
          ${C.address ? `<span>${I.pin} ${[C.city, C.address].filter(Boolean).join(', ')}</span>` : ''}
        </div>
      </div>
      <div class="container footer__bottom">
        <span>© ${year} ${SITE.brand.name}</span>
        <span>Фарфор · Сервировка · Подарки</span>
      </div>`;

    // плавающая кнопка «Написать»
    const fabHref = waUrl() || igDm();
    if (fabHref) {
      const fab = document.createElement('a');
      fab.className = 'fab';
      fab.href = fabHref;
      fab.target = '_blank';
      fab.rel = 'noopener';
      fab.innerHTML = `${C.whatsapp ? I.whatsapp : I.instagram}<span>Написать</span>`;
      document.body.appendChild(fab);
    }

    // структурированные данные для поисковиков
    const ld = {
      '@context': 'https://schema.org',
      '@type': 'Store',
      name: SITE.brand.name,
      description: SITE.brand.description,
      image: new URL('assets/img/og-image.jpg', location.href).href,
      sameAs: C.instagram ? [igUrl()] : undefined,
      telephone: C.phone || undefined,
      address: C.address ? { '@type': 'PostalAddress', streetAddress: C.address, addressLocality: C.city || undefined } : undefined,
    };
    const sc = document.createElement('script');
    sc.type = 'application/ld+json';
    sc.textContent = JSON.stringify(ld);
    document.head.appendChild(sc);
  }

  /* ---------- behaviour ---------- */
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function initHeader() {
    const header = $('#header');
    const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 40);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    const burger = $('#burger');
    const menu = $('#mobile-menu');
    const toggle = (open) => {
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
      document.body.classList.toggle('menu-open', open);
      if (open) {
        menu.hidden = false;
        requestAnimationFrame(() => menu.classList.add('is-open'));
      } else {
        menu.classList.remove('is-open');
        setTimeout(() => (menu.hidden = true), 400);
      }
    };
    burger.addEventListener('click', () => toggle(burger.getAttribute('aria-expanded') !== 'true'));
    menu.addEventListener('click', (e) => e.target.closest('a') && toggle(false));
    document.addEventListener('keydown', (e) => e.key === 'Escape' && document.body.classList.contains('menu-open') && toggle(false));
  }

  function initReveal() {
    const els = $$('[data-reveal]');
    if (reduceMotion || !('IntersectionObserver' in window)) {
      els.forEach((el) => el.classList.add('is-in'));
      return;
    }
    const io = new IntersectionObserver(
      (entries) =>
        entries.forEach((en) => {
          if (en.isIntersecting) {
            en.target.classList.add('is-in');
            io.unobserve(en.target);
          }
        }),
      { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
    );
    els.forEach((el) => io.observe(el));
  }

  function initHero() {
    const slides = $$('.hero__slide');
    const cur = $('.hero__current');
    if (slides.length < 2) return;
    let i = 0;
    setInterval(() => {
      slides[i].classList.remove('is-active');
      i = (i + 1) % slides.length;
      slides[i].classList.add('is-active');
      if (cur) cur.textContent = pad(i + 1);
    }, 6500);
  }

  function initCatalog() {
    const chips = $$('[data-chip]');
    const apply = (val) => {
      chips.forEach((c) => c.classList.toggle('is-active', c.dataset.chip === val));
      $$('.product').forEach((p) => {
        const show = val === '*' || p.dataset.collection === val;
        p.hidden = !show;
        if (show) p.classList.add('is-in');
      });
    };
    chips.forEach((c) => c.addEventListener('click', () => apply(c.dataset.chip)));
    // «Смотреть коллекцию» → фильтр каталога
    $$('[data-filter]').forEach((a) =>
      a.addEventListener('click', () => {
        const val = a.dataset.filter;
        if (chips.some((c) => c.dataset.chip === val)) apply(val);
      })
    );
  }

  /* ---------- modal: product / gallery ---------- */
  const modal = $('#modal');
  const body = $('#modal-body');
  let galleryIndex = 0;

  function openModal(html, kind) {
    body.innerHTML = html;
    modal.dataset.kind = kind;
    if (typeof modal.showModal === 'function') modal.showModal();
    else modal.setAttribute('open', '');
    document.body.classList.add('modal-open');
  }
  function closeModal() {
    if (modal.open && typeof modal.close === 'function') modal.close();
    else modal.removeAttribute('open');
  }
  modal.addEventListener('close', () => document.body.classList.remove('modal-open'));
  modal.addEventListener('click', (e) => {
    if (e.target === modal || e.target.closest('[data-close]')) closeModal();
  });

  function productHtml(p) {
    const name = strip(p.name);
    return `
      <div class="pmodal">
        <div class="pmodal__media">${img(p.image, p.name)}</div>
        <div class="pmodal__info">
          ${p.collection ? `<p class="eyebrow">${p.collection}</p>` : ''}
          <h3 class="pmodal__name">${p.name}</h3>
          <span class="rule"></span>
          ${p.text ? `<p>${p.text}</p>` : ''}
          ${p.details ? `<ul class="pmodal__details">${p.details.map((d) => `<li>${d}</li>`).join('')}</ul>` : ''}
          ${p.price ? `<p class="price price--lg">${p.price}</p>` : ''}
          <div class="btn-row">
            <a class="btn" href="${attr(link('order:' + name).href)}" target="_blank" rel="noopener" data-order="${attr(name)}">Заказать</a>
            ${C.instagram ? `<a class="btn btn--ghost" href="${igUrl()}" target="_blank" rel="noopener">Больше фото</a>` : ''}
          </div>
        </div>
      </div>`;
  }
  function galleryHtml(i) {
    const g = galleryItems[i];
    return `
      <figure class="lightbox">
        <img src="${attr(g.src)}" alt="${attr(g.alt)}">
        ${g.alt ? `<figcaption>${g.alt}</figcaption>` : ''}
      </figure>
      ${
        galleryItems.length > 1
          ? `<button class="lightbox__nav lightbox__nav--prev" data-step="-1" aria-label="Предыдущее фото">${I.arrow}</button>
             <button class="lightbox__nav lightbox__nav--next" data-step="1" aria-label="Следующее фото">${I.arrow}</button>`
          : ''
      }`;
  }
  function stepGallery(d) {
    galleryIndex = (galleryIndex + d + galleryItems.length) % galleryItems.length;
    body.innerHTML = galleryHtml(galleryIndex);
  }

  /* ---------- order: WhatsApp с готовым текстом или Instagram Direct ---------- */
  let toastTimer;
  function toast(msg) {
    let t = $('.toast');
    if (!t) {
      t = document.createElement('div');
      t.className = 'toast';
      t.setAttribute('role', 'status');
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.classList.add('is-on');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => t.classList.remove('is-on'), 4200);
  }

  document.addEventListener('click', (e) => {
    const prod = e.target.closest('[data-product]');
    if (prod) return openModal(productHtml(catalogItems[+prod.dataset.product]), 'product');

    const gal = e.target.closest('[data-gallery]');
    if (gal) {
      galleryIndex = +gal.dataset.gallery;
      return openModal(galleryHtml(galleryIndex), 'gallery');
    }
    const step = e.target.closest('[data-step]');
    if (step) return stepGallery(+step.dataset.step);

    const order = e.target.closest('[data-order]');
    if (order && !C.whatsapp && C.instagram) {
      // В Instagram нельзя передать текст сообщения — копируем его в буфер
      const text = orderText(order.dataset.order);
      if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(
          () => toast('Текст сообщения скопирован — вставьте его в Direct'),
          () => {}
        );
      }
    }
  });
  document.addEventListener('keydown', (e) => {
    if (!modal.open || modal.dataset.kind !== 'gallery') return;
    if (e.key === 'ArrowRight') stepGallery(1);
    if (e.key === 'ArrowLeft') stepGallery(-1);
  });

  /* ---------- go ---------- */
  build();
  initHeader();
  initReveal();
  initHero();
  initCatalog();
})();
