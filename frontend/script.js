// ---- Basic configuration ----
// If your backend is running on a different origin (e.g. http://localhost:8000),
// update BASE_URL accordingly. When serving this frontend via the same host/port
// as the FastAPI app, you can leave this as an empty string.
const BASE_URL = "";

const ENDPOINTS = {
  root: "/",
  seats: "/seats/",
  bookings: "/bookings",
  bookingsCreate: "/bookings/",
  bookingsCancel: "/bookings/cancel",
  prediction: "/prediction/waitlist-confirmation",
};

// ---- Helper functions ----

async function apiFetch(path, options = {}) {
  const url = BASE_URL + path;
  const defaultHeaders = {
    "Content-Type": "application/json",
  };

  const opts = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...(options.headers || {}),
    },
  };

  const res = await fetch(url, opts);
  let data = null;

  try {
    data = await res.json();
  } catch {
    // ignore JSON parse errors for non-JSON responses
  }

  if (!res.ok) {
    const detail = data && (data.detail || data.message);
    const message =
      typeof detail === "string"
        ? detail
        : Array.isArray(detail)
        ? detail.map((d) => d.msg || d).join("; ")
        : `Request failed (${res.status})`;
    const error = new Error(message);
    error.status = res.status;
    error.data = data;
    throw error;
  }

  return data;
}

function qs(id) {
  return document.getElementById(id);
}

function setHidden(el, hidden) {
  if (!el) return;
  el.classList.toggle("hidden", hidden);
}

function formatDate(dateStr) {
  if (!dateStr) return "";
  const d = new Date(dateStr);
  if (Number.isNaN(d.getTime())) return dateStr;
  return d.toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

function escapeHtml(value) {
  const str = value == null ? "" : String(value);
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

// ---- Navigation ----

function setupNavigation() {
  const buttons = document.querySelectorAll(".nav-btn");
  const panels = document.querySelectorAll(".panel");

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const target = btn.getAttribute("data-target");

      buttons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      panels.forEach((panel) => {
        panel.classList.toggle("active", panel.id === target);
      });
    });
  });
}

// ---- Initial load: stations & health ----

async function initApp() {
  setupNavigation();

  const statusEl = qs("api-status");
  const footerMeta = qs("footer-meta");

  try {
    const meta = await apiFetch(ENDPOINTS.root);

    statusEl.textContent = "API connected";
    statusEl.classList.remove("error");
    statusEl.classList.add("ok");

    if (meta && meta.stations) {
      populateStationSelects(meta.stations);
    }
    if (meta && meta.pricing && typeof meta.pricing.meal_price === "number") {
      footerMeta.textContent = `Meal price: ₹${meta.pricing.meal_price}`;
    }

    // pre-fill dates with today
    const today = new Date().toISOString().slice(0, 10);
    ["travel-date", "booking-date", "filter-date"].forEach((id) => {
      const el = qs(id);
      if (el && !el.value) {
        el.value = today;
      }
    });
  } catch (err) {
    console.error(err);
    statusEl.textContent = "API unreachable";
    statusEl.classList.remove("ok");
    statusEl.classList.add("error");
  }

  setupSeatsFlow();
  setupBookingFlow();
  setupBookingsList();
  setupCancelFlow();
  setupPredictionFlow();
}

function populateStationSelect(select, stations) {
  select.innerHTML = "";
  const placeholder = document.createElement("option");
  placeholder.value = "";
  placeholder.textContent = "Select";
  select.appendChild(placeholder);
  stations.forEach((st) => {
    const opt = document.createElement("option");
    opt.value = st;
    opt.textContent = st;
    select.appendChild(opt);
  });
}

function populateStationSelects(stations) {
  const ids = [
    "source",
    "destination",
    "booking-source",
    "booking-destination",
    "prediction-source",
    "prediction-destination",
  ];

  ids.forEach((id) => {
    const el = qs(id);
    if (el) populateStationSelect(el, stations);
  });
}

// ---- Seats & route ----

const selectedSeats = new Set();

function setupSeatsFlow() {
  const form = qs("seats-form");
  const listEl = qs("seats-list");
  const resultsWrapper = qs("seats-results");
  const emptyEl = qs("seats-empty");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const source = qs("source").value;
    const destination = qs("destination").value;
    const travelDate = qs("travel-date").value;

    if (!source || !destination || !travelDate) return;

    setHidden(resultsWrapper, false);
      listEl.textContent = "Loading seats...";
    setHidden(emptyEl, true);

    const params = new URLSearchParams({
      source,
      destination,
      travel_date: travelDate,
    }).toString();

    try {
      const data = await apiFetch(`${ENDPOINTS.seats}?${params}`);

      listEl.innerHTML = "";
      selectedSeats.clear();
      syncSelectedSeatsToBookingInput();

      if (!data || !Array.isArray(data.seats) || data.seats.length === 0) {
        setHidden(emptyEl, false);
        return;
      }

      data.seats.forEach((seat) => {
        const card = document.createElement("div");
        card.className = "seat-card";
        card.dataset.id = String(seat.id);

        const idEl = document.createElement("div");
        idEl.className = "seat-id";
        idEl.textContent = escapeHtml(seat.id);

        const metaEl = document.createElement("div");
        metaEl.className = "seat-meta";

        const catEl = document.createElement("span");
        catEl.textContent = escapeHtml(seat.category ?? "Seat");

        const priceEl = document.createElement("span");
        priceEl.className = "seat-price";
        priceEl.textContent = `₹${seat.price}`;

        metaEl.appendChild(catEl);
        metaEl.appendChild(priceEl);
        card.appendChild(idEl);
        card.appendChild(metaEl);

        card.addEventListener("click", () => {
          const id = seat.id;
          if (selectedSeats.has(id)) {
            selectedSeats.delete(id);
            card.classList.remove("selected");
          } else {
            selectedSeats.add(id);
            card.classList.add("selected");
          }
          syncSelectedSeatsToBookingInput();
        });

        listEl.appendChild(card);
      });
    } catch (err) {
      console.error(err);
      listEl.textContent = `Error: ${escapeHtml(
        err.message || "Unable to fetch seats"
      )}`;
    }
  });
}

function syncSelectedSeatsToBookingInput() {
  const input = qs("booking-seat-ids");
  if (!input) return;
  input.value =
    selectedSeats.size === 0
      ? ""
      : Array.from(selectedSeats)
          .map((s) => String(s))
          .join(", ");

  // also sync route + date to booking form when available
  const src = qs("source").value;
  const dst = qs("destination").value;
  const date = qs("travel-date").value;
  if (src) qs("booking-source").value = src;
  if (dst) qs("booking-destination").value = dst;
  if (date) qs("booking-date").value = date;
}

// ---- Create booking ----

function setupBookingFlow() {
  const form = qs("booking-form");
  const resultEl = qs("booking-result");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    setHidden(resultEl, true);
    resultEl.classList.remove("error");
    resultEl.innerHTML = "";

    const seatIdsRaw = qs("booking-seat-ids").value || "";
    const seat_ids = seatIdsRaw
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);

    if (!seat_ids.length) {
      showResult(resultEl, "Please select at least one seat.", true);
      return;
    }

    const body = {
      seat_ids,
      passenger_name: qs("passenger-name").value.trim(),
      age: Number(qs("age").value),
      gender: qs("gender").value,
      phone: qs("phone").value.trim(),
      source: qs("booking-source").value,
      destination: qs("booking-destination").value,
      travel_date: qs("booking-date").value,
      num_meals: Number(qs("num-meals").value || 0),
      waitlist_position: qs("waitlist-position").value
        ? Number(qs("waitlist-position").value)
        : null,
    };

    try {
      const booking = await apiFetch(ENDPOINTS.bookingsCreate, {
        method: "POST",
        body: JSON.stringify(body),
      });

      showResult(
        resultEl,
        `Booking created successfully. ID: <strong>${booking.booking_id}</strong>, status: <strong>${booking.status}</strong>, total price: <strong>₹${booking.total_price}</strong>`,
        false
      );

      // refresh bookings list in background
      refreshBookingsList().catch(() => {});
    } catch (err) {
      console.error(err);
      showResult(resultEl, err.message || "Failed to create booking.", true);
    }
  });
}

function showResult(container, message, isError = false) {
  if (!container) return;
  container.classList.toggle("error", !!isError);
  container.innerHTML = "";

  const titleEl = document.createElement("div");
  titleEl.className = "result-title";
  titleEl.textContent = isError ? "Something went wrong" : "Success";

  const bodyEl = document.createElement("div");
  bodyEl.textContent = message;

  container.appendChild(titleEl);
  container.appendChild(bodyEl);
  setHidden(container, false);
}

// ---- List bookings ----

function setupBookingsList() {
  const form = qs("filter-bookings-form");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    refreshBookingsList();
  });

  // initial load
  refreshBookingsList().catch(() => {});
}

async function refreshBookingsList() {
  const listEl = qs("bookings-list");
  const emptyEl = qs("bookings-empty");

  listEl.textContent = "Loading bookings...";
  setHidden(emptyEl, true);

  const date = qs("filter-date").value;
  const status = qs("filter-status").value;

  const params = new URLSearchParams();
  if (date) params.set("travel_date", date);
  if (status) params.set("status", status);

  const query = params.toString();

  try {
    const data = await apiFetch(
      `${ENDPOINTS.bookings}${query ? `?${query}` : ""}`
    );
    listEl.innerHTML = "";

    if (!Array.isArray(data) || data.length === 0) {
      setHidden(emptyEl, false);
      return;
    }

    data.forEach((b) => {
      const card = document.createElement("div");
      card.className = "booking-card";

      const main = document.createElement("div");
      main.className = "booking-main";

      const title = document.createElement("div");
      title.className = "booking-title";
      title.textContent = escapeHtml(b.passenger_name);

      const sub = document.createElement("div");
      sub.className = "booking-sub";
      const seatList = (b.seat_ids || "").split(",").join(", ") || "N/A";
      sub.textContent = `${escapeHtml(b.booking_id)} · Seats: ${escapeHtml(
        seatList
      )}`;

      main.appendChild(title);
      main.appendChild(sub);

      const metaLeft = document.createElement("div");
      metaLeft.className = "booking-meta";

      const route = document.createElement("div");
      route.textContent = `${escapeHtml(b.source)} → ${escapeHtml(
        b.destination
      )}`;

      const dateEl = document.createElement("div");
      dateEl.textContent = formatDate(b.travel_date);

      const extra = document.createElement("div");
      extra.className = "booking-extra";
      const meals = b.num_meals ?? 0;
      const wl =
        b.waitlist_position != null ? ` · WL: ${b.waitlist_position}` : "";
      extra.textContent = `Meals: ${meals}${wl}`;

      metaLeft.appendChild(route);
      metaLeft.appendChild(dateEl);
      metaLeft.appendChild(extra);

      const metaRight = document.createElement("div");
      metaRight.className = "booking-meta";

      const price = document.createElement("div");
      price.className = "booking-price";
      price.textContent = `₹${b.total_price ?? "—"}`;

      const badge = document.createElement("span");
      badge.className = `badge status-${escapeHtml(b.status)}`;
      badge.textContent = escapeHtml(b.status);

      metaRight.appendChild(price);
      metaRight.appendChild(badge);

      card.appendChild(main);
      card.appendChild(metaLeft);
      card.appendChild(metaRight);

      card.addEventListener("click", () => {
        const target = qs("cancel-booking-id");
        if (target) {
          target.value = b.booking_id;
          target.focus();
        }
      });

      listEl.appendChild(card);
    });
  } catch (err) {
    console.error(err);
    listEl.textContent = `Error: ${escapeHtml(
      err.message || "Unable to load bookings"
    )}`;
  }
}

// ---- Cancel booking ----

function setupCancelFlow() {
  const form = qs("cancel-form");
  const resultEl = qs("cancel-result");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    setHidden(resultEl, true);
    resultEl.classList.remove("error");

    const bookingId = qs("cancel-booking-id").value.trim();
    if (!bookingId) return;

    try {
      const res = await apiFetch(ENDPOINTS.bookingsCancel, {
        method: "POST",
        body: JSON.stringify({ booking_id: bookingId }),
      });

      showResult(
        resultEl,
        `Booking <strong>${res.booking_id}</strong> cancelled successfully.`,
        false
      );
      refreshBookingsList().catch(() => {});
    } catch (err) {
      console.error(err);
      showResult(resultEl, err.message || "Failed to cancel booking.", true);
    }
  });
}

// ---- Prediction ----

function setupPredictionFlow() {
  const form = qs("prediction-form");
  const resultEl = qs("prediction-result");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    setHidden(resultEl, true);
    resultEl.classList.remove("error");

    const body = {
      source: qs("prediction-source").value,
      destination: qs("prediction-destination").value,
      days_before_travel: Number(qs("days-before-travel").value),
      waitlist_position: Number(qs("prediction-waitlist-position").value),
    };

    try {
      const res = await apiFetch(ENDPOINTS.prediction, {
        method: "POST",
        body: JSON.stringify(body),
      });

      const prob = res.confirmation_probability || `${res.probability_value ?? ""}%`;

      const confidence = res.confidence_score
        ? res.confidence_score
        : res.details && res.details.confidence_score
        ? res.details.confidence_score
        : "";

      const detailsObj =
        res.details && typeof res.details === "object" ? res.details : null;

      resultEl.innerHTML = "";

      const main = document.createElement("div");
      main.className = "prediction-main";
      main.textContent = escapeHtml(prob);

      const confEl = document.createElement("div");
      confEl.className = "prediction-conf";
      confEl.textContent = confidence ? `Confidence: ${escapeHtml(confidence)}` : "";

      resultEl.appendChild(main);
      resultEl.appendChild(confEl);

      if (detailsObj) {
        const title = document.createElement("div");
        title.className = "result-title";
        title.textContent = "Details";

        const detailsEl = document.createElement("div");
        detailsEl.style.fontSize = "12px";

        Object.entries(detailsObj).forEach(([k, v]) => {
          const line = document.createElement("div");
          line.textContent = `${k}: ${v}`;
          detailsEl.appendChild(line);
        });

        resultEl.appendChild(title);
        resultEl.appendChild(detailsEl);
      }
      setHidden(resultEl, false);
    } catch (err) {
      console.error(err);
      showResult(resultEl, err.message || "Failed to get prediction.", true);
    }
  });
}

// ---- Boot ----

document.addEventListener("DOMContentLoaded", initApp);

