const API = "/api";
const PAGE_SIZE = 24;
const $ = id => document.getElementById(id);

let meta = { features: {} };
let carIndex = new Map();      // id -> car (all cars, never filtered)
let filteredCars = [];
let visibleCount = PAGE_SIZE;
let activeBody = "";

/* ---------------- Safe localStorage ---------------- */
const store = {
  get(key, fallback) {
    try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; }
  },
  set(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* storage unavailable */ }
  },
};
let selectedIds = store.get("carcompare_selected", []);
let savedComparisons = store.get("carcompare_saved", []);

/* ---------------- Helpers ---------------- */
function escapeHtml(value = "") {
  return String(value).replace(/[&<>"']/g, ch => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[ch]));
}
function money(value) {
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(value);
}
function shortPrice(value) {
  return value >= 10000000 ? `₹${(value / 10000000).toFixed(2)} crore` : `₹${(value / 100000).toFixed(2)} lakh`;
}
function mileageText(car) {
  return car.fuelType === "Electric" ? `${car.mileage} km` : `${car.mileage} ${car.mileageUnit}`;
}
function fullName(car) { return `${car.brand} ${car.name}`; }
function carImage(car, alt = true) {
  return car.image
    ? `<img src="${escapeHtml(car.image)}" alt="${alt ? escapeHtml(fullName(car)) : ""}" loading="lazy">`
    : `<div class="no-photo"><span>${escapeHtml(car.brand.toUpperCase())}<b>${escapeHtml(car.name)}</b><small>PHOTO COMING SOON</small></span></div>`;
}
function showToast(message) {
  const toast = $("toast");
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => toast.classList.remove("show"), 2500);
}
async function request(url) {
  const response = await fetch(url);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Something went wrong.");
  return data;
}
function fillSelect(select, values, firstLabel) {
  select.innerHTML = `<option value="">${firstLabel}</option>` +
    values.map(v => `<option value="${escapeHtml(v)}">${escapeHtml(v)}</option>`).join("");
}

/* ---------------- Variants helpers ---------------- */
function variantsOf(modelId) {
  return [...carIndex.values()].filter(c => c.modelId === modelId).sort((a, b) => a.price - b.price);
}
function modelSelected(modelId) {
  return selectedIds.some(id => carIndex.get(id)?.modelId === modelId);
}
function priceRange(min, max) {
  if (min === max) return shortPrice(min);
  const [a, b] = [shortPrice(min), shortPrice(max)];
  // "₹6.49 lakh – ₹8.20 lakh" -> "₹6.49 – 8.20 lakh" when units match
  return a.split(" ")[1] === b.split(" ")[1] ? `${a.split(" ")[0]} – ${b.replace("₹", "")}` : `${a} – ${b}`;
}
function variantOptions(car) {
  const all = variantsOf(car.modelId);
  return ["Base", "Mid", "Top"].map(level => {
    const group = all.filter(v => v.trimLevel === level);
    if (!group.length) return "";
    return `<optgroup label="${level} model">${group.map(v =>
      `<option value="${escapeHtml(v.id)}" ${v.id === car.id ? "selected" : ""}>${escapeHtml(v.variant)} · ${shortPrice(v.price)}</option>`).join("")}</optgroup>`;
  }).join("");
}

/* ---------------- Explore (one card per model) ---------------- */
function cardHtml(model) {
  const added = modelSelected(model.modelId);
  const power = model.powerMin === model.powerMax ? `${model.powerMax}` : `${model.powerMin}–${model.powerMax}`;
  return `
    <article class="car-card">
      <div class="car-image" data-details="${escapeHtml(model.defaultVariantId)}">
        ${carImage(model)}
        <span class="car-tag">${escapeHtml(model.bodyType.toUpperCase())}</span>
        <span class="variant-count">${model.variantCount} VARIANT${model.variantCount > 1 ? "S" : ""}</span>
      </div>
      <div class="car-info">
        <p class="car-brand">${escapeHtml(model.brand)}</p>
        <h3>${escapeHtml(model.name)}</h3>
        <div class="fuel-chips">${model.fuelTypes.map(f => `<span class="fuel-chip ${escapeHtml(f)}">${escapeHtml(f)}</span>`).join("")}</div>
        <p class="car-price">${priceRange(model.priceMin, model.priceMax)}<small>ex-showroom*</small></p>
        <div class="trim-dots">${model.trims.map(t => `<span class="level-badge ${t}" style="margin:0">${t}</span>`).join("")}</div>
        <div class="car-specs">
          <div><strong>${power} bhp</strong><span>POWER</span></div>
          <div><strong>${escapeHtml(model.transmissions.length > 1 ? "MT / AT" : model.transmissions[0])}</strong><span>GEARBOX</span></div>
          <div><strong>${model.seating} seats</strong><span>SEATING</span></div>
        </div>
        <div class="card-actions">
          <button class="add-compare ${added ? "added" : ""}" data-compare-model="${escapeHtml(model.modelId)}" data-default="${escapeHtml(model.defaultVariantId)}">${added ? "✓ Added" : "+ Compare"}</button>
          <button class="details-btn" data-details="${escapeHtml(model.defaultVariantId)}">View variants</button>
        </div>
      </div>
    </article>`;
}

function renderCars() {
  const grid = $("carGrid");
  if (!filteredCars.length) {
    grid.innerHTML = '<p class="empty-state">No vehicles match those filters. Try changing your search.</p>';
  } else {
    grid.innerHTML = filteredCars.slice(0, visibleCount).map(cardHtml).join("");
  }
  const remaining = filteredCars.length - visibleCount;
  $("showMore").hidden = remaining <= 0;
  $("showMore").textContent = `Show more models (${Math.max(remaining, 0)} left)`;
  const variants = filteredCars.reduce((sum, m) => sum + m.variantCount, 0);
  $("resultsCount").textContent = `${filteredCars.length} MODELS · ${variants} VARIANTS`;
}

function syncCompareButtons() {
  document.querySelectorAll("[data-compare]").forEach(btn => {
    const added = selectedIds.includes(btn.dataset.compare);
    btn.classList.toggle("added", added);
    btn.textContent = added ? "✓ Added" : "+ Compare";
  });
  document.querySelectorAll("[data-compare-model]").forEach(btn => {
    const added = modelSelected(btn.dataset.compareModel);
    btn.classList.toggle("added", added);
    btn.textContent = added ? "✓ Added" : "+ Compare";
  });
}

async function loadCars() {
  const params = new URLSearchParams();
  const q = $("searchInput").value.trim();
  if (q) params.set("q", q);
  if (activeBody) params.set("body", activeBody);
  if ($("brandFilter").value) params.set("brand", $("brandFilter").value);
  if ($("fuelFilter").value) params.set("fuel", $("fuelFilter").value);
  if ($("transFilter").value) params.set("transmission", $("transFilter").value);
  if ($("trimFilter").value) params.set("trim", $("trimFilter").value);
  if ($("priceFilter").value) params.set("maxPrice", $("priceFilter").value);
  params.set("sort", $("sortSelect").value);
  try {
    filteredCars = await request(`${API}/models?${params}`);
    visibleCount = PAGE_SIZE;
    renderCars();
  } catch (error) {
    $("carGrid").innerHTML = `<p class="empty-state">${escapeHtml(error.message)}</p>`;
  }
}

function renderBodyTabs() {
  const counts = {};
  const models = new Map();
  carIndex.forEach(c => models.set(c.modelId, c.bodyType));
  models.forEach(body => { counts[body] = (counts[body] || 0) + 1; });
  const tabs = [["", "All cars", models.size], ...meta.bodyTypes.map(b => [b, b === "MUV" ? "MUVs" : `${b}s`, counts[b]])];
  $("bodyTabs").innerHTML = tabs.map(([value, label, n]) =>
    `<button class="body-tab ${value === activeBody ? "active" : ""}" data-body="${escapeHtml(value)}">${escapeHtml(label)}<small>${n}</small></button>`).join("");
}

/* ---------------- Hero slideshow ---------------- */
function startHero() {
  const picks = ["hyundai-creta", "mahindra-thar-roxx", "tata-curvv", "bmw-x5", "maruti-suzuki-swift", "toyota-fortuner", "kia-ev6", "honda-city"];
  const seen = new Set();
  const slides = [];
  for (const id of picks) {
    const car = [...carIndex.values()].find(c => c.modelId === id && c.image);
    if (car && !seen.has(id)) { seen.add(id); slides.push(car); }
  }
  // Top up with any other models that have photos.
  for (const car of carIndex.values()) {
    if (slides.length >= 8) break;
    if (car.image && !seen.has(car.modelId)) { seen.add(car.modelId); slides.push(car); }
  }
  if (!slides.length) return;
  $("heroSlides").innerHTML = slides.map((c, i) =>
    `<img src="${escapeHtml(c.image)}" alt="${escapeHtml(fullName(c))}" class="${i === 0 ? "active" : ""}">`).join("");
  let index = 0;
  const show = () => {
    const imgs = $("heroSlides").querySelectorAll("img");
    imgs.forEach((img, i) => img.classList.toggle("active", i === index));
    $("heroCaption").textContent = fullName(slides[index]).toUpperCase();
    $("heroCounter").textContent = `${String(index + 1).padStart(2, "0")} / ${String(slides.length).padStart(2, "0")}`;
  };
  show();
  setInterval(() => { index = (index + 1) % slides.length; show(); }, 4500);
}

/* ---------------- Detail modal ---------------- */
let modalVariants = [];
let variantFilter = { level: "", fuel: "" };

async function openDetail(id) {
  // Switching variant inside the open model: no need to refetch.
  const local = modalVariants.find(v => v.id === id);
  if (local && !$("carModal").hidden) return renderDetail(local, modalVariants);
  try {
    const { car, variants } = await request(`${API}/cars/${encodeURIComponent(id)}`);
    variantFilter = { level: "", fuel: "" };
    modalVariants = variants;
    renderDetail(car, variants);
    $("carModal").hidden = false;
    document.body.classList.add("modal-open");
  } catch (error) { showToast(error.message); }
}

function renderDetail(car, variants) {
  const credit = car.imageCredit;
  const specs = [
    ["PRICE", money(car.price)],
    ["TRIM", `${car.trim} (${car.trimLevel} model)`],
    ["FUEL", car.fuelType],
    ["TRANSMISSION", car.transmission],
    [car.fuelType === "Electric" ? "BATTERY" : "ENGINE", car.engine],
    ["POWER", `${car.power} bhp`],
    ["TORQUE", `${car.torque} Nm`],
    [car.fuelType === "Electric" ? "CLAIMED RANGE" : "MILEAGE", mileageText(car)],
    ["RUNNING COST", `≈ ₹${car.runningCost}/km`],
    ["SEATING", `${car.seating} seats`],
    ["AIRBAGS", car.airbags],
    ["SAFETY RATING", car.ncap ? `${"★".repeat(car.ncap)} (${car.ncap}/5)` : "Not tested"],
    ["LENGTH", `${car.length} mm`],
    ["BOOT SPACE", car.bootSpace ? `${car.bootSpace} L` : "—"],
    [car.fuelType === "Electric" ? "FUEL TANK" : "FUEL TANK", car.fuelTank ? `${car.fuelTank} L` : "—"],
    ["GROUND CLEARANCE", `${car.groundClearance} mm`],
    ["BODY TYPE", car.bodyType],
  ];
  const added = selectedIds.includes(car.id);
  $("modalBody").innerHTML = `
    <div class="modal-hero">
      ${car.image ? `<img src="${escapeHtml(car.image)}" alt="${escapeHtml(fullName(car))}">` : `<div class="no-photo" style="height:300px">${escapeHtml(car.name)}</div>`}
      ${credit ? `<p class="photo-credit">Photo: ${escapeHtml(credit.author)} · ${escapeHtml(credit.license)} · <a href="${escapeHtml(credit.source)}" target="_blank" rel="noopener">Wikimedia Commons</a></p>` : ""}
    </div>
    <div class="modal-content">
      <p class="car-brand">${escapeHtml(car.brand)} · ${escapeHtml(car.bodyType)}</p>
      <h3 id="modalTitle">${escapeHtml(car.name)}</h3>
      <p class="lead">${escapeHtml(car.description)}</p>
      <p class="modal-price">${priceRange(variants[0].price, variants[variants.length - 1].price)} <small style="font:11px var(--font);color:var(--muted)">ex-showroom*</small></p>

      <p class="eyebrow" style="margin-bottom:10px">ALL ${variants.length} VARIANTS · BASE, MID &amp; TOP MODELS · CLICK ONE TO SEE ITS SPECS</p>
      <div id="variantTableBox"></div>

      <p class="eyebrow" style="margin:24px 0 12px">SPECIFICATIONS · ${escapeHtml(car.variant.toUpperCase())} <span class="level-badge ${escapeHtml(car.trimLevel)}">${escapeHtml(car.trimLevel)} model</span></p>
      <div class="spec-grid">${specs.map(([k, v]) => `<div><span>${k}</span><strong>${escapeHtml(v)}</strong></div>`).join("")}</div>
      <p class="eyebrow" style="margin-bottom:12px">FEATURES (TOP TRIM)</p>
      <div class="feature-list">${Object.entries(meta.features).map(([key, label]) =>
        `<span class="${car.features.includes(key) ? "yes" : "no"}">${car.features.includes(key) ? "✓" : "✗"} <span style="color:${car.features.includes(key) ? "#ddd" : "#666"};font-weight:400">${escapeHtml(label)}</span></span>`).join("")}</div>
      <div class="modal-actions">
        <button class="btn btn-primary add-compare ${added ? "added" : ""}" data-compare="${escapeHtml(car.id)}">${added ? "✓ Added" : "+ Compare"}</button>
        <a class="btn btn-ghost" href="#compare" data-close>Go to compare</a>
        <button class="btn btn-ghost" data-close>Close</button>
      </div>
    </div>`;
  renderVariantTable(car.id);
}

function renderVariantTable(activeId) {
  const levels = ["Base", "Mid", "Top"].filter(l => modalVariants.some(v => v.trimLevel === l));
  const fuels = [...new Set(modalVariants.map(v => v.fuelType))];
  const rows = modalVariants.filter(v =>
    (!variantFilter.level || v.trimLevel === variantFilter.level) &&
    (!variantFilter.fuel || v.fuelType === variantFilter.fuel));
  const chip = (kind, value, label) =>
    `<button class="vf-chip ${variantFilter[kind] === value ? "active" : ""}" data-vf-${kind}="${escapeHtml(value)}">${escapeHtml(label)}</button>`;
  $("variantTableBox").innerHTML = `
    <div class="variant-filters">
      ${levels.length > 1 ? `<span>MODEL</span>${chip("level", "", "All")}${levels.map(l => chip("level", l, l)).join("")}` : ""}
      ${fuels.length > 1 ? `<span>FUEL</span>${chip("fuel", "", "All")}${fuels.map(f => chip("fuel", f, f)).join("")}` : ""}
    </div>
    <div class="variant-table-wrap"><table class="variant-table">
      <thead><tr><th>Trim</th><th>Engine / gearbox</th><th>Fuel</th><th>Power</th><th>Mileage / range</th><th>Features</th><th>Price</th><th></th></tr></thead>
      <tbody>${rows.length ? rows.map(v => {
        const vAdded = selectedIds.includes(v.id);
        return `<tr class="${v.id === activeId ? "active" : ""}" data-variant="${escapeHtml(v.id)}">
          <td><strong>${escapeHtml(v.trim)}</strong><span class="level-badge ${escapeHtml(v.trimLevel)}">${escapeHtml(v.trimLevel)}</span></td>
          <td>${escapeHtml(v.powertrain)}</td>
          <td><span class="fuel-chip ${escapeHtml(v.fuelType)}">${escapeHtml(v.fuelType)}</span></td>
          <td>${v.power} bhp</td>
          <td>${escapeHtml(mileageText(v))}</td>
          <td>${v.features.length} / ${Object.keys(meta.features).length}</td>
          <td><strong>${shortPrice(v.price)}</strong></td>
          <td><button class="add-compare small ${vAdded ? "added" : ""}" data-compare="${escapeHtml(v.id)}">${vAdded ? "✓ Added" : "+ Compare"}</button></td>
        </tr>`;
      }).join("") : '<tr><td colspan="8" style="color:var(--muted)">No variants match this filter.</td></tr>'}</tbody>
    </table></div>`;
}

function closeModal() {
  $("carModal").hidden = true;
  document.body.classList.remove("modal-open");
}

/* ---------------- Recommend ---------------- */
function updateBudgetLabel() { $("budgetLabel").textContent = shortPrice(Number($("budgetInput").value)); }

async function runRecommend(event) {
  event.preventDefault();
  const params = new URLSearchParams({
    budget: $("budgetInput").value, body: $("recBody").value, fuel: $("recFuel").value,
    seats: $("recSeats").value, priority: $("recPriority").value,
  });
  const box = $("recommendResult");
  try {
    const data = await request(`${API}/recommend?${params}`);
    if (!data.results.length) {
      box.innerHTML = `<p class="empty-state">${escapeHtml(data.message)}</p>`;
      return;
    }
    box.innerHTML = `
      <p class="rec-summary">SCORED ${data.considered} CARS IN YOUR RANGE · TOP ${data.results.length} PICKS</p>
      <div class="rec-grid">${data.results.map(({ car, score, reasons }, i) => `
        <article class="rec-card ${i === 0 ? "top" : ""}">
          ${i === 0 ? '<span class="rec-rank">BEST MATCH</span>' : ""}
          <div class="car-image" data-details="${escapeHtml(car.id)}">${carImage(car)}
            <span class="fuel-tag ${escapeHtml(car.fuelType)}">${escapeHtml(car.fuelType.toUpperCase())} · ${escapeHtml(car.transmission.toUpperCase())}</span></div>
          <div class="rec-body">
            <p class="car-brand">${escapeHtml(car.brand)} · ${escapeHtml(car.bodyType)}</p>
            <h3 style="font:600 20px var(--display)">${escapeHtml(car.name)}</h3>
            <p class="car-variant">${escapeHtml(car.variant)} · <b style="color:white">${shortPrice(car.price)}</b></p>
            <div class="rec-score"><span>MATCH</span><span class="bar"><i style="width:${score}%"></i></span><b>${score}%</b></div>
            <ul class="rec-reasons">${reasons.map(r => `<li>${escapeHtml(r)}</li>`).join("")}</ul>
            <div class="card-actions">
              <button class="add-compare" data-compare="${escapeHtml(car.id)}">+ Compare</button>
              <button class="details-btn" data-details="${escapeHtml(car.id)}">View details</button>
            </div>
          </div>
        </article>`).join("")}</div>`;
    syncCompareButtons();
  } catch (error) {
    box.innerHTML = `<p class="empty-state">${escapeHtml(error.message)}</p>`;
  }
}

/* ---------------- Compare ---------------- */
function persistSelection() { store.set("carcompare_selected", selectedIds); }

function renderSelection() {
  const chosen = selectedIds.map(id => carIndex.get(id)).filter(Boolean);
  $("compareCount").textContent = chosen.length;
  $("navCompareCount").textContent = chosen.length;
  $("selectedCars").innerHTML = chosen.length ? chosen.map(car => `
    <div class="selected-item">
      ${car.image ? `<img src="${escapeHtml(car.image)}" alt="">` : '<span class="thumb"></span>'}
      <div><strong>${escapeHtml(fullName(car))}</strong>
        <select class="variant-select" data-swap="${escapeHtml(car.id)}" aria-label="Choose variant">${variantOptions(car)}</select></div>
      <button class="remove-selected" data-remove="${escapeHtml(car.id)}" aria-label="Remove">×</button>
    </div>`).join("")
    : '<p class="empty-state">Your comparison is empty. Use “+ Compare” on any car.</p>';
  syncCompareButtons();
}

function swapVariant(oldId, newId) {
  if (oldId === newId) return;
  if (selectedIds.includes(newId)) {
    renderSelection();
    return showToast("That variant is already in your comparison.");
  }
  selectedIds = selectedIds.map(id => (id === oldId ? newId : id));
  persistSelection();
  const comparing = $("comparisonResult").innerHTML.trim() !== "";
  renderSelection();
  if (comparing) runCompare(false);   // refresh the table in place
}

function toggleModel(modelId, defaultId) {
  // From a model card: remove every variant of that model, or add its default variant.
  if (modelSelected(modelId)) {
    selectedIds = selectedIds.filter(id => carIndex.get(id)?.modelId !== modelId);
    persistSelection();
    $("comparisonResult").innerHTML = "";
    renderSelection();
    return;
  }
  toggleCompare(defaultId);
}

function toggleCompare(id) {
  if (selectedIds.includes(id)) {
    selectedIds = selectedIds.filter(item => item !== id);
  } else if (selectedIds.length >= 3) {
    return showToast("You can compare up to 3 cars. Remove one first.");
  } else {
    selectedIds.push(id);
    const car = carIndex.get(id);
    if (car) showToast(`${fullName(car)} added to compare (${selectedIds.length}/3).`);
  }
  persistSelection();
  $("comparisonResult").innerHTML = "";
  renderSelection();
}

function compareRows() {
  const num = (v) => (v === null || v === undefined ? null : Number(v));
  const rows = [
    ["group", "OVERVIEW"],
    ["Trim", c => `${c.trim} (${c.trimLevel} model)`],
    ["Price (ex-showroom)", c => money(c.price), c => c.price, "low"],
    ["Body type", c => c.bodyType],
    ["Fuel", c => c.fuelType],
    ["Transmission", c => c.transmission],
    ["Seating", c => `${c.seating} seats`, c => c.seating, "high"],
    ["group", "ENGINE & PERFORMANCE"],
    ["Engine / battery", c => c.engine],
    ["Power", c => `${c.power} bhp`, c => c.power, "high"],
    ["Torque", c => `${c.torque} Nm`, c => c.torque, "high"],
    ["group", "EFFICIENCY"],
    ["Mileage / range", c => mileageText(c)],
    ["Running cost", c => `≈ ₹${c.runningCost}/km`, c => c.runningCost, "low"],
    ["Fuel tank", c => (c.fuelTank ? `${c.fuelTank} L` : "—"), c => num(c.fuelTank), "high"],
    ["group", "SIZE & PRACTICALITY"],
    ["Length", c => `${c.length} mm`, c => c.length, "high"],
    ["Boot space", c => (c.bootSpace ? `${c.bootSpace} L` : "—"), c => num(c.bootSpace), "high"],
    ["Ground clearance", c => `${c.groundClearance} mm`, c => c.groundClearance, "high"],
    ["group", "SAFETY"],
    ["Airbags", c => c.airbags, c => c.airbags, "high"],
    ["Safety rating", c => (c.ncap ? `${c.ncap}/5 stars` : "Not tested"), c => num(c.ncap), "high"],
    ["group", "FEATURES"],
    ["Features count", c => `${c.features.length} of ${Object.keys(meta.features).length}`, c => c.features.length, "high"],
    ...Object.entries(meta.features).map(([key, label]) => ["feature", label, key]),
  ];
  return rows;
}

function renderComparison(cars) {
  const cells = compareRows().map(row => {
    const [label, display, valueFn, better] = row;
    if (label === "group") return `<tr class="group"><th colspan="${cars.length + 1}">${display}</th></tr>`;
    if (label === "feature") {
      return `<tr><th>${escapeHtml(display)}</th>${cars.map(c =>
        c.features.includes(valueFn) ? '<td class="yes">✓ Yes</td>' : '<td class="no">✗ No</td>').join("")}</tr>`;
    }
    let bestValue = null;
    if (better) {
      const values = cars.map(valueFn).filter(v => v !== null && v !== undefined);
      if (values.length > 1 && new Set(values).size > 1) {
        bestValue = better === "high" ? Math.max(...values) : Math.min(...values);
      }
    }
    return `<tr><th>${escapeHtml(label)}</th>${cars.map(c => {
      const isBest = bestValue !== null && valueFn(c) === bestValue;
      return `<td class="${isBest ? "best" : ""}">${escapeHtml(display(c))}</td>`;
    }).join("")}</tr>`;
  }).join("");

  $("comparisonResult").innerHTML = `
    <table class="comparison-table">
      <thead><tr><th>SPECIFICATION</th>${cars.map(c => `
        <th>${c.image ? `<img src="${escapeHtml(c.image)}" alt="${escapeHtml(fullName(c))}">` : ""}
        ${escapeHtml(fullName(c))}
        <select class="variant-select" data-swap="${escapeHtml(c.id)}" aria-label="Choose variant">${variantOptions(c)}</select></th>`).join("")}</tr></thead>
      <tbody>${cells}</tbody>
    </table>
    <div class="compare-actions">
      <span class="compare-legend">★ = best in this comparison</span>
      <button class="btn btn-primary" id="saveComparison">♥ Save this comparison</button>
    </div>`;
  $("saveComparison").addEventListener("click", () => saveComparison(cars.map(c => c.id)));
}

async function runCompare(scroll = true) {
  if (selectedIds.length < 2) return showToast("Select at least 2 cars to compare.");
  try {
    const cars = await request(`${API}/compare?ids=${selectedIds.map(encodeURIComponent).join(",")}`);
    renderComparison(cars);
    if (scroll) $("comparisonResult").scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) { showToast(error.message); }
}

/* ---------------- Saved comparisons ---------------- */
function saveComparison(ids) {
  const key = [...ids].sort().join(",");
  if (savedComparisons.some(s => [...s.ids].sort().join(",") === key)) {
    return showToast("This comparison is already saved.");
  }
  savedComparisons.unshift({ ids, savedAt: new Date().toISOString() });
  store.set("carcompare_saved", savedComparisons);
  renderSaved();
  showToast("Comparison saved. Find it under Saved.");
}

function renderSaved() {
  const list = $("savedList");
  if (!savedComparisons.length) {
    list.innerHTML = '<p class="empty-state">No saved comparisons yet. Compare 2–3 cars and press “Save this comparison”.</p>';
    return;
  }
  list.innerHTML = savedComparisons.map((s, index) => {
    const cars = s.ids.map(id => carIndex.get(id)).filter(Boolean);
    const date = new Date(s.savedAt).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
    return `
      <div class="saved-item">
        <div class="saved-thumbs">${cars.map(c => (c.image ? `<img src="${escapeHtml(c.image)}" alt="">` : "")).join("")}</div>
        <div class="meta"><strong>${cars.map(c => escapeHtml(c.name)).join(" vs ")}</strong>
          <small>${cars.map(c => escapeHtml(c.variant)).join(" · ")} — saved ${date}</small></div>
        <button class="btn btn-primary" data-open-saved="${index}">Open</button>
        <button class="text-btn" data-delete-saved="${index}">Delete</button>
      </div>`;
  }).join("");
}

function openSaved(index) {
  const saved = savedComparisons[index];
  if (!saved) return;
  selectedIds = saved.ids.filter(id => carIndex.has(id));
  persistSelection();
  renderSelection();
  runCompare();
}

/* ---------------- Events ---------------- */
document.addEventListener("click", event => {
  const t = event.target;
  const el = sel => t.closest(sel);
  if (t.closest("select")) return;   // variant dropdowns handle themselves
  if (el("[data-compare]")) return toggleCompare(el("[data-compare]").dataset.compare);
  if (el("[data-compare-model]")) {
    const btn = el("[data-compare-model]");
    return toggleModel(btn.dataset.compareModel, btn.dataset.default);
  }
  if (el("[data-remove]")) return toggleCompare(el("[data-remove]").dataset.remove);
  const vf = el("[data-vf-level]") || el("[data-vf-fuel]");
  if (vf) {
    if (vf.dataset.vfLevel !== undefined) variantFilter.level = vf.dataset.vfLevel;
    if (vf.dataset.vfFuel !== undefined) variantFilter.fuel = vf.dataset.vfFuel;
    const active = $("variantTableBox").querySelector("tr.active");
    return renderVariantTable(active ? active.dataset.variant : "");
  }
  if (el("[data-variant]")) return openDetail(el("[data-variant]").dataset.variant);
  if (el("[data-details]")) return openDetail(el("[data-details]").dataset.details);
  if (el("[data-close]")) return closeModal();
  if (el("[data-open-saved]")) return openSaved(Number(el("[data-open-saved]").dataset.openSaved));
  if (el("[data-delete-saved]")) {
    savedComparisons.splice(Number(el("[data-delete-saved]").dataset.deleteSaved), 1);
    store.set("carcompare_saved", savedComparisons);
    renderSaved();
    return showToast("Saved comparison deleted.");
  }
  if (el("[data-body]")) {
    activeBody = el("[data-body]").dataset.body;
    renderBodyTabs();
    loadCars();
  }
});
document.addEventListener("change", e => {
  const select = e.target.closest("[data-swap]");
  if (select) swapVariant(select.dataset.swap, select.value);
});
document.addEventListener("keydown", e => { if (e.key === "Escape" && !$("carModal").hidden) closeModal(); });

$("compareButton").addEventListener("click", runCompare);
$("clearCompare").addEventListener("click", () => {
  selectedIds = [];
  persistSelection();
  $("comparisonResult").innerHTML = "";
  renderSelection();
});
$("resetFilters").addEventListener("click", () => {
  ["searchInput", "brandFilter", "fuelFilter", "transFilter", "trimFilter", "priceFilter"].forEach(id => { $(id).value = ""; });
  $("sortSelect").value = "name";
  activeBody = "";
  renderBodyTabs();
  loadCars();
});
$("showMore").addEventListener("click", () => { visibleCount += PAGE_SIZE; renderCars(); });
let searchTimer;
$("searchInput").addEventListener("input", () => { clearTimeout(searchTimer); searchTimer = setTimeout(loadCars, 250); });
["brandFilter", "fuelFilter", "transFilter", "trimFilter", "priceFilter", "sortSelect"].forEach(id => $(id).addEventListener("change", loadCars));
$("budgetInput").addEventListener("input", updateBudgetLabel);
$("recommendForm").addEventListener("submit", runRecommend);
$("menuToggle").addEventListener("click", () => document.querySelector(".nav-links").classList.toggle("open"));
document.querySelectorAll(".nav-links a").forEach(a => a.addEventListener("click", () => document.querySelector(".nav-links").classList.remove("open")));

/* ---------------- Start ---------------- */
(async function init() {
  try {
    const [metaData, allCars] = await Promise.all([request(`${API}/meta`), request(`${API}/cars`)]);
    meta = metaData;
    carIndex = new Map(allCars.map(c => [c.id, c]));
    selectedIds = selectedIds.filter(id => carIndex.has(id));

    $("statCars").textContent = meta.count;
    $("statModels").textContent = meta.models;
    $("statBrands").textContent = meta.brands.length;
    fillSelect($("brandFilter"), meta.brands, "All brands");
    fillSelect($("fuelFilter"), meta.fuelTypes, "All fuels");
    fillSelect($("transFilter"), meta.transmissions, "All gearboxes");
    fillSelect($("recBody"), meta.bodyTypes, "Any");
    fillSelect($("recFuel"), meta.fuelTypes, "Any");

    renderBodyTabs();
    startHero();
    updateBudgetLabel();
    renderSelection();
    renderSaved();
    await loadCars();
  } catch (error) {
    $("carGrid").innerHTML = `<p class="empty-state">Could not load cars: ${escapeHtml(error.message)}</p>`;
  }
})();
