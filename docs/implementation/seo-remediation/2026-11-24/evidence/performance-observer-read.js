// Read at a consistent 12,000ms navigation-time horizon; use awaitPromise=true.
(async () => {
  const horizon = 12000;
  if (performance.now() < horizon) await new Promise((resolve) => setTimeout(resolve, horizon - performance.now()));
  const raw = window.__drcilPerformanceObservation || { lcp: [], shifts: [], longTasks: [], errors: ['observer not installed before navigation'] };
  const shifts = raw.shifts.filter((s) => !s.hadRecentInput && s.startTime <= horizon).sort((a, b) => a.startTime - b.startTime);
  let cls = 0, score = 0, start = 0, previous = -Infinity;
  for (const e of shifts) {
    if (e.startTime - previous > 1000 || e.startTime - start > 5000) { score = e.value; start = e.startTime; }
    else score += e.value;
    previous = e.startTime;
    cls = Math.max(cls, score);
  }
  const nav = performance.getEntriesByType('navigation')[0]?.toJSON() || null;
  const resources = performance.getEntriesByType('resource').filter((e) => e.startTime <= horizon).map((e) => ({ name: e.name, initiatorType: e.initiatorType, startTime: e.startTime, duration: e.duration, transferSize: e.transferSize, encodedBodySize: e.encodedBodySize, decodedBodySize: e.decodedBodySize, responseEnd: e.responseEnd }));
  const lcp = raw.lcp.filter((e) => e.startTime <= horizon).at(-1) || null;
  return {
    url: location.href, timestampUtc: new Date().toISOString(), horizonMs: horizon, sampledAtMs: performance.now(),
    userAgent: navigator.userAgent, viewport: { width: innerWidth, height: innerHeight, dpr: devicePixelRatio },
    navigation: nav, paints: performance.getEntriesByType('paint').map((e) => e.toJSON()), lcp,
    clsMaxSessionWindowWithinHorizon: cls, layoutShifts: shifts,
    longTasks: raw.longTasks.filter((e) => e.startTime <= horizon), resources,
    domElements: document.getElementsByTagName('*').length,
    viewerStates: [...document.querySelectorAll('[data-heart-model]')].map((e) => ({ state: e.dataset.heartState, canvas: !!e.querySelector('canvas') })),
    observerErrors: raw.errors,
    limits: ['CDP laboratory observation; not Lighthouse or field p75.', 'No TBT/INP, GPU attribution or score inferred.', 'Cross-origin transferSize=0 may mean missing Timing-Allow-Origin or cache; not zero network cost.', 'Browser cache disabled does not flush DNS/TLS/OS/CDN caches.']
  };
})();
