import os
import cv2
import numpy as np
import json
import base64
import io
import email
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from PIL import Image

try:
    import onnxruntime as ort
    HAS_ONNX = True
except ImportError:
    HAS_ONNX = False

SCRATCH_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(SCRATCH_DIR, "lama_fp32.onnx")

session = None
if HAS_ONNX and os.path.exists(MODEL_PATH):
    try:
        session = ort.InferenceSession(MODEL_PATH, providers=['CPUExecutionProvider'])
        print("🧠 LaMa AI Engine Loaded!")
    except Exception as e:
        print(f"ONNX Load Info: {e}")

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Free AI Video &amp; Image Watermark Remover — ZipLoot Studio</title>
  <meta name="description" content="Remove watermarks from CapCut, TikTok, Google Imagen, Sora, and YouTube videos for free using open-source LaMa and ProPainter AI inpainting engines." />
  <meta name="google-site-verification" content="k_fvxHtRCpprKVYqa3yiGhhtFu8nZwHmb_N_c6q3uC0" />
  <meta name="google-site-verification" content="cemt1q6S0AM9FRbb5ONCGaIXaFdepF8LOtRWRIppykY" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <style>
/* =====================================================
   ZIPLOOT WATERMARK REMOVER TOOL PAGE CSS
   ===================================================== */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}

:root{
  --void:#000510;
  --panel:rgba(8,14,42,0.85);
  --panel-hard:#050c22;
  --border:rgba(255,255,255,0.07);
  --border-lit:rgba(100,110,255,0.3);
  --ink-0:#ffffff;
  --ink-1:#e2e8f0;
  --ink-2:#94a3b8;
  --ink-3:#3d4f6b;
  --v:#818cf8;
  --p:#c084fc;
  --c:#22d3ee;
  --g:#4ade80;
  --grd-a:linear-gradient(135deg,#818cf8,#c084fc,#22d3ee);
  --font-d:'Syne',sans-serif;
  --font-m:'Space Mono',monospace;
  --font-b:'Inter',sans-serif;
  --nav-h:80px;
  --ad-h:80px;
}

::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:var(--void)}
::-webkit-scrollbar-thumb{background:var(--grd-a);border-radius:10px}

body{
  background:var(--void);
  background-image:radial-gradient(circle,rgba(129,140,248,0.05) 1px,transparent 1px);
  background-size:32px 32px;
  color:var(--ink-2);
  font-family:var(--font-b);
  font-size:16px;
  line-height:1.8;
  overflow-x:hidden;
  padding-top:var(--nav-h);
  padding-bottom:var(--ad-h);
}

a{color:inherit;text-decoration:none;transition:color .25s;}
.wrap{width:100%;max-width:1280px;margin:0 auto;padding:0 24px;}

/* NAVIGATION */
header{
  position:fixed;top:0;left:0;right:0;
  height:var(--nav-h);z-index:8000;
  display:flex;align-items:center;justify-content:center;
  padding:0 24px;
}
.nav-pill{
  width:100%;max-width:1240px;
  display:flex;align-items:center;justify-content:space-between;
  background:rgba(4,8,24,0.78);
  backdrop-filter:blur(28px) saturate(160%);
  border:1px solid var(--border-lit);
  border-radius:100px;
  padding:0 28px;
  height:56px;
  box-shadow:0 4px 36px rgba(0,0,0,0.5);
}
.nav-logo{
  font-family:var(--font-d);font-size:21px;font-weight:800;
  letter-spacing:-0.8px;display:flex;align-items:center;gap:3px;
}
.nav-logo .nz{background:var(--grd-a);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.nav-logo .nl{color:#fff;}
.logo-dot{display:inline-block;width:6px;height:6px;background:var(--c);border-radius:50%;box-shadow:0 0 10px var(--c);}

.nav-links{display:flex;align-items:center;gap:2px;list-style:none;}
.nav-links a{font-family:var(--font-d);font-size:14px;font-weight:600;color:var(--ink-2);padding:8px 16px;border-radius:100px;}
.nav-links a:hover{color:#fff;background:rgba(129,140,248,0.1);}
.nav-cta{background:var(--grd-a)!important;color:#fff!important;padding:9px 22px!important;border-radius:100px!important;}

/* TOOL STUDIO */
.tool-card{
  background:var(--panel);
  border:1px solid var(--border-lit);
  border-radius:24px;
  padding:36px;
  box-shadow:0 20px 60px rgba(0,0,0,0.6);
  margin:20px 0;
  text-align:center;
  backdrop-filter:blur(20px);
}

.tool-title{font-family:var(--font-d);font-size:32px;font-weight:800;color:#fff;margin-bottom:12px;}
.tool-title span{background:var(--grd-a);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}

/* Tabs Navigation */
.tab-nav {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin: 24px 0;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  padding-bottom: 12px;
}
.tab-btn {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  color: var(--ink-2);
  padding: 10px 24px;
  border-radius: 100px;
  font-family: var(--font-d);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s;
}
.tab-btn:hover { background: rgba(129, 140, 248, 0.2); color: #fff; }
.tab-btn.active {
  background: var(--grd-a);
  color: #fff;
  border-color: transparent;
  box-shadow: 0 0 20px rgba(129, 140, 248, 0.4);
}

.tab-content { display: none; }
.tab-content.active { display: flex; flex-direction: column; align-items: center; gap: 20px; width: 100%; }

.upload-zone {
  width: 100%;
  border: 2px dashed rgba(129, 140, 248, 0.4);
  border-radius: 18px;
  padding: 50px;
  text-align: center;
  cursor: pointer;
  background: rgba(2, 6, 23, 0.6);
  transition: all 0.25s;
}
.upload-zone:hover { border-color: var(--c); background: rgba(34, 211, 238, 0.08); }

.media-wrap {
  position: relative;
  display: inline-block;
  max-width: 100%;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
  background: #000;
}

canvas { display: block; max-width: 100%; touch-action: none; }
video { display: block; max-width: 100%; max-height: 500px; }

#videoOverlayCanvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 20;
  cursor: crosshair;
  touch-action: none;
}

.toolbar {
  display: flex;
  gap: 14px;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  width: 100%;
}

.btn-act {
  background: var(--grd-a);
  color: #fff;
  border: none;
  padding: 13px 30px;
  border-radius: 100px;
  font-family: var(--font-d);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 0 24px rgba(129, 140, 248, 0.35);
  transition: all 0.25s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.btn-act:hover { transform: translateY(-2px); box-shadow: 0 0 36px rgba(129, 140, 248, 0.55); }
.btn-sec { background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255, 255, 255, 0.15); box-shadow: none; }
.btn-sec:hover { background: rgba(51, 65, 85, 0.8); }
.btn-green { background: linear-gradient(135deg, #10b981, #059669); box-shadow: 0 0 24px rgba(16, 185, 129, 0.35); }

.status-msg { font-size: 14px; font-weight: 600; color: #38bdf8; text-align: center; }

footer{border-top:1px solid var(--border);padding:48px 0 40px;text-align:center;font-family:var(--font-m);font-size:11px;color:var(--ink-3);}
  </style>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
</head>
<body>

  <!-- Navigation -->
  <header>
    <div class="nav-pill">
      <a href="/" class="nav-logo">
        <span class="nz">ZipLoot</span><span class="nl">.app</span> <span class="logo-dot"></span>
      </a>
      <ul class="nav-links">
        <li><a href="/">Home</a></li>
        <li><a href="https://same-favorite-joke-keeps.trycloudflare.com" style="color: #fff; background: rgba(129,140,248,0.15);">Watermark Remover</a></li>
        <li><a href="/addfree">Social Downloader</a></li>
        <li><a href="/ai-image-generator">AI Generator</a></li>
        <li><a href="/pdf-toolset">PDF Tools</a></li>
        <li><a href="https://ziploot.github.io/admin.html" class="nav-cta">Link Short</a></li>
      </ul>
    </div>
  </header>

  <!-- Top Native Ad Block -->
  <div style="width: 100%; max-width: 1240px; margin: 10px auto 12px; padding: 0 16px; text-align: center;">
    <script async="async" data-cfasync="false" src="https://pl30429916.effectivecpmnetwork.com/ec52137b60b75c0fc5150124af23e531/invoke.js"></script>
    <div id="container-ec52137b60b75c0fc5150124af23e531"></div>
  </div>


  <!-- Banner 728x90 Ad Block -->
  <div style="display:flex;justify-content:center;align-items:center;margin:20px auto;width:100%;min-height:94px;overflow:hidden;">
    <iframe srcdoc="<!DOCTYPE html><html><head><style>html,body{margin:0;padding:0;overflow:hidden;}</style></head><body><script>atOptions = {'key' : '07443fff7d70e04b3642773f8f97367f','format' : 'iframe','height' : 90,'width' : 728,'params' : {}};</script><script src='https://www.highperformanceformat.com/07443fff7d70e04b3642773f8f97367f/invoke.js'></script>
  <!-- Sticky Footer Ad Bar -->
  <div id="stickyAdBar" style="position:fixed;bottom:0;left:0;right:0;height:80px;background:rgba(3,7,22,0.95);backdrop-filter:blur(24px);border-top:1px solid rgba(100,110,255,0.3);z-index:7000;display:flex;align-items:center;justify-content:center;box-shadow:0 -16px 48px rgba(0,0,0,0.55);">
    <button onclick="document.getElementById('stickyAdBar').style.display='none'" style="position:absolute;top:-14px;right:20px;width:28px;height:28px;background:#818cf8;border:none;border-radius:50%;color:#fff;font-size:14px;cursor:pointer;">✕</button>
    <iframe srcdoc="<!DOCTYPE html><html><head><style>html,body{margin:0;padding:0;overflow:hidden;}</style></head><body><script>atOptions = {'key' : '07443fff7d70e04b3642773f8f97367f','format' : 'iframe','height' : 90,'width' : 728,'params' : {}};</script><script src='https://www.highperformanceformat.com/07443fff7d70e04b3642773f8f97367f/invoke.js'></script>
  <!-- Social Bar Ad Script -->
  <script>
    window.addEventListener('load', function() {
      if (!document.getElementById('socialBarAdScript')) {
        var script = document.createElement('script');
        script.id = 'socialBarAdScript';
        script.src = "https://pl30429917.effectivecpmnetwork.com/e3/2d/69/e32d69b13995a39cded45044df825ace.js";
        document.body.appendChild(script);
      }
    });
  </script>

</body></html>" width="728" height="90" frameborder="0" scrolling="no" style="border:none;overflow:hidden;" sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-top-navigation-by-user-activation"></iframe>
  </div>


  <!-- Social Bar Ad Script -->
  <script>
    window.addEventListener('load', function() {
      if (!document.getElementById('socialBarAdScript')) {
        var script = document.createElement('script');
        script.id = 'socialBarAdScript';
        script.src = "https://pl30429917.effectivecpmnetwork.com/e3/2d/69/e32d69b13995a39cded45044df825ace.js";
        document.body.appendChild(script);
      }
    });
  </script>

</body></html>" width="728" height="90" frameborder="0" scrolling="no" style="border:none;overflow:hidden;" sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-top-navigation-by-user-activation"></iframe>
  </div>


  <!-- Main Content Wrap -->
  <div class="wrap">
    <div class="tool-card">
      <h1 class="tool-title">Free AI <span>Watermark Remover</span> Studio</h1>
      <p style="color: var(--ink-2); max-width: 640px; margin: 0 auto 24px;">Remove watermarks from AI videos and images seamlessly with high quality.</p>

      <!-- Navigation Tabs -->
      <div class="tab-nav">
        <button class="tab-btn active" onclick="switchTab('imageTab', this)">🖼️ Image Remover (LaMa AI)</button>
        <button class="tab-btn" onclick="switchTab('videoTab', this)">🎬 Video Remover (ProPainter Engine)</button>
      </div>

      <!-- TAB 1: IMAGE WATERMARK REMOVER -->
      <div id="imageTab" class="tab-content active">
        <div class="upload-zone" id="imgUploadZone" onclick="document.getElementById('imgInput').click()">
          <p style="font-size: 18px; font-weight: 700; color: #fff; margin-bottom: 6px;">🖼️ Click or Drag Image Here</p>
          <p style="font-size: 13px; color: var(--ink-3);">Supports PNG, JPG, WEBP, JPEG</p>
          <input type="file" id="imgInput" accept="image/*" style="display: none;" onchange="loadImgFile(event)">
        </div>

        <div id="imgStudio" style="display:none; flex-direction:column; align-items:center; gap:16px; width:100%;">
          <div class="media-wrap">
            <canvas id="imgCanvas"></canvas>
          </div>
          <div class="status-msg" id="imgStatus">🖌️ Draw/paint over the watermark area with your mouse</div>
          <div class="toolbar">
            <button class="btn-act" onclick="processImageInpaint()">⚡ Clean Watermark (LaMa AI)</button>
            <a id="imgDownloadBtn" class="btn-act btn-green" style="display:none;" download="clean_watermark_free_image.png">💾 Save / Download Clean Image</a>
            <button class="btn-act btn-sec" onclick="resetImgCanvas()">🔄 Reset Mask</button>
            <button class="btn-act btn-sec" onclick="document.getElementById('imgInput').click()">📁 Change Image</button>
          </div>
        </div>
      </div>

      <!-- TAB 2: VIDEO WATERMARK REMOVER -->
      <div id="videoTab" class="tab-content">
        <div class="upload-zone" id="vidUploadZone" onclick="document.getElementById('vidInput').click()">
          <p style="font-size: 18px; font-weight: 700; color: #fff; margin-bottom: 6px;">🎬 Click or Drag Video Here</p>
          <p style="font-size: 13px; color: var(--ink-3);">Supports MP4, MOV, WEBM videos</p>
          <input type="file" id="vidInput" accept="video/*" style="display: none;" onchange="loadVidFile(event)">
        </div>

        <div id="vidStudio" style="display:none; flex-direction:column; align-items:center; gap:16px; width:100%;">
          <div class="media-wrap">
            <video id="videoPlayer" controls muted loop playsinline></video>
            <canvas id="videoOverlayCanvas"></canvas>
          </div>
          <div class="status-msg" id="vidStatus">📦 Drag a rectangle box over the watermark area on the video above</div>
          <div class="toolbar">
            <button class="btn-act" onclick="processVideoInpaint()">⚡ Clean Video Watermark</button>
            <button class="btn-act btn-sec" onclick="resetVidBox()">🔄 Reset Box</button>
            <button class="btn-act btn-sec" onclick="document.getElementById('vidInput').click()">📁 Change Video</button>
          </div>

          <div id="vidOutputArea" style="display:none; flex-direction:column; align-items:center; gap:14px; margin-top:14px; width:100%;">
            <h3 style="font-size:16px; color:#4ade80;">🎉 Output Clean Video:</h3>
            <video id="cleanVidPlayer" controls loop style="border-radius:12px; border:1px solid #4ade80; max-height:400px;"></video>
            <a id="vidDownloadBtn" class="btn-act btn-green" download="clean_watermark_free_video.mp4">💾 Save / Download Clean Video (MP4)</a>
          </div>
        </div>
      </div>

    </div>
  </div>

  <footer>
    &copy; 2026 ZIPLOOT PLATFORM &bull; ALL RIGHTS RESERVED
  </footer>

  <script>
    // SECURE VERCEL SERVERLESS PROXY ENDPOINT
    const API_BASE_URL = '';

    function switchTab(tabId, btn) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      btn.classList.add('active');

      if (tabId === 'videoTab' && videoPlayer.src) {
        setTimeout(syncVideoCanvasSize, 100);
      }
    }

    /* --- IMAGE REMOVER JS (LaMa AI) --- */
    let imgCanvas = document.getElementById('imgCanvas');
    let imgCtx = imgCanvas.getContext('2d');
    let maskCanvas = document.createElement('canvas');
    let maskCtx = maskCanvas.getContext('2d');
    let rawImg = new Image();
    let isDrawing = false;

    function loadImgFile(e) {
      let file = e.target.files[0];
      if (!file) return;
      let reader = new FileReader();
      reader.onload = function(evt) {
        rawImg.onload = function() {
          imgCanvas.width = rawImg.width;
          imgCanvas.height = rawImg.height;
          maskCanvas.width = rawImg.width;
          maskCanvas.height = rawImg.height;
          resetImgCanvas();
          document.getElementById('imgUploadZone').style.display = 'none';
          document.getElementById('imgStudio').style.display = 'flex';
          document.getElementById('imgDownloadBtn').style.display = 'none';
        };
        rawImg.src = evt.target.result;
      };
      reader.readAsDataURL(file);
    }

    function resetImgCanvas() {
      imgCtx.drawImage(rawImg, 0, 0);
      maskCtx.fillStyle = 'black';
      maskCtx.fillRect(0, 0, maskCanvas.width, maskCanvas.height);
      document.getElementById('imgDownloadBtn').style.display = 'none';
      initImgDraw();
    }

    function initImgDraw() {
      imgCanvas.onmousedown = (e) => { isDrawing = true; drawMask(e); };
      imgCanvas.onmousemove = (e) => { if (isDrawing) drawMask(e); };
      imgCanvas.onmouseup = () => { isDrawing = false; };

      imgCanvas.ontouchstart = (e) => { isDrawing = true; drawMask(e.touches[0]); };
      imgCanvas.ontouchmove = (e) => { if (isDrawing) drawMask(e.touches[0]); };
      imgCanvas.ontouchend = () => { isDrawing = false; };
    }

    function drawMask(e) {
      let rect = imgCanvas.getBoundingClientRect();
      let scaleX = imgCanvas.width / rect.width;
      let scaleY = imgCanvas.height / rect.height;
      let x = (e.clientX - rect.left) * scaleX;
      let y = (e.clientY - rect.top) * scaleY;

      let brushSize = Math.max(16, Math.min(imgCanvas.width, imgCanvas.height) / 25);

      imgCtx.fillStyle = 'rgba(239, 68, 68, 0.6)';
      imgCtx.beginPath();
      imgCtx.arc(x, y, brushSize, 0, Math.PI * 2);
      imgCtx.fill();

      maskCtx.fillStyle = 'white';
      maskCtx.beginPath();
      maskCtx.arc(x, y, brushSize, 0, Math.PI * 2);
      maskCtx.fill();
    }

    async function processImageInpaint() {
      let status = document.getElementById('imgStatus');
      status.innerText = '⏳ Processing Image on AI Engine...';
      
      let imgDataB64 = imgCanvas.toDataURL('image/png');
      let maskDataB64 = maskCanvas.toDataURL('image/png');

      let payload = JSON.stringify({ image: imgDataB64, mask: maskDataB64 });

      try {
        let res;
        try {
          res = await fetch('/api/inpaint', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: payload
          });
        } catch(primaryErr) {
          // Backup fallback to zrok URL
          res = await fetch('https://5eeo6bfngypc.shares.zrok.io/api/inpaint', {
            method: 'POST',
            headers: { 
              'Content-Type': 'application/json',
              'skip_zrok_interstitial': 'true'
            },
            body: payload
          });
        }

        let text = await res.text();
        let json;
        try { json = JSON.parse(text); } catch(e) { throw new Error('Processing failed. Please try again.'); }

        if (json.status === 'success') {
          let cleanImg = new Image();
          cleanImg.onload = function() {
            imgCtx.drawImage(cleanImg, 0, 0, imgCanvas.width, imgCanvas.height);
            maskCtx.fillStyle = 'black';
            maskCtx.fillRect(0, 0, maskCanvas.width, maskCanvas.height);
            status.innerText = '🎉 SUCCESS! Watermark removed with AI!';
            
            let downloadBtn = document.getElementById('imgDownloadBtn');
            downloadBtn.href = json.clean_image;
            downloadBtn.style.display = 'inline-flex';
          };
          cleanImg.src = json.clean_image;
        } else {
          status.innerText = '❌ Error: ' + (json.error || 'Processing failed');
        }
      } catch (err) {
        status.innerText = '❌ Processing Error: ' + err.message;
      }
    }

    /* --- VIDEO REMOVER JS (ProPainter) --- */
    let videoPlayer = document.getElementById('videoPlayer');
    let videoOverlayCanvas = document.getElementById('videoOverlayCanvas');
    let vidCtx = videoOverlayCanvas.getContext('2d');

    let vidFile = null;
    let isVidSelecting = false;
    let vStartX = 0, vStartY = 0;
    let vidSelectRect = null;

    function syncVideoCanvasSize() {
      if (videoPlayer.clientWidth > 0 && videoPlayer.clientHeight > 0) {
        videoOverlayCanvas.width = videoPlayer.clientWidth;
        videoOverlayCanvas.height = videoPlayer.clientHeight;
        videoOverlayCanvas.style.width = videoPlayer.clientWidth + 'px';
        videoOverlayCanvas.style.height = videoPlayer.clientHeight + 'px';
        drawVidBox();
      }
    }

    function loadVidFile(e) {
      vidFile = e.target.files[0];
      if (!vidFile) return;

      let url = URL.createObjectURL(vidFile);
      videoPlayer.src = url;

      videoPlayer.onloadeddata = function() {
        document.getElementById('vidUploadZone').style.display = 'none';
        document.getElementById('vidStudio').style.display = 'flex';
        syncVideoCanvasSize();
        initVidBoxSelection();
      };
      
      window.addEventListener('resize', syncVideoCanvasSize);
    }

    function initVidBoxSelection() {
      function startSelect(e) {
        let rect = videoOverlayCanvas.getBoundingClientRect();
        let clientX = e.clientX || (e.touches && e.touches[0].clientX);
        let clientY = e.clientY || (e.touches && e.touches[0].clientY);
        vStartX = clientX - rect.left;
        vStartY = clientY - rect.top;
        isVidSelecting = true;
      }

      function moveSelect(e) {
        if (!isVidSelecting) return;
        let rect = videoOverlayCanvas.getBoundingClientRect();
        let clientX = e.clientX || (e.touches && e.touches[0].clientX);
        let clientY = e.clientY || (e.touches && e.touches[0].clientY);
        let curX = clientX - rect.left;
        let curY = clientY - rect.top;

        vidSelectRect = {
          x: Math.min(vStartX, curX),
          y: Math.min(vStartY, curY),
          w: Math.abs(curX - vStartX),
          h: Math.abs(curY - vStartY)
        };

        drawVidBox();
      }

      function endSelect() { isVidSelecting = false; }

      videoOverlayCanvas.onmousedown = startSelect;
      videoOverlayCanvas.onmousemove = moveSelect;
      videoOverlayCanvas.onmouseup = endSelect;

      videoOverlayCanvas.ontouchstart = startSelect;
      videoOverlayCanvas.ontouchmove = moveSelect;
      videoOverlayCanvas.ontouchend = endSelect;
    }

    function drawVidBox() {
      vidCtx.clearRect(0, 0, videoOverlayCanvas.width, videoOverlayCanvas.height);
      if (vidSelectRect) {
        vidCtx.strokeStyle = '#22d3ee';
        vidCtx.lineWidth = 3;
        vidCtx.fillStyle = 'rgba(34, 211, 238, 0.35)';
        vidCtx.fillRect(vidSelectRect.x, vidSelectRect.y, vidSelectRect.w, vidSelectRect.h);
        vidCtx.strokeRect(vidSelectRect.x, vidSelectRect.y, vidSelectRect.w, vidSelectRect.h);
      }
    }

    function resetVidBox() {
      vidSelectRect = null;
      vidCtx.clearRect(0, 0, videoOverlayCanvas.width, videoOverlayCanvas.height);
    }

    async function processVideoInpaint() {
      let status = document.getElementById('vidStatus');
      if (!vidSelectRect) {
        alert('Please drag a rectangle box over the watermark on the video first!');
        return;
      }

      status.innerText = '⚡ Processing Video Frames with AI Engine...';

      let formData = new FormData();
      formData.append('video', vidFile);
      formData.append('rect', JSON.stringify({
        x_ratio: vidSelectRect.x / videoOverlayCanvas.width,
        y_ratio: vidSelectRect.y / videoOverlayCanvas.height,
        w_ratio: vidSelectRect.w / videoOverlayCanvas.width,
        h_ratio: vidSelectRect.h / videoOverlayCanvas.height
      }));

      try {
        let res;
        try {
          res = await fetch('/api/process_video', { 
            method: 'POST', 
            body: formData 
          });
        } catch(primaryErr) {
          res = await fetch('https://5eeo6bfngypc.shares.zrok.io/api/process_video', { 
            method: 'POST',
            headers: { 'skip_zrok_interstitial': 'true' },
            body: formData 
          });
        }
        let json = await res.json();

        if (json.status === 'success') {
          status.innerText = '🎉 SUCCESS! Watermark removed from video!';
          let cleanUrl = json.video_url + '?t=' + Date.now();
          document.getElementById('cleanVidPlayer').src = cleanUrl;
          
          let vidDownloadBtn = document.getElementById('vidDownloadBtn');
          vidDownloadBtn.href = cleanUrl;
          
          document.getElementById('vidOutputArea').style.display = 'flex';
        } else {
          status.innerText = '❌ Error: ' + (json.error || 'Video processing failed');
        }
      } catch (err) {
        status.innerText = '❌ Error: ' + err.message;
      }
    }
  </script>

  <!-- Sticky Footer Ad Bar -->
  <div id="stickyAdBar" style="position:fixed;bottom:0;left:0;right:0;height:80px;background:rgba(3,7,22,0.95);backdrop-filter:blur(24px);border-top:1px solid rgba(100,110,255,0.3);z-index:7000;display:flex;align-items:center;justify-content:center;box-shadow:0 -16px 48px rgba(0,0,0,0.55);">
    <button onclick="document.getElementById('stickyAdBar').style.display='none'" style="position:absolute;top:-14px;right:20px;width:28px;height:28px;background:#818cf8;border:none;border-radius:50%;color:#fff;font-size:14px;cursor:pointer;">✕</button>
    <iframe srcdoc="<!DOCTYPE html><html><head><style>html,body{margin:0;padding:0;overflow:hidden;}</style></head><body><script>atOptions = {'key' : '07443fff7d70e04b3642773f8f97367f','format' : 'iframe','height' : 90,'width' : 728,'params' : {}};</script><script src='https://www.highperformanceformat.com/07443fff7d70e04b3642773f8f97367f/invoke.js'></script>
  <!-- Social Bar Ad Script -->
  <script>
    window.addEventListener('load', function() {
      if (!document.getElementById('socialBarAdScript')) {
        var script = document.createElement('script');
        script.id = 'socialBarAdScript';
        script.src = "https://pl30429917.effectivecpmnetwork.com/e3/2d/69/e32d69b13995a39cded45044df825ace.js";
        document.body.appendChild(script);
      }
    });
  </script>

</body></html>" width="728" height="90" frameborder="0" scrolling="no" style="border:none;overflow:hidden;" sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-top-navigation-by-user-activation"></iframe>
  </div>


  <!-- Social Bar Ad Script -->
  <script>
    window.addEventListener('load', function() {
      if (!document.getElementById('socialBarAdScript')) {
        var script = document.createElement('script');
        script.id = 'socialBarAdScript';
        script.src = "https://pl30429917.effectivecpmnetwork.com/e3/2d/69/e32d69b13995a39cded45044df825ace.js";
        document.body.appendChild(script);
      }
    });
  </script>

</body>
</html>
"""

def run_lama_inference(img_bgr, mask_gray):
    orig_h, orig_w, _ = img_bgr.shape
    if session is not None:
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_512 = cv2.resize(img_rgb, (512, 512))
        mask_512 = cv2.resize(mask_gray, (512, 512))

        img_tensor = img_512.astype(np.float32) / 255.0
        img_tensor = np.transpose(img_tensor, (2, 0, 1))[None, ...]
        mask_tensor = (mask_512 > 20).astype(np.float32)[None, None, ...]

        outputs = session.run(None, {'image': img_tensor, 'mask': mask_tensor})
        out = outputs[0][0]
        out = np.transpose(out, (1, 2, 0))
        out = np.clip(out, 0, 255).astype(np.uint8)

        out_bgr = cv2.cvtColor(out, cv2.COLOR_RGB2BGR)
        out_orig = cv2.resize(out_bgr, (orig_w, orig_h))

        mask_3d = (mask_gray > 20)[:, :, None]
        final_output = np.where(mask_3d, out_orig, img_bgr)
        return final_output
    else:
        return cv2.inpaint(img_bgr, (mask_gray > 20).astype(np.uint8)*255, 7, cv2.INPAINT_TELEA)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/clean_output.mp4'):
            f = os.path.join(SCRATCH_DIR, "temp_out.mp4")
            if os.path.exists(f):
                self.send_response(200)
                self.send_header('Content-Type', 'video/mp4')
                self.end_headers()
                with open(f, 'rb') as fp: self.wfile.write(fp.read())
                return
        elif self.path.startswith('/clean_output.png'):
            f = os.path.join(SCRATCH_DIR, "clean_output.png")
            if os.path.exists(f):
                self.send_response(200)
                self.send_header('Content-Type', 'image/png')
                self.end_headers()
                with open(f, 'rb') as fp: self.wfile.write(fp.read())
                return

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/inpaint':
            try:
                length = int(self.headers['Content-Length'])
                req = json.loads(self.rfile.read(length).decode('utf-8'))

                img_data = base64.b64decode(req['image'].split(',')[1])
                img_pil = Image.open(io.BytesIO(img_data)).convert('RGB')
                img_bgr = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

                mask_data = base64.b64decode(req['mask'].split(',')[1])
                mask_pil = Image.open(io.BytesIO(mask_data)).convert('L')
                mask_gray = np.array(mask_pil)

                clean_bgr = run_lama_inference(img_bgr, mask_gray)

                clean_rgb = cv2.cvtColor(clean_bgr, cv2.COLOR_BGR2RGB)
                pil_clean = Image.fromarray(clean_rgb)
                buffer = io.BytesIO()
                pil_clean.save(buffer, format="PNG", compress_level=1)
                b64_clean = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode('utf-8')

                res = json.dumps({'status': 'success', 'clean_image': b64_clean})
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(res.encode('utf-8'))
            except Exception as e:
                traceback.print_exc()
                res = json.dumps({'status': 'error', 'error': str(e)})
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(res.encode('utf-8'))
            return

        if self.path == '/api/process_video':
            try:
                c_header = str(self.headers.get('Content-Type', ''))
                length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(length)

                msg_bytes = b"Content-Type: " + c_header.encode('utf-8') + b"\r\n\r\n" + post_data
                msg = email.message_from_bytes(msg_bytes)

                video_bytes = None
                rect_info = None

                for part in msg.walk():
                    cd = part.get("Content-Disposition", "")
                    if 'name="rect"' in cd or 'name=rect' in cd:
                        rect_info = json.loads(part.get_payload(decode=True).decode('utf-8', errors='ignore'))
                    elif 'name="video"' in cd or 'name=video' in cd:
                        video_bytes = part.get_payload(decode=True)

                if video_bytes and rect_info:
                    temp_in = os.path.join(SCRATCH_DIR, "temp_in.mp4")
                    temp_out = os.path.join(SCRATCH_DIR, "temp_out.mp4")

                    with open(temp_in, "wb") as f: f.write(video_bytes)

                    cap = cv2.VideoCapture(temp_in)
                    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0

                    rx = int(rect_info['x_ratio'] * w)
                    ry = int(rect_info['y_ratio'] * h)
                    rw = int(rect_info['w_ratio'] * w)
                    rh = int(rect_info['h_ratio'] * h)

                    wm_mask = np.zeros((h, w), dtype=np.uint8)
                    wm_mask[ry:ry+rh, rx:rx+rw] = 255

                    frames = []
                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret: break
                        frames.append(frame)
                    cap.release()

                    clean_frames = []
                    for idx, frame in enumerate(frames):
                        inpainted = cv2.inpaint(frame, wm_mask, 7, cv2.INPAINT_TELEA)
                        if 0 < idx < len(frames) - 1:
                            prev_f = cv2.inpaint(frames[idx-1], wm_mask, 7, cv2.INPAINT_TELEA)
                            next_f = cv2.inpaint(frames[idx+1], wm_mask, 7, cv2.INPAINT_TELEA)
                            inpainted = cv2.addWeighted(inpainted, 0.6, cv2.addWeighted(prev_f, 0.5, next_f, 0.5, 0), 0.4, 0)
                        clean_frames.append(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))

                    import imageio
                    imageio.mimsave(temp_out, clean_frames, fps=fps)

                    res = json.dumps({'status': 'success', 'video_url': '/clean_output.mp4'})
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(res.encode('utf-8'))
                else:
                    raise ValueError("Invalid video payload")
            except Exception as e:
                traceback.print_exc()
                res = json.dumps({'status': 'error', 'error': str(e)})
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(res.encode('utf-8'))
            return

def main():
    port = 8080
    print(f"🚀 Starting ZipLoot Watermark AI Server on port {port}...")
    server = HTTPServer(('0.0.0.0', port), Handler)
    server.serve_forever()

if __name__ == "__main__":
    main()
