import * as PIXI from 'pixi.js';

// Get the canvas element
const canvas = document.getElementById('slime-bg');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// PixiJS Application
const app = new PIXI.Application({
  view: canvas,
  width: window.innerWidth,
  height: window.innerHeight,
  resizeTo: window,
  backgroundAlpha: 0,
  antialias: true,
  autoDensity: true,
});

// Create a gradient texture
function createGradientTexture(width, height) {
  const gradCanvas = document.createElement('canvas');
  gradCanvas.width = width;
  gradCanvas.height = height;
  const ctx = gradCanvas.getContext('2d');
  const grad = ctx.createLinearGradient(0, 0, width, height);
  grad.addColorStop(0, '#7F7FD5');
  grad.addColorStop(0.5, '#86A8E7');
  grad.addColorStop(1, '#91EAE4');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, width, height);
  return PIXI.Texture.from(gradCanvas);
}

let gradientSprite = new PIXI.Sprite(createGradientTexture(window.innerWidth, window.innerHeight));
gradientSprite.width = window.innerWidth;
gradientSprite.height = window.innerHeight;
app.stage.addChild(gradientSprite);

// Slime shader (fragment)
const slimeFrag = `
varying vec2 vTextureCoord;
uniform sampler2D uSampler;
uniform vec2 mouse;
uniform float time;
void main() {
    vec2 uv = vTextureCoord;
    float dist = distance(uv, mouse);
    float strength = 0.18 / (dist * 8.0 + 0.18);
    float angle = atan(mouse.y - uv.y, mouse.x - uv.x);
    uv.x += cos(angle) * strength * 0.18;
    uv.y += sin(angle) * strength * 0.18;
    // Wobble
    uv.x += sin(time * 0.7 + uv.y * 8.0) * 0.01;
    uv.y += cos(time * 0.5 + uv.x * 8.0) * 0.01;
    gl_FragColor = texture2D(uSampler, uv);
}
`;

// Custom filter
const slimeFilter = new PIXI.Filter(undefined, slimeFrag, {
  mouse: [0.5, 0.5],
  time: 0,
});
gradientSprite.filters = [slimeFilter];

// Mouse tracking
let mouse = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
canvas.addEventListener('mousemove', (e) => {
  const rect = canvas.getBoundingClientRect();
  mouse.x = e.clientX - rect.left;
  mouse.y = e.clientY - rect.top;
});
window.addEventListener('touchmove', (e) => {
  if (e.touches && e.touches.length > 0) {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.touches[0].clientX - rect.left;
    mouse.y = e.touches[0].clientY - rect.top;
  }
}, { passive: false });

// Responsive
window.addEventListener('resize', () => {
  gradientSprite.texture = createGradientTexture(window.innerWidth, window.innerHeight);
  gradientSprite.width = window.innerWidth;
  gradientSprite.height = window.innerHeight;
});

// Blob/trail effect
const TRAIL_LENGTH = 18;
let trail = Array.from({ length: TRAIL_LENGTH }, () => ({ x: mouse.x, y: mouse.y }));
const blobGraphics = new PIXI.Graphics();
app.stage.addChild(blobGraphics);

app.ticker.add((delta) => {
  // Update shader uniforms
  slimeFilter.uniforms.mouse = [mouse.x / window.innerWidth, mouse.y / window.innerHeight];
  slimeFilter.uniforms.time += delta / 60;

  // Update trail
  trail.unshift({ x: mouse.x, y: mouse.y });
  if (trail.length > TRAIL_LENGTH) trail.pop();

  // Draw blob/trail
  blobGraphics.clear();
  for (let i = 0; i < trail.length; i++) {
    const t = trail[i];
    const alpha = 0.12 * (1 - i / TRAIL_LENGTH);
    const radius = 38 * (1 - i / TRAIL_LENGTH) + 12;
    blobGraphics.beginFill(0x91EAE4, alpha);
    blobGraphics.drawCircle(t.x, t.y, radius);
    blobGraphics.endFill();
  }
  // Main cursor blob
  blobGraphics.beginFill(0xFFFFFF, 0.18);
  blobGraphics.drawCircle(mouse.x, mouse.y, 44);
  blobGraphics.endFill();
}); 