// Install with tab-scoped Page.addScriptToEvaluateOnNewDocument before reload.
// Instrumentation only; no score, TBT or INP is inferred from these observations.
(() => {
  const result = { lcp: [], shifts: [], longTasks: [], errors: [] };
  window.__drcilPerformanceObservation = result;
  const observe = (type, read) => {
    try { new PerformanceObserver((list) => list.getEntries().forEach(read)).observe({ type, buffered: true }); }
    catch (error) { result.errors.push({ type, message: String(error) }); }
  };
  observe('largest-contentful-paint', (e) => result.lcp.push({ startTime: e.startTime, renderTime: e.renderTime, loadTime: e.loadTime, size: e.size, url: e.url, element: e.element?.tagName || null, className: e.element?.className || null }));
  observe('layout-shift', (e) => result.shifts.push({ startTime: e.startTime, value: e.value, hadRecentInput: e.hadRecentInput, sources: (e.sources || []).map((s) => ({ tag: s.node?.tagName || null, previousRect: s.previousRect?.toJSON?.() || s.previousRect, currentRect: s.currentRect?.toJSON?.() || s.currentRect })) }));
  observe('longtask', (e) => result.longTasks.push({ startTime: e.startTime, duration: e.duration, name: e.name }));
})();
