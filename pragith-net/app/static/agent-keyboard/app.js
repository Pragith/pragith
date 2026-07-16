(() => {
  'use strict';

  const consoleEl = document.getElementById('console');
  const device = document.getElementById('device');
  const soundToggle = document.getElementById('soundToggle');
  const soundLabel = document.getElementById('soundLabel');

  function log(text) {
    const line = document.createElement('div');
    line.className = 'console-line';
    line.textContent = text;
    consoleEl.appendChild(line);
    consoleEl.scrollTop = consoleEl.scrollHeight;
    while (consoleEl.children.length > 40) consoleEl.removeChild(consoleEl.firstChild);
  }

  // ---------------- sound engine ----------------
  // Synthesized mechanical click (Web Audio, no audio files needed).
  // "Mechanical" = crisp clicky switch. "Muted" = soft dampened macbook-style thock.

  let ctx = null;
  let muted = JSON.parse(localStorage.getItem('codexmicro-muted') || 'false');

  function ensureCtx() {
    if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }

  function playClick(kind) {
    const ac = ensureCtx();
    const now = ac.currentTime;
    const master = ac.createGain();
    master.connect(ac.destination);

    if (muted) {
      // real-MacBook-style "thock": a bandpass-filtered noise transient
      // (the plasticky knock of the keycap bottoming out) layered over a
      // fast-decaying low sine body (the dull thud through the chassis).
      // Keyup is quieter/higher than keydown, and each hit is randomized
      // slightly so it doesn't sound like a robotic loop.
      const jitter = 0.92 + Math.random() * 0.16;
      const isUp = kind === 'up';

      const bufferSize = Math.floor(ac.sampleRate * 0.02);
      const buffer = ac.createBuffer(1, bufferSize, ac.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / bufferSize, 2);
      }
      const noise = ac.createBufferSource();
      noise.buffer = buffer;
      const bandpass = ac.createBiquadFilter();
      bandpass.type = 'bandpass';
      bandpass.frequency.value = (isUp ? 1500 : 1100) * jitter;
      bandpass.Q.value = 1.1;
      const noiseGain = ac.createGain();
      noiseGain.gain.setValueAtTime(isUp ? 0.07 : 0.11, now);
      noiseGain.gain.exponentialRampToValueAtTime(0.001, now + 0.02);
      noise.connect(bandpass);
      bandpass.connect(noiseGain);
      noiseGain.connect(master);

      const body = ac.createOscillator();
      body.type = 'sine';
      const bodyFreq = (isUp ? 210 : 150) * jitter;
      body.frequency.setValueAtTime(bodyFreq, now);
      body.frequency.exponentialRampToValueAtTime(bodyFreq * 0.7, now + 0.03);
      const bodyGain = ac.createGain();
      bodyGain.gain.setValueAtTime(isUp ? 0.08 : 0.13, now);
      bodyGain.gain.exponentialRampToValueAtTime(0.001, now + 0.035);
      body.connect(bodyGain);
      bodyGain.connect(master);

      master.gain.setValueAtTime(1, now);
      noise.start(now);
      body.start(now);
      noise.stop(now + 0.025);
      body.stop(now + 0.04);
      return;
    }

    // mechanical clicky: filtered noise burst + short tonal tick
    const bufferSize = ac.sampleRate * 0.03;
    const buffer = ac.createBuffer(1, bufferSize, ac.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      data[i] = (Math.random() * 2 - 1) * (1 - i / bufferSize);
    }
    const noise = ac.createBufferSource();
    noise.buffer = buffer;
    const filter = ac.createBiquadFilter();
    filter.type = 'highpass';
    filter.frequency.value = kind === 'up' ? 2200 : 3200;
    noise.connect(filter);

    const noiseGain = ac.createGain();
    noiseGain.gain.setValueAtTime(0.5, now);
    noiseGain.gain.exponentialRampToValueAtTime(0.001, now + 0.045);
    filter.connect(noiseGain);
    noiseGain.connect(master);

    const tick = ac.createOscillator();
    tick.type = 'square';
    tick.frequency.setValueAtTime(kind === 'up' ? 2600 : 3400, now);
    const tickGain = ac.createGain();
    tickGain.gain.setValueAtTime(0.08, now);
    tickGain.gain.exponentialRampToValueAtTime(0.001, now + 0.02);
    tick.connect(tickGain);
    tickGain.connect(master);

    master.gain.setValueAtTime(0.9, now);
    noise.start(now);
    tick.start(now);
    noise.stop(now + 0.05);
    tick.stop(now + 0.03);
  }

  function setMuted(next) {
    muted = next;
    localStorage.setItem('codexmicro-muted', JSON.stringify(muted));
    soundToggle.setAttribute('aria-pressed', String(muted));
    soundLabel.textContent = muted ? 'Muted' : 'Mechanical';
  }
  setMuted(muted);
  soundToggle.addEventListener('click', () => {
    setMuted(!muted);
    playClick('down');
  });

  // ---------------- generic key press wiring ----------------

  function bindKey(el, { onDown, onUp } = {}) {
    const press = () => {
      el.classList.add('pressed');
      playClick('down');
      if (onDown) onDown();
    };
    const release = () => {
      el.classList.remove('pressed');
      playClick('up');
      if (onUp) onUp();
    };
    el.addEventListener('pointerdown', (e) => { e.preventDefault(); press(); });
    el.addEventListener('pointerup', release);
    el.addEventListener('pointerleave', () => el.classList.remove('pressed'));
    el.addEventListener('contextmenu', (e) => e.preventDefault());
  }

  // ---------------- icon action keys ----------------

  const actions = {
    run: () => log('build queued → running task…'),
    approve: () => log('change approved ✓'),
    reject: () => log('change rejected ✕'),
    deploy: () => log('deploying to prod → done'),
    cloud: () => {
      const quotes = [
        'human knowledge belongs to the world.',
        'ship the small thing today.',
        'the fastest way is the direct way.',
        'clarity beats cleverness.',
        'make it work, then make it vibe.'
      ];
      log('// ' + quotes[Math.floor(Math.random() * quotes.length)]);
    }
  };

  document.querySelectorAll('[data-action]').forEach((el) => {
    const action = el.dataset.action;
    if (action === 'mic') return; // handled separately (hold-to-talk)
    bindKey(el, { onDown: () => actions[action] && actions[action]() });
  });

  // (switch slot click handling is wired later, once the panel-key icon
  // library is defined — see "panel keys" section below)

  // ---------------- mic: hold to talk ----------------

  const micKey = document.querySelector('[data-action="mic"]');
  const micLabel = micKey.querySelector('.mic-label');
  let recognition = null;
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRec) {
    recognition = new SpeechRec();
    recognition.continuous = true;
    recognition.interimResults = false;
    recognition.onresult = (e) => {
      const said = e.results[e.results.length - 1][0].transcript.trim();
      if (said) log('heard: "' + said + '"');
    };
    recognition.onerror = () => {};
  }

  function startListening() {
    micKey.classList.add('pressed', 'listening');
    micLabel.textContent = 'Listening…';
    playClick('down');
    log('mic: listening…');
    if (recognition) { try { recognition.start(); } catch (_) {} }
  }
  function stopListening() {
    micKey.classList.remove('pressed', 'listening');
    playClick('up');
    log('mic: off');
    if (recognition) { try { recognition.stop(); } catch (_) {} }
  }
  micKey.addEventListener('pointerdown', (e) => { e.preventDefault(); startListening(); });
  micKey.addEventListener('pointerup', stopListening);
  micKey.addEventListener('pointerleave', () => {
    if (micKey.classList.contains('listening')) stopListening();
  });

  // ---------------- rotary dial: drag / scroll → intensity ----------------

  const dial = document.getElementById('dial');
  const dialCap = dial.querySelector('.dial-cap');
  let dialValue = 15; // 0..100, mirrors --glow
  let dragging = false;
  let lastY = 0;
  let rotation = 0;

  function applyDial() {
    device.style.setProperty('--glow', (0.1 + dialValue / 100 * 0.7).toFixed(2));
    dialCap.style.setProperty('--dial-rot', rotation);
  }

  dial.addEventListener('pointerdown', (e) => {
    dragging = true;
    lastY = e.clientY;
    dial.setPointerCapture(e.pointerId);
    playClick('down');
  });
  dial.addEventListener('pointermove', (e) => {
    if (!dragging) return;
    const delta = lastY - e.clientY;
    lastY = e.clientY;
    dialValue = Math.min(100, Math.max(0, dialValue + delta));
    rotation += delta * 1.5;
    applyDial();
  });
  ['pointerup', 'pointercancel'].forEach((ev) =>
    dial.addEventListener(ev, () => { if (dragging) { dragging = false; playClick('up'); log('dial: intensity ' + Math.round(dialValue) + '%'); } })
  );
  dial.addEventListener('wheel', (e) => {
    e.preventDefault();
    dialValue = Math.min(100, Math.max(0, dialValue - e.deltaY * 0.2));
    rotation += -e.deltaY * 0.3;
    applyDial();
    log('dial: intensity ' + Math.round(dialValue) + '%');
  }, { passive: false });
  applyDial();

  // ---------------- joystick: drag → nudge / scroll console ----------------

  const joystick = document.getElementById('joystick');
  const joyCap = joystick.querySelector('.joy-cap');
  let joyDragging = false;
  let joyStart = { x: 0, y: 0 };

  joystick.addEventListener('pointerdown', (e) => {
    joyDragging = true;
    joyStart = { x: e.clientX, y: e.clientY };
    joystick.setPointerCapture(e.pointerId);
    playClick('down');
  });
  joystick.addEventListener('pointermove', (e) => {
    if (!joyDragging) return;
    const dx = Math.max(-8, Math.min(8, e.clientX - joyStart.x));
    const dy = Math.max(-8, Math.min(8, e.clientY - joyStart.y));
    joyCap.style.transform = `translate(${dx}px, ${dy}px)`;
    consoleEl.scrollTop += dy * 0.5;
  });
  ['pointerup', 'pointercancel'].forEach((ev) =>
    joystick.addEventListener(ev, () => {
      if (!joyDragging) return;
      joyDragging = false;
      joyCap.style.transform = '';
      playClick('up');
    })
  );

  // ---------------- keybinding manager ----------------
  // Single source of truth for "physical key → on-screen action". Today the
  // physical key is a browser keydown; in the eventual Electron build this
  // same table gets read by the HID/hardware-macropad listener instead —
  // see AGENTS.md "grand vision" milestone 4.

  const BIND_ACTIONS = [
    { action: 'run', label: 'Run' },
    { action: 'approve', label: 'Approve' },
    { action: 'reject', label: 'Reject' },
    { action: 'deploy', label: 'Deploy' },
    { action: 'cloud', label: 'Inspire' },
    { action: 'mic', label: 'Mic (hold)' }
  ];
  const DEFAULT_BINDS = { run: '1', approve: '2', reject: '3', deploy: '4', cloud: 'c', mic: 'm' };
  const BIND_KEY = 'codexmicro-keybinds';

  let binds = { ...DEFAULT_BINDS, ...(JSON.parse(localStorage.getItem(BIND_KEY) || '{}')) };

  function saveBinds() {
    localStorage.setItem(BIND_KEY, JSON.stringify(binds));
  }

  function actionForKey(key) {
    return Object.keys(binds).find((action) => binds[action] === key);
  }

  function fireDown(action) {
    if (action === 'mic') { startListening(); return; }
    const el = document.querySelector(`[data-action="${action}"]`);
    if (el) el.classList.add('pressed');
    playClick('down');
    if (actions[action]) actions[action]();
  }
  function fireUp(action) {
    if (action === 'mic') { stopListening(); return; }
    const el = document.querySelector(`[data-action="${action}"]`);
    if (el) el.classList.remove('pressed');
    playClick('up');
  }

  const held = new Set();
  window.addEventListener('keydown', (e) => {
    if (capturingAction) return; // rebind flow handles this key itself
    const k = e.key.toLowerCase();
    if (held.has(k)) return;
    held.add(k);
    const action = actionForKey(k);
    if (action) fireDown(action);
  });
  window.addEventListener('keyup', (e) => {
    const k = e.key.toLowerCase();
    held.delete(k);
    const action = actionForKey(k);
    if (action) fireUp(action);
  });

  // ---------------- settings overlay ----------------

  const settingsBtn = document.getElementById('settingsBtn');
  const overlayBackdrop = document.getElementById('overlayBackdrop');
  const overlayClose = document.getElementById('overlayClose');
  const overlayReset = document.getElementById('overlayReset');
  const bindList = document.getElementById('bindList');

  let capturingAction = null;

  function renderBindList() {
    bindList.innerHTML = '';
    BIND_ACTIONS.forEach(({ action, label }) => {
      const row = document.createElement('div');
      row.className = 'bind-row';

      const name = document.createElement('span');
      name.className = 'bind-name';
      name.textContent = label;

      const controls = document.createElement('span');
      controls.className = 'bind-controls';

      const keyBadge = document.createElement('span');
      keyBadge.className = 'bind-key';
      keyBadge.textContent = binds[action] || '—';

      const rebindBtn = document.createElement('button');
      rebindBtn.className = 'bind-rebind';
      rebindBtn.textContent = capturingAction === action ? 'Press a key…' : 'Rebind';
      if (capturingAction === action) rebindBtn.classList.add('listening');
      rebindBtn.addEventListener('click', () => beginCapture(action));

      controls.append(keyBadge, rebindBtn);
      row.append(name, controls);
      bindList.appendChild(row);
    });
  }

  function beginCapture(action) {
    capturingAction = action;
    renderBindList();
    const onKey = (e) => {
      e.preventDefault();
      const k = e.key.toLowerCase();
      // clear whichever action currently owns this key to avoid double-binding
      const prevOwner = actionForKey(k);
      if (prevOwner && prevOwner !== action) delete binds[prevOwner];
      binds[action] = k;
      saveBinds();
      capturingAction = null;
      window.removeEventListener('keydown', onKey, true);
      renderBindList();
      log(`bound "${k}" → ${action}`);
    };
    window.addEventListener('keydown', onKey, true);
  }

  function openOverlay() { overlayBackdrop.classList.add('open'); renderBindList(); }
  function closeOverlay() { overlayBackdrop.classList.remove('open'); capturingAction = null; }

  bindKey(settingsBtn, { onDown: () => openOverlay() });
  overlayClose.addEventListener('click', () => { playClick('up'); closeOverlay(); });
  overlayBackdrop.addEventListener('click', (e) => { if (e.target === overlayBackdrop) closeOverlay(); });
  overlayReset.addEventListener('click', () => {
    binds = { ...DEFAULT_BINDS };
    saveBinds();
    renderBindList();
    log('keybindings reset to defaults');
  });
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && overlayBackdrop.classList.contains('open')) closeOverlay();
  });

  // ---------------- settings tabs ----------------

  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');
  tabBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      tabBtns.forEach((b) => b.classList.remove('active'));
      tabPanes.forEach((p) => p.classList.remove('active'));
      btn.classList.add('active');
      document.querySelector(`.tab-pane[data-pane="${btn.dataset.tab}"]`).classList.add('active');
      playClick('down');
    });
  });

  // ---------------- panel keys: swappable icon library for the blank switch slots ----------------

  const ICON_LIBRARY = [
    { id: 'star', label: 'Favorite', svg: '<path d="M12 3l2.6 5.9 6.4.6-4.8 4.3 1.4 6.3L12 16.9 6.4 20.1l1.4-6.3-4.8-4.3 6.4-.6L12 3z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>' },
    { id: 'trash', label: 'Delete', svg: '<path d="M5 7h14M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2M8 7l1 13a1 1 0 0 0 1 1h4a1 1 0 0 0 1-1l1-13" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>' },
    { id: 'download', label: 'Download', svg: '<path d="M12 3v12m0 0 4-4m-4 4-4-4M5 19h14" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>' },
    { id: 'upload', label: 'Upload', svg: '<path d="M12 21V9m0 0 4 4m-4-4-4 4M5 5h14" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>' },
    { id: 'edit', label: 'Edit', svg: '<path d="M4 20l1-4L16 5l3 3L8 19l-4 1z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>' },
    { id: 'send', label: 'Send', svg: '<path d="M4 12l16-8-6 16-3-6-7-2z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>' },
    { id: 'add', label: 'Add', svg: '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M12 8v8M8 12h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>' },
    { id: 'play', label: 'Play', svg: '<path d="M8 6l11 6-11 6V6z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>' },
    { id: 'branch', label: 'Branch', svg: '<circle cx="6" cy="6" r="2" fill="none" stroke="currentColor" stroke-width="1.4"/><circle cx="6" cy="18" r="2" fill="none" stroke="currentColor" stroke-width="1.4"/><circle cx="18" cy="12" r="2" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M6 8v6m0-6c0 4 6 4 10 4" fill="none" stroke="currentColor" stroke-width="1.4"/>' },
    { id: 'flask', label: 'Experiment', svg: '<path d="M10 3h4M9 3v6l-5 9a2 2 0 0 0 2 3h12a2 2 0 0 0 2-3l-5-9V3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>' },
    { id: 'clock', label: 'History', svg: '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M12 7v5l4 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" fill="none"/>' },
    { id: 'gear', label: 'Settings', svg: '<circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M12 4v2M12 18v2M4 12h2M18 12h2M6.3 6.3l1.4 1.4M16.3 16.3l1.4 1.4M6.3 17.7l1.4-1.4M16.3 7.7l1.4-1.4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>' },
    { id: 'folder', label: 'New folder', svg: '<path d="M4 6h6l2 2h8v10H4z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M12 12v4M10 14h4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>' },
    { id: 'grid', label: 'Apps', svg: '<circle cx="7" cy="7" r="1.6" fill="currentColor"/><circle cx="17" cy="7" r="1.6" fill="currentColor"/><circle cx="7" cy="17" r="1.6" fill="currentColor"/><circle cx="17" cy="17" r="1.6" fill="currentColor"/>' },
    { id: 'sparkle', label: 'Generate', svg: '<path d="M12 3l1.3 4.7L18 9l-4.7 1.3L12 15l-1.3-4.7L6 9l4.7-1.3L12 3z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/><path d="M19 15l.6 2.4L22 18l-2.4.6L19 21l-.6-2.4L16 18l2.4-.6L19 15z" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/>' }
  ];
  const SLOT_KEYS = ['s1', 's2', 's3', 's4', 's5', 's6'];
  const SLOTS_KEY = 'codexmicro-slots';
  let slotAssign = JSON.parse(localStorage.getItem(SLOTS_KEY) || '{}');
  let pendingIconId = null;

  const slotList = document.getElementById('slotList');
  const iconLib = document.getElementById('iconLib');

  function saveSlots() { localStorage.setItem(SLOTS_KEY, JSON.stringify(slotAssign)); }
  function iconById(id) { return ICON_LIBRARY.find((i) => i.id === id); }

  function applySlotAssignments() {
    SLOT_KEYS.forEach((slot) => {
      const el = document.querySelector(`.switch[data-key="${slot}"]`);
      if (!el) return;
      const icon = iconById(slotAssign[slot]);
      if (icon) {
        el.classList.add('assigned');
        el.innerHTML = `<svg class="switch-icon" viewBox="0 0 24 24">${icon.svg}</svg>`;
      } else {
        el.classList.remove('assigned');
        el.innerHTML = '<span class="switch-led"></span>';
      }
    });
  }

  function renderIconLib() {
    iconLib.innerHTML = '';
    ICON_LIBRARY.forEach((icon) => {
      const btn = document.createElement('button');
      btn.className = 'icon-tile' + (pendingIconId === icon.id ? ' selected' : '');
      btn.title = icon.label;
      btn.draggable = true;
      btn.innerHTML = `<svg viewBox="0 0 24 24">${icon.svg}</svg>`;
      btn.addEventListener('click', () => {
        pendingIconId = pendingIconId === icon.id ? null : icon.id;
        renderPanelKeysTab();
        if (pendingIconId) log(`"${icon.label}" selected — click a panel slot below to place it`);
      });
      btn.addEventListener('dragstart', (e) => {
        e.dataTransfer.setData('text/plain', icon.id);
        e.dataTransfer.effectAllowed = 'copy';
        btn.classList.add('dragging');
      });
      btn.addEventListener('dragend', () => btn.classList.remove('dragging'));
      iconLib.appendChild(btn);
    });
  }

  function renderSlotList() {
    slotList.innerHTML = '';
    SLOT_KEYS.forEach((slot, i) => {
      const row = document.createElement('div');
      row.className = 'slot-row';
      row.style.cursor = pendingIconId ? 'pointer' : 'default';

      const icon = iconById(slotAssign[slot]);
      const swatch = document.createElement('span');
      swatch.className = 'slot-swatch';
      swatch.innerHTML = icon ? `<svg viewBox="0 0 24 24">${icon.svg}</svg>` : '';

      const name = document.createElement('span');
      name.className = 'slot-name';
      name.innerHTML = icon ? icon.label : `<span class="slot-empty">Empty slot ${i + 1}</span>`;

      const clearBtn = document.createElement('button');
      clearBtn.className = 'slot-clear';
      clearBtn.textContent = 'Clear';
      clearBtn.disabled = !icon;
      clearBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        delete slotAssign[slot];
        saveSlots();
        renderPanelKeysTab();
        applySlotAssignments();
        log(`cleared panel slot ${i + 1}`);
      });

      row.append(swatch, name, clearBtn);
      row.addEventListener('click', () => {
        if (!pendingIconId) return;
        slotAssign[slot] = pendingIconId;
        saveSlots();
        const placed = iconById(pendingIconId);
        log(`placed "${placed.label}" on panel slot ${i + 1}`);
        pendingIconId = null;
        renderPanelKeysTab();
        applySlotAssignments();
      });
      row.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';
        row.classList.add('drop-target');
      });
      row.addEventListener('dragleave', () => row.classList.remove('drop-target'));
      row.addEventListener('drop', (e) => {
        e.preventDefault();
        row.classList.remove('drop-target');
        const droppedId = e.dataTransfer.getData('text/plain');
        const dropped = iconById(droppedId);
        if (!dropped) return;
        slotAssign[slot] = droppedId;
        saveSlots();
        log(`placed "${dropped.label}" on panel slot ${i + 1}`);
        pendingIconId = null;
        renderPanelKeysTab();
        applySlotAssignments();
      });
      slotList.appendChild(row);
    });
  }

  function renderPanelKeysTab() { renderSlotList(); renderIconLib(); }

  // clicking an assigned switch slot on the physical panel fires its icon's action;
  // an unassigned (blank) slot just toggles its indicator LED
  document.querySelectorAll('.switch').forEach((el) => {
    bindKey(el, {
      onUp: () => {
        const icon = iconById(slotAssign[el.dataset.key]);
        if (icon) log(`${icon.label} triggered`);
        else el.classList.toggle('active');
      }
    });
  });
  applySlotAssignments();

  // ---------------- agents tab ----------------

  const AGENTS = [
    { id: 'claude', name: 'Claude Code', desc: "Anthropic's CLI coding agent.", mark: 'C' },
    { id: 'codex', name: 'Codex', desc: "A CLI coding agent.", mark: 'X' },
    { id: 'antigravity', name: 'Antigravity', desc: 'An agentic IDE runtime.', mark: 'A' }
  ];
  const AGENT_KEY = 'codexmicro-agent';
  let activeAgent = localStorage.getItem(AGENT_KEY) || 'claude';
  const agentList = document.getElementById('agentList');

  function renderAgentList() {
    agentList.innerHTML = '';
    AGENTS.forEach((a) => {
      const card = document.createElement('button');
      card.className = 'agent-card' + (activeAgent === a.id ? ' selected' : '');
      card.innerHTML = `
        <span class="agent-mark ${a.id}">${a.mark}</span>
        <span class="agent-body">
          <span class="agent-name">${a.name}</span>
          <span class="agent-desc">${a.desc}</span>
        </span>
        <span class="agent-check"></span>`;
      card.addEventListener('click', () => {
        activeAgent = a.id;
        localStorage.setItem(AGENT_KEY, activeAgent);
        renderAgentList();
        playClick('down');
        log(`agent target set → ${a.name}`);
      });
      agentList.appendChild(card);
    });
  }
  renderAgentList();

  // ---------------- appearance tab ----------------

  const ACCENTS = [
    { id: 'blue', color: '#6d8cff' },
    { id: 'purple', color: '#a06dff' },
    { id: 'green', color: '#3ecf8e' },
    { id: 'amber', color: '#ffb545' },
    { id: 'pink', color: '#ff6db3' }
  ];
  const ACCENT_KEY = 'codexmicro-accent';
  let activeAccent = localStorage.getItem(ACCENT_KEY) || 'blue';
  const swatchRow = document.getElementById('swatchRow');
  const reduceMotionEl = document.getElementById('reduceMotion');

  function applyAccent() {
    const a = ACCENTS.find((x) => x.id === activeAccent) || ACCENTS[0];
    document.documentElement.style.setProperty('--accent', a.color);
    document.documentElement.style.setProperty('--accent-glow', a.color + '80');
  }
  function renderSwatches() {
    swatchRow.innerHTML = '';
    ACCENTS.forEach((a) => {
      const sw = document.createElement('button');
      sw.className = 'swatch' + (activeAccent === a.id ? ' selected' : '');
      sw.style.background = a.color;
      sw.title = a.id;
      sw.addEventListener('click', () => {
        activeAccent = a.id;
        localStorage.setItem(ACCENT_KEY, activeAccent);
        applyAccent();
        renderSwatches();
        playClick('down');
      });
      swatchRow.appendChild(sw);
    });
  }
  applyAccent();
  renderSwatches();

  const REDUCE_MOTION_KEY = 'codexmicro-reduce-motion';
  reduceMotionEl.checked = JSON.parse(localStorage.getItem(REDUCE_MOTION_KEY) || 'false');
  document.body.classList.toggle('reduce-motion', reduceMotionEl.checked);
  reduceMotionEl.addEventListener('change', () => {
    localStorage.setItem(REDUCE_MOTION_KEY, JSON.stringify(reduceMotionEl.checked));
    document.body.classList.toggle('reduce-motion', reduceMotionEl.checked);
  });

  // debug console: optional, off by default
  const CONSOLE_VISIBLE_KEY = 'codexmicro-console-visible';
  const consoleToggleEl = document.getElementById('consoleToggle');
  consoleToggleEl.checked = JSON.parse(localStorage.getItem(CONSOLE_VISIBLE_KEY) || 'false');
  consoleEl.classList.toggle('visible', consoleToggleEl.checked);
  consoleToggleEl.addEventListener('change', () => {
    localStorage.setItem(CONSOLE_VISIBLE_KEY, JSON.stringify(consoleToggleEl.checked));
    consoleEl.classList.toggle('visible', consoleToggleEl.checked);
  });

  // initial render for tabs not open by default
  renderPanelKeysTab();

  log('scroll the dial, drag the stick, hold your bound mic key to talk.');
  log('press the ⚙ key to rebind keys, assign panel icons, or pick your agent.');
})();
