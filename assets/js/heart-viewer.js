// No Three.js or GLB request is made until the visitor chooses the 3D view.
let libraries;
function loadLibraries() {
  if (!libraries) {
    libraries = Promise.all([
      import('https://cdn.skypack.dev/three@0.132.2'),
      import('https://cdn.skypack.dev/three@0.132.2/examples/jsm/loaders/GLTFLoader.js'),
      import('https://cdn.skypack.dev/three@0.132.2/examples/jsm/controls/OrbitControls.js'),
    ]).catch((error) => { libraries = null; throw error; });
  }
  return libraries;
}

// One cancellable frame chain; visibility and motion preferences are separate.
export function createHeartRenderLoop({ render, shouldRender, shouldAnimate, requestFrame, cancelFrame }) {
  let frame = null;
  let disposed = false;
  const stop = () => {
    if (frame !== null) cancelFrame(frame);
    frame = null;
  };
  const schedule = () => {
    if (!disposed && frame === null && shouldRender() && shouldAnimate()) frame = requestFrame(tick);
  };
  const tick = () => {
    frame = null;
    if (disposed || !shouldRender()) return;
    render();
    schedule();
  };
  return {
    sync() {
      if (disposed || !shouldRender()) { stop(); return; }
      render();
      if (shouldAnimate()) schedule(); else stop();
    },
    stop,
    dispose() { disposed = true; stop(); },
  };
}

export function initViewer(root) {
  if (root.dataset.heartBound) return;
  root.dataset.heartBound = 'true';
  const viewer = root.querySelector('[data-heart-viewer]');
  const poster = root.querySelector('[data-heart-poster]');
  const status = root.querySelector('[data-heart-status]');
  const load = root.querySelector('[data-heart-load]');
  const motion = root.querySelector('[data-heart-motion]');
  const hint = root.querySelector('[data-heart-hint]');
  if (!viewer || !poster || !status || !load || !motion) return;

  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  let visible = false;
  let state = 'idle';
  let userPaused = false;
  let generation = 0;
  let renderer, controls, scene, camera, loop, model;
  let resizeObserver, themeObserver;
  const removeListeners = [];
  const setState = (value) => { state = value; root.dataset.heartState = value; };
  setState('idle');

  const canRender = () => state === 'ready' && visible && !document.hidden && root.isConnected;
  const updateMotionLabel = () => {
    motion.textContent = controls?.autoRotate ? root.dataset.pauseLabel : root.dataset.playLabel;
  };
  const render = () => {
    if (controls.autoRotate) controls.update();
    renderer.render(scene, camera);
  };
  const listen = (target, name, handler, options) => {
    target.addEventListener(name, handler, options);
    removeListeners.push(() => target.removeEventListener(name, handler, options));
  };
  const disposeTree = (object) => object?.traverse((node) => {
    if (!node.isMesh) return;
    node.geometry?.dispose();
    for (const material of Array.isArray(node.material) ? node.material : [node.material]) {
      for (const value of Object.values(material || {})) if (value?.isTexture) value.dispose();
      material?.dispose();
    }
  });
  const disposeModel = () => {
    loop?.dispose();
    loop = null;
    resizeObserver?.disconnect();
    themeObserver?.disconnect();
    controls?.dispose();
    disposeTree(model);
    renderer?.dispose();
    renderer?.domElement.remove();
    renderer = controls = model = scene = camera = null;
  };
  const showError = () => {
    generation += 1;
    setState('error');
    disposeModel();
    viewer.removeAttribute('aria-busy');
    poster.hidden = false;
    motion.hidden = true;
    if (hint) hint.hidden = true;
    status.textContent = root.dataset.errorLabel;
    load.textContent = root.dataset.retryLabel;
    load.disabled = false;
    load.removeAttribute('aria-disabled');
    load.hidden = false;
  };

  const checkVisibility = () => {
    const box = viewer.getBoundingClientRect();
    visible = box.bottom > 0 && box.top < window.innerHeight && box.right > 0 && box.left < window.innerWidth;
    loop?.sync();
  };
  let visibilityObserver;
  if ('IntersectionObserver' in window) {
    visibilityObserver = new IntersectionObserver((entries) => {
      visible = entries.some((entry) => entry.isIntersecting && entry.intersectionRatio > 0);
      loop?.sync();
    }, { rootMargin: '0px', threshold: 0.01 });
    visibilityObserver.observe(viewer);
  } else {
    listen(window, 'scroll', checkVisibility, { passive: true });
    listen(window, 'resize', checkVisibility, { passive: true });
  }
  checkVisibility();
  listen(document, 'visibilitychange', () => loop?.sync());

  const onPreferenceChange = () => {
    if (!controls) return;
    controls.autoRotate = !preference.matches && !userPaused;
    controls.enableDamping = controls.autoRotate;
    updateMotionLabel();
    loop?.sync();
  };
  if (preference.addEventListener) listen(preference, 'change', onPreferenceChange);
  else if (preference.addListener) {
    preference.addListener(onPreferenceChange);
    removeListeners.push(() => preference.removeListener(onPreferenceChange));
  }
  listen(motion, 'click', () => {
    if (state !== 'ready') return;
    controls.autoRotate = !controls.autoRotate;
    userPaused = !controls.autoRotate;
    controls.enableDamping = controls.autoRotate;
    updateMotionLabel();
    loop.sync();
  });

  listen(load, 'click', async () => {
    if (state === 'loading' || state === 'ready') return;
    const attempt = ++generation;
    setState('loading');
    load.setAttribute('aria-disabled', 'true');
    status.textContent = root.dataset.loadingLabel;
    viewer.setAttribute('aria-busy', 'true');
    try {
      // Detect unsupported WebGL before requesting remote modules or a GLB.
      const probe = document.createElement('canvas');
      const context = probe.getContext('webgl2') || probe.getContext('webgl');
      if (!context) throw new Error('WebGL unavailable');
      context.getExtension('WEBGL_lose_context')?.loseContext();
      const [THREE, { GLTFLoader }, { OrbitControls }] = await loadLibraries();
      if (attempt !== generation || !root.isConnected) return;
      scene = new THREE.Scene();
      const isDark = () => document.documentElement.classList.contains('dark');
      const updateTheme = () => {
        if (!scene) return;
        const color = isDark() ? 0x1f2937 : 0xffffff;
        scene.background = new THREE.Color(color);
        loop?.sync();
      };
      updateTheme();
      const width = Math.max(1, viewer.clientWidth);
      const height = Math.max(1, viewer.clientHeight);
      camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
      camera.position.set(0, 0, 5);
      const ratio = Math.min(window.devicePixelRatio || 1, 2);
      renderer = new THREE.WebGLRenderer({ antialias: ratio <= 1, alpha: true });
      renderer.setPixelRatio(ratio);
      renderer.setSize(width, height);
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;
      renderer.outputEncoding = THREE.sRGBEncoding;
      renderer.domElement.style.position = 'absolute';
      renderer.domElement.style.inset = '0';
      renderer.domElement.tabIndex = 0;
      renderer.domElement.setAttribute('role', 'img');
      if (hint?.id) renderer.domElement.setAttribute('aria-describedby', hint.id);
      renderer.domElement.setAttribute('aria-label', viewer.getAttribute('aria-label'));
      renderer.domElement.addEventListener('webglcontextlost', () => {
        if (attempt === generation) showError();
      }, { once: true });
      viewer.prepend(renderer.domElement);
      controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = !preference.matches;
      controls.dampingFactor = 0.05;
      controls.enableZoom = true;
      controls.autoRotate = !preference.matches && !userPaused;
      controls.autoRotateSpeed = 1;
      controls.addEventListener('change', () => { if (!controls.autoRotate) loop?.sync(); });
      scene.add(new THREE.AmbientLight(0xffffff, 1.2));
      const light = new THREE.DirectionalLight(0xffffff, 1.5);
      light.position.set(5, 10, 7);
      light.castShadow = true;
      scene.add(light);
      const fill = new THREE.DirectionalLight(0xe3e3e3, 1);
      fill.position.set(-5, 0, 5);
      scene.add(fill);
      const loadedModel = await new Promise((resolve, reject) => {
        new GLTFLoader().load(root.dataset.modelUrl, (gltf) => resolve(gltf.scene), undefined, reject);
      });
      if (attempt !== generation || !root.isConnected) { disposeTree(loadedModel); return; }
      model = loadedModel;
      model.traverse((node) => {
        if (node.isMesh) { node.castShadow = true; node.receiveShadow = true; }
      });
      const box = new THREE.Box3().setFromObject(model);
      const size = box.getSize(new THREE.Vector3());
      model.position.sub(box.getCenter(new THREE.Vector3()));
      scene.add(model);
      const extent = Math.max(size.y, size.x / camera.aspect, size.z);
      const distance = extent * 1.2 / (2 * Math.tan(camera.fov * Math.PI / 360));
      camera.position.set(0, 0, distance);
      camera.near = Math.max(distance / 100, 0.001);
      camera.far = distance * 100;
      camera.updateProjectionMatrix();
      controls.target.set(0, 0, 0);
      controls.minDistance = distance * 0.6;
      controls.maxDistance = distance * 2.5;
      controls.update();
      setState('ready');
      loop = createHeartRenderLoop({
        render, shouldRender: canRender, shouldAnimate: () => controls.autoRotate,
        requestFrame: (callback) => window.requestAnimationFrame(callback),
        cancelFrame: (id) => window.cancelAnimationFrame(id),
      });
      renderer.domElement.addEventListener('keydown', (event) => {
        if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', '+', '=', '-', '−'].includes(event.key)) return;
        event.preventDefault();
        userPaused = true;
        controls.autoRotate = false;
        controls.enableDamping = false;
        const offset = camera.position.clone().sub(controls.target);
        const spherical = new THREE.Spherical().setFromVector3(offset);
        if (event.key === 'ArrowLeft') spherical.theta -= 0.12;
        if (event.key === 'ArrowRight') spherical.theta += 0.12;
        if (event.key === 'ArrowUp') spherical.phi -= 0.12;
        if (event.key === 'ArrowDown') spherical.phi += 0.12;
        if (event.key === '+' || event.key === '=') spherical.radius *= 0.9;
        if (event.key === '-' || event.key === '−') spherical.radius *= 1.1;
        spherical.phi = Math.max(0.01, Math.min(Math.PI - 0.01, spherical.phi));
        spherical.radius = Math.max(controls.minDistance, Math.min(controls.maxDistance, spherical.radius));
        camera.position.setFromSpherical(spherical).add(controls.target);
        controls.update();
        updateMotionLabel();
        loop.sync();
      });
      const resize = () => {
        if (!renderer || !camera) return;
        const width = Math.max(1, viewer.clientWidth);
        const height = Math.max(1, viewer.clientHeight);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
        loop.sync();
      };
      if ('ResizeObserver' in window) {
        resizeObserver = new ResizeObserver(resize);
        resizeObserver.observe(viewer);
      } else listen(window, 'resize', resize, { passive: true });
      themeObserver = new MutationObserver(updateTheme);
      themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
      const returnFocus = document.activeElement === load;
      poster.hidden = true;
      load.hidden = true;
      load.disabled = false;
      load.removeAttribute('aria-disabled');
      motion.hidden = false;
      if (hint) hint.hidden = false;
      status.textContent = '';
      viewer.removeAttribute('aria-busy');
      updateMotionLabel();
      checkVisibility();
      // The action remains keyboard reachable when the load button is hidden.
      if (returnFocus) motion.focus({ preventScroll: true });
    } catch (error) {
      if (attempt !== generation) return;
      console.warn('3D heart view unavailable', error);
      showError();
    }
  });
  load.hidden = false;

  listen(window, 'pagehide', (event) => {
    loop?.stop();
    if (event.persisted) return;
    generation += 1;
    setState('disposed');
    disposeModel();
    visibilityObserver?.disconnect();
    for (const remove of removeListeners) remove();
  });
  listen(window, 'pageshow', () => { checkVisibility(); loop?.sync(); });
}

if (typeof document !== 'undefined') {
  for (const root of document.querySelectorAll('[data-heart-model]')) initViewer(root);
}
