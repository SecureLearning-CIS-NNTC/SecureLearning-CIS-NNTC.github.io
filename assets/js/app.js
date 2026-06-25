(function () {
  const data = window.SiteData;
  const pageId = document.body.dataset.page || "home";
  const current = data.pages[pageId] || data.pages.home;
  const root = document.getElementById("content");
  const depth = Number(document.body.dataset.depth || 0);
  const prefix = depth === 0 ? "" : "../".repeat(depth);

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function pathFor(href) {
    if (/^https?:|^mailto:/.test(href)) return href;
    return prefix + href.replace(/^\.\//, "");
  }

  function linkList(links) {
    if (!links || !links.length) return "";
    return `<div class="link-row">${links.map((link) =>
      `<a href="${escapeHtml(pathFor(link.href))}" ${/^https?:/.test(link.href) ? 'target="_blank" rel="noopener"' : ""}>${escapeHtml(link.label)}</a>`
    ).join("")}</div>`;
  }

  function personLine(person) {
    const email = person.email ? ` <a href="mailto:${escapeHtml(person.email)}">${escapeHtml(person.email)}</a>` : "";
    return `<li><strong>${escapeHtml(person.name)}</strong><span>${escapeHtml(person.affiliation || "")}${email}</span></li>`;
  }

  function renderNav() {
    const nav = document.getElementById("site-nav");
    nav.innerHTML = data.nav.map((item) => {
      const active = item.page === pageId ? "active" : "";
      return `<a class="${active}" href="${escapeHtml(pathFor(item.href))}">${escapeHtml(item.label)}</a>`;
    }).join("");
  }

  function renderHero() {
    document.title = `${current.title} | ${data.siteTitle}`;
    document.getElementById("hero-eyebrow").textContent = data.eyebrow;
    document.getElementById("hero-title").textContent = pageId === "home" ? data.title : current.title;
    document.getElementById("hero-summary").textContent = current.summary || data.title;
  }

  function renderPeople() {
    return `
      <section class="section">
        <h2>Task Force Leadership</h2>
        <div class="people-grid">
          <div>
            <h3>Task Force Chair</h3>
            <ul class="people-list">${data.people.chair.map(personLine).join("")}</ul>
          </div>
          <div>
            <h3>Task Force Vice-Chairs</h3>
            <ul class="people-list">${data.people.viceChairs.map(personLine).join("")}</ul>
          </div>
        </div>
      </section>
      <section class="section">
        <h2>Task Force Members</h2>
        <ul class="people-list columns">${data.people.members.map(personLine).join("")}</ul>
      </section>`;
  }

  function renderSection(section) {
    if (section.type === "people") return renderPeople();

    if (section.type === "rich") {
      const paragraphs = (section.paragraphs || []).map((p) => `<p>${escapeHtml(p)}</p>`).join("");
      const list = section.list ? `<ul>${section.list.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>` : "";
      return `<section class="section"><h2>${escapeHtml(section.title)}</h2>${paragraphs}${list}${linkList(section.links)}</section>`;
    }

    if (section.type === "news") {
      return `<section class="section"><h2>${escapeHtml(section.title)}</h2><div class="news-list">${section.items.map((item) => `
        <article class="news-item">
          <div class="date">${escapeHtml(item.date)}</div>
          <h3>${escapeHtml(item.title)}</h3>
          <p>${escapeHtml(item.text)} ${item.note ? `<span class="note">(${escapeHtml(item.note)})</span>` : ""}</p>
          ${linkList(item.links)}
        </article>`).join("")}</div></section>`;
    }

    if (section.type === "activityGroups") {
      return `<section class="section"><h2>${escapeHtml(section.title)}</h2><div class="activity-list">${section.groups.map((group) => `
        <article class="activity-group">
          <h3>${escapeHtml(group.title)}</h3>
          <ul>${(group.items || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
          ${linkList(group.links)}
        </article>`).join("")}</div></section>`;
    }

    if (section.type === "timeline") {
      return `<section class="section"><h2>${escapeHtml(section.title)}</h2><div class="timeline">${section.items.map((item) => `
        <div class="timeline-row"><strong>${escapeHtml(item[0])}</strong><span>${escapeHtml(item[1])}</span></div>`).join("")}</div></section>`;
    }

    if (section.type === "cards") {
      return `<section class="section"><h2>${escapeHtml(section.title)}</h2><div class="card-grid">${section.cards.map((card) => `
        <a class="card" href="${escapeHtml(pathFor(card.href))}">
          <h3>${escapeHtml(card.title)}</h3>
          <p>${escapeHtml(card.text)}</p>
        </a>`).join("")}</div></section>`;
    }

    if (section.type === "peopleList") {
      return `<section class="section"><h2>${escapeHtml(section.title)}</h2><ul class="people-list">${section.people.map(personLine).join("")}</ul></section>`;
    }

    return "";
  }

  renderNav();
  renderHero();
  root.innerHTML = current.sections.map(renderSection).join("");
  document.getElementById("source-link").href = data.sourceUrl;
})();
