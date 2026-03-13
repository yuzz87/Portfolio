/* ==============================
   Config
============================== */

const CONFIG = Object.freeze({
  /* ===== 可視化設定 ===== */
  VIS_ARRAY_SIZE: 40,
  VIS_DELAY: 8,

  BAR_W: 6,
  BAR_GAP: 1,
  HEIGHT_SCALE: 4,

  /* ===== C++ベンチマーク ===== */
  BENCHMARK_ARRAY_SIZE: 2000,

  /* ===== API ===== */
  API_TIMEOUT_MS: 10000,
  SAVE_TO_SERVER: true,

  /* ===== 統計 ===== */
  HISTORY_LIMIT: 10,
});

/* ==============================
   Algorithms (JS Visualizer)
============================== */

const ALGORITHMS = Object.freeze({
  バブル: bubbleSteps,
  選択: selectionSteps,
  挿入: insertionSteps,
  マージ: mergeSteps,
  クイック: quickSteps,
  ヒープ: heapSteps,
});

/* C++側識別子 */
const ENGINE_ALGO_KEY = Object.freeze({
  バブル: "bubble",
  選択: "selection",
  挿入: "insertion",
  マージ: "merge",
  クイック: "quick",
  ヒープ: "heap",
});

const ENGINE_KEY_TO_JA = Object.freeze(
  Object.fromEntries(
    Object.entries(ENGINE_ALGO_KEY).map(([ja, key]) => [key, ja]),
  ),
);

const EXPECTED_ENGINE_KEYS = Object.freeze(Object.values(ENGINE_ALGO_KEY));
const EXPECTED_JA_NAMES = Object.freeze(Object.keys(ALGORITHMS));

/* ==============================
   DOM
============================== */

const DOM = Object.freeze({
  grid: document.getElementById("battle-grid"),
  startBtn: document.getElementById("start-battle"),
  generateBtn: document.getElementById("generate-board"),
  result: document.getElementById("prediction-result"),
  stats: document.getElementById("statistics"),
  canvas: document.getElementById("fireworks-canvas"),
  rankSlots: Array.from(document.querySelectorAll(".slot")),
  algoPool: document.getElementById("algo-pool"),
});

/* ==============================
   Utils
============================== */

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function escapeHtml(value) {
  return String(value).replace(
    /[&<>"']/g,
    (m) =>
      ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
      })[m],
  );
}

function showMessage(html, type = "normal") {
  if (!DOM.result) return;

  const safeType =
    type === "error" ? "error" : type === "success" ? "success" : "normal";

  DOM.result.innerHTML = `<span class="message-${safeType}">${html}</span>`;
}

function showError(message) {
  showMessage(escapeHtml(message), "error");
}

function clearMessage() {
  if (!DOM.result) return;
  DOM.result.textContent = "";
}

function makeValues(size) {
  const arr = Array.from({ length: size }, (_, i) => i + 1);

  for (let i = arr.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }

  return arr;
}

function clearCardDecorations() {
  EXPECTED_JA_NAMES.forEach((name) => {
    const card = document.getElementById(`card-${name}`);
    if (!card) return;

    card.classList.remove("rank-1", "rank-2", "rank-3");
    card.querySelectorAll(".time-label").forEach((el) => el.remove());
  });
}

function clearStatistics() {
  if (DOM.stats) DOM.stats.innerHTML = "";
}

function resetPredictionSlots() {
  DOM.rankSlots.forEach((slot) => {
    delete slot.dataset.value;
  });
}

function setButtonBusy(isBusy) {
  if (DOM.startBtn) {
    DOM.startBtn.disabled = isBusy;
    DOM.startBtn.textContent = isBusy ? "実行中..." : "Start";
  }

  if (DOM.generateBtn) {
    DOM.generateBtn.disabled = isBusy;
  }
}

function createNode(tag, className, text) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (text != null) el.textContent = text;
  return el;
}

/* ==============================
   fetch wrapper
============================== */

async function fetchJson(url, options = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), CONFIG.API_TIMEOUT_MS);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });

    const data = await response.json().catch(() => null);

    return {
      ok: response.ok,
      status: response.status,
      data,
      error: null,
    };
  } catch (error) {
    return {
      ok: false,
      status: 0,
      data: null,
      error,
    };
  } finally {
    clearTimeout(timer);
  }
}

/* ==============================
   Board Rendering
============================== */

function createBoards(values) {
  if (!DOM.grid) return;

  DOM.grid.innerHTML = "";
  const fragment = document.createDocumentFragment();

  EXPECTED_JA_NAMES.forEach((name) => {
    const card = createNode("div", "battle-card");
    card.id = `card-${name}`;

    const title = createNode("div", "battle-title", name);

    const board = createNode("div", "mini-board");
    board.id = `board-${name}`;

    values.forEach((v, i) => {
      const bar = createNode("div", "mini-bar");
      bar.style.left = `${i * (CONFIG.BAR_W + CONFIG.BAR_GAP)}px`;
      bar.style.width = `${CONFIG.BAR_W}px`;
      bar.style.height = `${v * CONFIG.HEIGHT_SCALE}px`;
      board.appendChild(bar);
    });

    card.appendChild(title);
    card.appendChild(board);
    fragment.appendChild(card);
  });

  DOM.grid.appendChild(fragment);
}

/* ==============================
   Prediction
============================== */

function initDragPrediction() {
  if (!DOM.algoPool || DOM.rankSlots.length === 0) return;

  DOM.algoPool.innerHTML = "";
  let draggedCard = null;

  EXPECTED_JA_NAMES.forEach((name) => {
    const card = createNode("div", "algo-card", name);
    card.draggable = true;

    card.addEventListener("dragstart", (event) => {
      draggedCard = card;
      event.dataTransfer.effectAllowed = "move";
      event.dataTransfer.setData("text/plain", name);
    });

    card.addEventListener("dragend", () => {
      draggedCard = null;
    });

    DOM.algoPool.appendChild(card);
  });

  DOM.rankSlots.forEach((slot) => {
    slot.addEventListener("dragover", (event) => {
      event.preventDefault();
      event.dataTransfer.dropEffect = "move";
    });

    slot.addEventListener("drop", (event) => {
      event.preventDefault();

      if (!draggedCard) return;
      if (slot.contains(draggedCard)) return;

      const existingCard = slot.querySelector(".algo-card");
      if (existingCard) {
        DOM.algoPool.appendChild(existingCard);
      }

      slot.innerHTML = "";
      slot.appendChild(draggedCard);
      slot.dataset.value = draggedCard.textContent || "";

      draggedCard.classList.add("dropped");
      setTimeout(() => {
        draggedCard?.classList.remove("dropped");
      }, 200);

      draggedCard = null;
    });
  });
}

function getPredictionPicks() {
  return DOM.rankSlots.map((slot) => slot.dataset.value || "");
}

function validatePrediction() {
  const picks = getPredictionPicks();
  if (picks.length !== 3) return false;
  if (picks.some((value) => !value)) return false;
  return new Set(picks).size === picks.length;
}

/* ==============================
   Fireworks
============================== */

let fireworksRunning = false;

function launchFireworks() {
  if (fireworksRunning) return;
  if (!DOM.canvas) return;

  const canvas = DOM.canvas;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  fireworksRunning = true;

  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const particles = Array.from({ length: 150 }, () => ({
    x: canvas.width / 2,
    y: canvas.height / 2,
    angle: Math.random() * Math.PI * 2,
    speed: Math.random() * 6 + 2,
    life: 80,
    color: `hsl(${Math.random() * 360},100%,60%)`,
  }));

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach((particle) => {
      if (particle.life <= 0) return;

      particle.x += Math.cos(particle.angle) * particle.speed;
      particle.y += Math.sin(particle.angle) * particle.speed;
      particle.life -= 1;

      ctx.fillStyle = particle.color;
      ctx.fillRect(particle.x, particle.y, 3, 3);
    });

    if (particles.some((particle) => particle.life > 0)) {
      requestAnimationFrame(animate);
      return;
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    fireworksRunning = false;
  }

  animate();
}

/* ==============================
   Validation helpers
============================== */

function isValidRankingRow(row) {
  if (!row || typeof row !== "object") return false;

  const rank = Number(row.rank);
  const duration = Number(row.duration_ms);
  const algorithmKey = String(row.algorithm);

  return (
    Number.isInteger(rank) &&
    rank >= 1 &&
    rank <= EXPECTED_ENGINE_KEYS.length &&
    Number.isFinite(duration) &&
    duration >= 0 &&
    EXPECTED_ENGINE_KEYS.includes(algorithmKey)
  );
}

function normalizeRanking(rawRanking) {
  if (!Array.isArray(rawRanking)) {
    throw new Error("ranking が配列ではありません");
  }

  if (rawRanking.length !== EXPECTED_ENGINE_KEYS.length) {
    throw new Error(
      `ranking件数が不正です: expected=${EXPECTED_ENGINE_KEYS.length}, actual=${rawRanking.length}`,
    );
  }

  const normalized = rawRanking
    .map((row) => {
      if (!isValidRankingRow(row)) {
        throw new Error("ranking 内の要素形式が不正です");
      }

      const algorithmKey = String(row.algorithm);
      const algorithmJa = ENGINE_KEY_TO_JA[algorithmKey];

      if (!algorithmJa) {
        throw new Error(`未対応の algorithm です: ${algorithmKey}`);
      }

      return {
        rank: Number(row.rank),
        algorithmKey,
        algorithmJa,
        duration_ms: Number(row.duration_ms),
      };
    })
    .sort((a, b) => a.rank - b.rank);

  const rankSet = new Set(normalized.map((item) => item.rank));
  const algoSet = new Set(normalized.map((item) => item.algorithmKey));

  if (rankSet.size !== EXPECTED_ENGINE_KEYS.length) {
    throw new Error("rank が重複または欠損しています");
  }

  if (algoSet.size !== EXPECTED_ENGINE_KEYS.length) {
    throw new Error("algorithm が重複または欠損しています");
  }

  for (let i = 0; i < EXPECTED_ENGINE_KEYS.length; i += 1) {
    if (normalized[i].rank !== i + 1) {
      throw new Error("rank が 1 位から連番になっていません");
    }
  }

  return normalized;
}

/* ==============================
   Battle Engine
============================== */

class Battle {
  constructor() {
    this.results = [];
    this.history = [];
    this.running = false;
  }

  async run() {
    if (this.running) return;

    if (!validatePrediction()) {
      alert("1位〜3位を予想してください（重複不可）");
      return;
    }

    this.running = true;
    setButtonBusy(true);

    try {
      clearCardDecorations();
      clearMessage();
      clearStatistics();

      const values = makeValues(CONFIG.VIS_ARRAY_SIZE);
      createBoards(values);

      await this.fetchRankingFromServer();

      await Promise.all(
        Object.entries(ALGORITHMS).map(([name, algorithm]) =>
          this.visualize(name, algorithm, values.slice()),
        ),
      );

      this.updateHistory();
      this.renderRanking();
      this.renderPrediction();
      this.renderStatistics();

      if (CONFIG.SAVE_TO_SERVER) {
        await this.saveBattleToServer();
      }
    } catch (error) {
      console.error(error);
      showError(error?.message || "バトル実行中にエラーが発生しました");
    } finally {
      this.running = false;
      setButtonBusy(false);
    }
  }

  async fetchRankingFromServer() {
    const { ok, data, status, error } = await fetchJson("/api/run-battle", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        array_size: CONFIG.BENCHMARK_ARRAY_SIZE,
      }),
    });

    if (!ok || !data) {
      if (error?.name === "AbortError") {
        throw new Error("サーバー応答がタイムアウトしました");
      }
      throw new Error(`サーバー通信に失敗しました (status=${status})`);
    }

    if (!data.success) {
      throw new Error(data?.error?.message || "ランキング取得に失敗しました");
    }

    const rawRanking = Array.isArray(data?.data)
      ? data.data
      : data?.data?.ranking;
    this.results = normalizeRanking(rawRanking);
  }

  async visualize(name, algorithm, values) {
    const board = document.getElementById(`board-${name}`);
    if (!board) return;

    const bars = board.children;
    const steps = algorithm(values);

    if (!Array.isArray(steps)) return;

    for (const step of steps) {
      if (!step || typeof step !== "object") continue;

      if (step.type === "swap") {
        const i = Number(step.i);
        const j = Number(step.j);

        if (!Number.isInteger(i) || !Number.isInteger(j)) continue;
        if (i < 0 || j < 0 || i >= values.length || j >= values.length)
          continue;

        [values[i], values[j]] = [values[j], values[i]];

        if (bars[i])
          bars[i].style.height = `${values[i] * CONFIG.HEIGHT_SCALE}px`;
        if (bars[j])
          bars[j].style.height = `${values[j] * CONFIG.HEIGHT_SCALE}px`;
      }

      if (step.type === "set") {
        const index = Number(step.index);
        const value = Number(step.value);

        if (!Number.isInteger(index)) continue;
        if (index < 0 || index >= values.length) continue;
        if (!Number.isFinite(value)) continue;

        values[index] = value;
        if (bars[index]) {
          bars[index].style.height = `${values[index] * CONFIG.HEIGHT_SCALE}px`;
        }
      }

      await sleep(CONFIG.VIS_DELAY);
    }
  }

  renderRanking() {
    this.results.forEach((result, index) => {
      const card = document.getElementById(`card-${result.algorithmJa}`);
      if (!card) return;

      if (index === 0) card.classList.add("rank-1");
      if (index === 1) card.classList.add("rank-2");
      if (index === 2) card.classList.add("rank-3");

      const label = createNode(
        "div",
        "time-label",
        `${index + 1}位 : ${result.duration_ms.toFixed(3)} ms`,
      );

      card.appendChild(label);
    });
  }

  renderPrediction() {
    const picks = getPredictionPicks();

    let correct = 0;
    for (let i = 0; i < 3; i += 1) {
      if (this.results[i]?.algorithmJa === picks[i]) {
        correct += 1;
      }
    }

    const top3 = this.results
      .slice(0, 3)
      .map((result) => result.algorithmJa)
      .join(" → ");

    showMessage(
      `結果 : ${escapeHtml(top3)}<br>的中数 : ${correct}/3`,
      correct === 3 ? "success" : "normal",
    );

    if (correct === 3) {
      launchFireworks();
    }
  }

  updateHistory() {
    this.history.push(this.results.map((result) => result.algorithmJa));

    if (this.history.length > CONFIG.HISTORY_LIMIT) {
      this.history.shift();
    }
  }

  renderStatistics() {
    if (!DOM.stats) return;

    const counts = {};
    this.history.forEach((round) => {
      round.slice(0, 3).forEach((name, position) => {
        if (!counts[name]) counts[name] = [0, 0, 0];
        counts[name][position] += 1;
      });
    });

    const totalRounds = this.history.length;
    const wrapper = document.createDocumentFragment();

    const title = createNode(
      "h4",
      "",
      `直近${CONFIG.HISTORY_LIMIT}回統計（このページ内）`,
    );
    wrapper.appendChild(title);

    EXPECTED_JA_NAMES.forEach((name) => {
      const [first = 0, second = 0, third = 0] = counts[name] || [0, 0, 0];
      const line = createNode("div", "stats-line");

      const p1 =
        totalRounds === 0 ? 0 : ((first / totalRounds) * 100).toFixed(0);
      const p2 =
        totalRounds === 0 ? 0 : ((second / totalRounds) * 100).toFixed(0);
      const p3 =
        totalRounds === 0 ? 0 : ((third / totalRounds) * 100).toFixed(0);

      line.textContent = `${name} : 1位 ${p1}% / 2位 ${p2}% / 3位 ${p3}%`;
      wrapper.appendChild(line);
    });

    DOM.stats.innerHTML = "";
    DOM.stats.appendChild(wrapper);
  }

  async saveBattleToServer() {
    const payload = {
      user_id: null,
      array_size: CONFIG.VIS_ARRAY_SIZE,
      benchmark_size: CONFIG.BENCHMARK_ARRAY_SIZE,
      results: this.results.map((result) => ({
        algorithm: result.algorithmKey,
        duration_ms: result.duration_ms,
        rank: result.rank,
      })),
    };

    const { ok, status, data, error } = await fetchJson("/api/battles", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!ok) {
      console.warn("保存失敗", { status, data, error });
      showError("バトル結果の保存に失敗しました");
      return;
    }

    if (!data?.success) {
      console.warn("保存失敗", data);
      showError(data?.error?.message || "バトル結果の保存に失敗しました");
    }
  }
}

/* ==============================
   Init
============================== */

window.addEventListener("DOMContentLoaded", () => {
  if (!DOM.grid) return;

  initDragPrediction();

  const battle = new Battle();
  createBoards(makeValues(CONFIG.VIS_ARRAY_SIZE));

  DOM.generateBtn?.addEventListener("click", () => {
    if (battle.running) return;

    clearCardDecorations();
    clearMessage();
    createBoards(makeValues(CONFIG.VIS_ARRAY_SIZE));
  });

  DOM.startBtn?.addEventListener("click", async () => {
    await battle.run();
  });
});
