const STATUS_LABELS = {
  operational: "Operational",
  degraded: "Degraded performance",
  partial: "Partial outage",
  outage: "Major outage"
};

const STATUS_DOT = {
  operational: "dot dot-ok",
  degraded: "dot dot-warn",
  partial: "dot dot-warn",
  outage: "dot dot-bad"
};

const IMPACT_CLS = {
  minor: "imp imp-minor",
  major: "imp imp-major",
  critical: "imp imp-critical",
  maintenance: "imp imp-maint"
};

const OVERALL_STATE = {
  operational: {
    cls: "ok",
    icon: "✓",
    title: "All systems operational"
  },
  partial_degradation: {
    cls: "warn",
    icon: "!",
    title: "Partial service degradation"
  },
  major_outage: {
    cls: "bad",
    icon: "✕",
    title: "Major service outage"
  }
};

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function timeAgo(iso) {
  const then = new Date(iso).getTime();
  const seconds = Math.max(0, Math.floor((Date.now() - then) / 1000));

  if (seconds < 60) {
    return `${seconds}s ago`;
  }

  if (seconds < 3600) {
    return `${Math.floor(seconds / 60)}m ago`;
  }

  if (seconds < 86400) {
    return `${Math.floor(seconds / 3600)}h ago`;
  }

  return `${Math.floor(seconds / 86400)}d ago`;
}

function shortDate(iso) {
  return new Date(iso).toLocaleString("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  });
}

function longDate(iso) {
  return new Date(iso).toLocaleDateString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric"
  });
}

async function api(path) {
  const response = await fetch(path, {
    headers: {
      "Accept": "application/json"
    }
  });

  if (!response.ok) {
    throw new Error(`${path} returned ${response.status}`);
  }

  return response.json();
}

function updateMainBanner(overall) {
  const state = OVERALL_STATE[overall] || OVERALL_STATE.operational;
  const updatedAt = new Date().toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit"
  });

  const banner = document.getElementById("current");
  banner.className = `banner banner-${state.cls}`;

  document.getElementById("overall-icon").textContent = state.icon;
  document.getElementById("overall-title").textContent = state.title;
  document.getElementById("overall-sub").textContent = `Updated ${updatedAt} · Next check in 30s`;
}

function drawComponents(components, uptimeSeries) {
  const root = document.getElementById("components-root");
  const uptimeByComponent = new Map();

  for (const item of uptimeSeries) {
    uptimeByComponent.set(item.component_id, item);
  }

  const groups = new Map();

  for (const component of components) {
    if (!groups.has(component.group)) {
      groups.set(component.group, []);
    }

    groups.get(component.group).push(component);
  }

  const markup = [];

  for (const [groupName, groupComponents] of groups) {
    const rows = [];

    for (const component of groupComponents) {
      const uptime = uptimeByComponent.get(component.id);
      const dotClass = STATUS_DOT[component.status] || STATUS_DOT.operational;
      const statusLabel = STATUS_LABELS[component.status] || component.status;

      let uptimeBar = "";

      if (uptime) {
        const days = uptime.days.map((day) => {
          const status = STATUS_LABELS[day.status] || day.status;
          const title = `${escapeHtml(day.date)} · ${escapeHtml(status)}`;

          return `<div class="uptime-day uptime-${escapeHtml(day.status)}" title="${title}"></div>`;
        }).join("");

        uptimeBar = `<div class="uptime-bar">${days}</div>`;
      }

      rows.push(`
        <div class="row">
          <div class="row-l">
            <span class="${dotClass}"></span>
            <span class="row-name">${escapeHtml(component.name)}</span>
          </div>
          <div class="row-m">${uptimeBar}</div>
          <div class="row-r">
            <span class="row-pct">${uptime ? escapeHtml(uptime.uptime_pct) + "%" : "—"}</span>
            <span class="row-status">${escapeHtml(statusLabel)}</span>
          </div>
        </div>
      `);
    }

    markup.push(`
      <div class="group">
        <div class="group-h">${escapeHtml(groupName)}</div>
        ${rows.join("")}
      </div>
    `);
  }

  root.innerHTML = markup.join("");
}

function drawIncidents(incidents) {
  const root = document.getElementById("incidents-root");

  if (!incidents.length) {
    root.innerHTML = `<div class="empty">No incidents reported.</div>`;
    return;
  }

  const incidentsByDay = new Map();

  for (const incident of incidents) {
    const day = incident.created_at.slice(0, 10);

    if (!incidentsByDay.has(day)) {
      incidentsByDay.set(day, []);
    }

    incidentsByDay.get(day).push(incident);
  }

  const sections = [];

  for (const [day, dayIncidents] of incidentsByDay) {
    const cards = [];

    for (const incident of dayIncidents) {
      const impactClass = IMPACT_CLS[incident.impact] || "imp";
      const resolvedText = incident.resolved_at
        ? ` · resolved ${escapeHtml(timeAgo(incident.resolved_at))}`
        : "";

      const updates = incident.updates.map((update) => `
        <li>
          <span class="update-label">${escapeHtml(update.label)}</span>
          <span class="update-body">${escapeHtml(update.body)}</span>
          <span class="update-ts mono">${escapeHtml(shortDate(update.ts))}</span>
        </li>
      `).join("");

      cards.push(`
        <article class="incident">
          <header class="incident-h">
            <div>
              <span class="${impactClass}">${escapeHtml(incident.impact)}</span>
              <span class="incident-title">${escapeHtml(incident.title)}</span>
            </div>
            <span class="incident-status">${escapeHtml(incident.status)}</span>
          </header>

          <ol class="updates">${updates}</ol>

          <footer class="incident-f mono">
            Incident #${escapeHtml(incident.id)} · opened ${escapeHtml(timeAgo(incident.created_at))}${resolvedText}
          </footer>
        </article>
      `);
    }

    sections.push(`
      <div class="day-group">
        <div class="day-label">${escapeHtml(longDate(day))}</div>
        ${cards.join("")}
      </div>
    `);
  }

  root.innerHTML = sections.join("");
}

function drawSubscribers(subscribers) {
  document.getElementById("subscribers-root").textContent =
    `${subscribers.email.toLocaleString()} email · ` +
    `${subscribers.webhook.toLocaleString()} webhook · ` +
    `${subscribers.rss.toLocaleString()} rss subscribers`;
}

function showLoadError() {
  document.getElementById("overall-title").textContent = "Unable to load status";
  document.getElementById("overall-sub").textContent = "Refresh the page or try again later.";

  document.getElementById("components-root").innerHTML =
    `<div class="empty">Could not load component status.</div>`;

  document.getElementById("incidents-root").innerHTML =
    `<div class="empty">Could not load incidents.</div>`;
}

async function boot() {
  try {
    const status = await api("/api/status");
    updateMainBanner(status.overall);

    const components = await api("/api/components");
    const uptime = await api("/api/uptime");
    drawComponents(components.components, uptime.series);

    const incidents = await api("/api/incidents?public=1");
    drawIncidents(incidents.incidents);

    const subscribers = await api("/api/subscribers/count");
    drawSubscribers(subscribers);
  } catch (error) {
    showLoadError();
  }
}

boot();