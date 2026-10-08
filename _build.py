import os

with open(r'C:\Users\raymond\gym-tracker\_font_clean.txt', 'r', encoding='utf-8') as f:
    font_b64 = f.read().strip()

html = r"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>健身打卡遊戲</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
@font-face {
  font-family: 'PressStart';
  src: url('data:font/truetype;base64,FONT_B64_PLACEHOLDER') format('truetype');
}

*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans TC',sans-serif;background:#0a0a1a;color:#e0e0e0;min-height:100vh;display:flex;flex-direction:column;}

/* Header */
#app-header{background:#16213e;padding:12px 16px;display:flex;align-items:center;justify-content:space-between;border-bottom:2px solid #0f3460;}
#app-title{font-family:'PressStart',monospace;font-size:11px;color:#f39c12;letter-spacing:1px;}
#xp-area{display:flex;flex-direction:column;align-items:flex-end;gap:4px;}
#level-badge{font-family:'PressStart',monospace;font-size:10px;color:#f1c40f;}
#xp-bar-wrap{width:120px;height:8px;background:#2c3e50;border-radius:4px;overflow:hidden;}
#xp-bar{height:100%;background:linear-gradient(90deg,#f39c12,#e74c3c);border-radius:4px;transition:width 0.5s;}
#xp-text{font-family:'PressStart',monospace;font-size:7px;color:#bdc3c7;}

/* Streak */
#streak-bar{background:#0f3460;padding:6px 16px;text-align:center;font-size:13px;color:#f39c12;}

/* Main */
#main{flex:1;overflow-y:auto;padding-bottom:70px;}

/* Bottom Nav */
#bottom-nav{position:fixed;bottom:0;left:0;right:0;background:#16213e;border-top:2px solid #0f3460;display:flex;z-index:100;}
.nav-btn{flex:1;padding:10px 4px 8px;display:flex;flex-direction:column;align-items:center;gap:3px;cursor:pointer;border:none;background:none;color:#7f8c8d;font-size:9px;font-family:'Noto Sans TC',sans-serif;transition:color 0.2s;}
.nav-btn.active{color:#f39c12;}
.nav-btn svg{width:22px;height:22px;}
.nav-btn span{font-size:10px;}

/* Day Tabs */
#day-tabs{display:flex;overflow-x:auto;gap:6px;padding:12px 12px 0;scrollbar-width:none;}
#day-tabs::-webkit-scrollbar{display:none;}
.day-tab{flex-shrink:0;padding:6px 12px;border-radius:20px;border:2px solid transparent;cursor:pointer;font-size:12px;font-weight:500;transition:all 0.2s;background:#1a1a2e;color:#7f8c8d;}
.day-tab.active{color:#fff;border-color:currentColor;}
.day-tab.active.push{color:#e74c3c;border-color:#e74c3c;background:#2d1515;}
.day-tab.active.pull{color:#3498db;border-color:#3498db;background:#152030;}
.day-tab.active.legs{color:#2ecc71;border-color:#2ecc71;background:#152818;}
.day-tab.active.rest{color:#7f8c8d;border-color:#7f8c8d;}

/* Exercise Cards */
.ex-card{background:#1a1a2e;border-radius:12px;margin:12px;padding:14px;border:1px solid #2a2a4e;}
.ex-name{font-size:16px;font-weight:700;margin-bottom:10px;color:#fff;}
.ex-name span{font-size:12px;font-weight:400;color:#7f8c8d;margin-left:6px;}

/* Set rows */
.set-row{display:flex;align-items:center;gap:6px;margin-bottom:8px;padding:8px 10px;border-radius:8px;background:#0f0f2a;transition:all 0.2s;}
.set-row.confirmed{background:#0d1f0d;opacity:0.75;}
.set-row.locked{background:#111128;opacity:0.5;}
.set-num{font-size:12px;color:#7f8c8d;width:18px;flex-shrink:0;text-align:center;}
.set-inp{flex:1;min-width:0;}
.set-inp input{width:100%;background:#1e1e3e;border:1px solid #2a2a5e;border-radius:6px;color:#fff;font-size:16px;padding:6px 4px;font-family:'Noto Sans TC',sans-serif;text-align:center;}
.set-inp input:disabled{background:#181830;color:#555;border-color:#222;}
.set-inp label{font-size:10px;color:#7f8c8d;display:block;text-align:center;margin-bottom:2px;}
.confirm-btn{width:44px;height:44px;border-radius:50%;background:#27ae60;border:none;color:#fff;font-size:20px;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;transition:transform 0.1s;}
.confirm-btn:active{transform:scale(0.9);}
.confirmed-icon{width:44px;height:44px;border-radius:50%;background:#1a3a1a;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;}
.lock-icon{width:44px;height:44px;border-radius:50%;background:#1a1a2e;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;color:#444;}

/* Add set button */
.add-set-btn{width:100%;padding:8px;border:1px dashed #2a2a5e;border-radius:8px;background:none;color:#7f8c8d;font-size:13px;cursor:pointer;margin-top:4px;font-family:'Noto Sans TC',sans-serif;}
.add-set-btn:hover{border-color:#3498db;color:#3498db;}

/* Complete button */
#complete-btn-wrap{padding:0 12px 12px;}
#complete-btn{width:100%;padding:14px;border-radius:12px;background:linear-gradient(135deg,#f39c12,#e74c3c);border:none;color:#fff;font-size:16px;font-weight:700;cursor:pointer;font-family:'Noto Sans TC',sans-serif;transition:opacity 0.2s;}
#complete-btn:hover{opacity:0.9;}
#complete-btn:disabled{opacity:0.4;cursor:not-allowed;}

/* Rest day */
#rest-msg{text-align:center;padding:60px 20px;color:#7f8c8d;}
#rest-msg .rest-icon{font-size:60px;margin-bottom:16px;}
#rest-msg h2{font-size:20px;color:#fff;margin-bottom:8px;}
#rest-msg p{font-size:14px;}

/* Map */
#map-section{padding:12px;}
.map-title{font-family:'PressStart',monospace;font-size:10px;color:#f39c12;margin-bottom:12px;}
.map-week-row{display:flex;gap:4px;margin-bottom:4px;align-items:center;}
.week-label{width:30px;font-size:9px;color:#555;flex-shrink:0;}
.week-dots{display:grid;grid-template-columns:repeat(7,1fr);gap:3px;flex:1;}
.day-dot-sm{aspect-ratio:1;border-radius:3px;}
.push-done{background:#e74c3c;}
.pull-done{background:#3498db;}
.legs-done{background:#2ecc71;}
.rest-day{background:#2a2a4e;}
.map-future{background:#1a1a2e;border:1px solid #2a2a4e;}
.missed{background:#2a1a1a;}

/* Achievements */
#ach-section{padding:12px;}
.ach-card{background:#1a1a2e;border-radius:10px;padding:12px 14px;margin-bottom:8px;display:flex;align-items:center;gap:12px;border:1px solid #2a2a4e;}
.ach-card.unlocked{border-color:#f39c12;background:#1e1a10;}
.ach-icon{font-size:28px;width:44px;text-align:center;}
.ach-info{flex:1;}
.ach-name{font-size:14px;font-weight:700;color:#fff;}
.ach-card:not(.unlocked) .ach-name{color:#555;}
.ach-desc{font-size:12px;color:#7f8c8d;margin-top:2px;}
.ach-card:not(.unlocked) .ach-desc{color:#333;}
.ach-lock{font-size:20px;color:#333;}

/* Settings */
#set-section{padding:12px;}
.set-group{background:#1a1a2e;border-radius:12px;padding:14px;margin-bottom:12px;border:1px solid #2a2a4e;}
.set-group h3{font-size:14px;color:#f39c12;margin-bottom:12px;font-weight:700;}
.set-row-item{display:flex;flex-direction:column;gap:6px;margin-bottom:12px;}
.set-row-item label{font-size:13px;color:#bdc3c7;}
.set-row-item input[type=date]{background:#0f0f2a;border:1px solid #2a2a5e;border-radius:8px;color:#fff;font-size:16px;padding:8px 10px;font-family:'Noto Sans TC',sans-serif;width:100%;}
.danger-btn{width:100%;padding:12px;border-radius:8px;border:1px solid #e74c3c;background:none;color:#e74c3c;font-size:14px;cursor:pointer;font-family:'Noto Sans TC',sans-serif;margin-top:6px;}
.danger-btn:hover{background:#e74c3c;color:#fff;}
.save-btn{width:100%;padding:12px;border-radius:8px;border:none;background:#27ae60;color:#fff;font-size:14px;cursor:pointer;font-family:'Noto Sans TC',sans-serif;margin-top:6px;}

/* Toast */
#toast{position:fixed;top:20px;left:50%;transform:translateX(-50%) translateY(-80px);background:#f39c12;color:#000;padding:10px 20px;border-radius:20px;font-size:13px;font-weight:700;z-index:9999;transition:transform 0.3s;pointer-events:none;}
#toast.show{transform:translateX(-50%) translateY(0);}

/* Level up overlay */
#lvl-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.85);display:none;align-items:center;justify-content:center;z-index:9998;flex-direction:column;gap:16px;}
#lvl-overlay.show{display:flex;}
.lvl-title{font-family:'PressStart',monospace;font-size:16px;color:#f1c40f;text-align:center;line-height:2;}
.lvl-btn{padding:12px 32px;border-radius:20px;border:none;background:#f39c12;color:#000;font-size:16px;font-weight:700;cursor:pointer;font-family:'Noto Sans TC',sans-serif;}

/* No plan notice */
#no-plan-notice{background:#1a1a2e;border:1px solid #f39c12;border-radius:10px;margin:12px;padding:12px;font-size:13px;color:#f39c12;text-align:center;}

/* Day header */
.day-header{padding:10px 12px 4px;font-size:13px;color:#7f8c8d;}
.day-header strong{color:#fff;font-size:15px;}
</style>
</head>
<body>

<!-- Level Up Overlay -->
<div id="lvl-overlay">
  <div class="lvl-title" id="lvl-title"></div>
  <button class="lvl-btn" onclick="closeLvlOverlay()">繼續 ▶</button>
</div>

<!-- Toast -->
<div id="toast"></div>

<!-- Header -->
<div id="app-header">
  <div id="app-title">GYM QUEST</div>
  <div id="xp-area">
    <div id="level-badge">LV.1</div>
    <div id="xp-bar-wrap"><div id="xp-bar" style="width:0%"></div></div>
    <div id="xp-text">0 / 800 XP</div>
  </div>
</div>

<!-- Streak -->
<div id="streak-bar">🔥 連續 <strong id="streak-val">0</strong> 天</div>

<!-- Main -->
<div id="main">
  <div id="section-workout"></div>
  <div id="section-map" style="display:none"></div>
  <div id="section-achievements" style="display:none"></div>
  <div id="section-settings" style="display:none"></div>
</div>

<!-- Bottom Nav -->
<nav id="bottom-nav">
  <button class="nav-btn active" onclick="showSection('workout')" id="nav-workout">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6.5 6.5h11M6.5 17.5h11M4 12h16M2 8.5l2-2M2 15.5l2 2M20 6.5l2 2M20 17.5l2-2"/></svg>
    <span>訓練</span>
  </button>
  <button class="nav-btn" onclick="showSection('map')" id="nav-map">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/></svg>
    <span>地圖</span>
  </button>
  <button class="nav-btn" onclick="showSection('achievements')" id="nav-achievements">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
    <span>成就</span>
  </button>
  <button class="nav-btn" onclick="showSection('settings')" id="nav-settings">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
    <span>設定</span>
  </button>
</nav>

<script>
// ─── Constants ───────────────────────────────────────────────
const GYM_SESSIONS  = 'gym_sessions';
const GYM_GAME      = 'gym_game';
const GYM_TEMPLATES = 'gym_tpl';
const GYM_PLAN      = 'gym_plan';

const XP_PER_SET   = 3;
const XP_COMPLETE  = 50;
const XP_DELOAD    = 80;
const XP_PER_LEVEL = 800;
const MAX_LEVEL    = 52;

const DEFAULT_TEMPLATES = {
  1:[
    {name:'臥推',sets:[{w:50,r:6,rpe:7},{w:50,r:6,rpe:7},{w:50,r:6,rpe:7},{w:50,r:6,rpe:7},{w:50,r:6,rpe:7}]},
    {name:'上斜啞鈴臥推',sets:[{w:24,r:10,rpe:8},{w:24,r:10,rpe:8},{w:24,r:10,rpe:8}]},
    {name:'啞鈴側平舉',sets:[{w:6,r:12,rpe:8},{w:6,r:12,rpe:8},{w:6,r:12,rpe:8}]},
  ],
  2:[
    {name:'滑輪下拉',sets:[{w:36,r:10,rpe:8},{w:36,r:10,rpe:8},{w:36,r:10,rpe:8},{w:36,r:10,rpe:8}]},
    {name:'啞鈴划船',sets:[{w:40,r:8,rpe:8},{w:40,r:8,rpe:8},{w:40,r:8,rpe:8}]},
    {name:'W槓彎舉',sets:[{w:15,r:10,rpe:8},{w:15,r:10,rpe:8},{w:15,r:10,rpe:8}]},
  ],
  3:[
    {name:'腿推舉',sets:[{w:25,r:10,rpe:8},{w:25,r:10,rpe:8},{w:25,r:10,rpe:8},{w:25,r:10,rpe:8}]},
    {name:'V Squat',sets:[{w:20,r:12,rpe:8},{w:20,r:12,rpe:8},{w:20,r:12,rpe:8}]},
    {name:'腿伸屈',sets:[{w:18,r:12,rpe:8},{w:18,r:12,rpe:8},{w:18,r:12,rpe:8}]},
  ],
  4:[
    {name:'臥推',sets:[{w:50,r:6,rpe:7},{w:50,r:6,rpe:7},{w:50,r:6,rpe:7},{w:50,r:6,rpe:7},{w:50,r:6,rpe:7}]},
    {name:'三頭下壓',sets:[{w:15,r:12,rpe:8},{w:15,r:12,rpe:8},{w:15,r:12,rpe:8}]},
    {name:'啞鈴側平舉',sets:[{w:6,r:12,rpe:8},{w:6,r:12,rpe:8},{w:6,r:12,rpe:8}]},
  ],
  5:[
    {name:'滑輪下拉',sets:[{w:36,r:10,rpe:8},{w:36,r:10,rpe:8},{w:36,r:10,rpe:8},{w:36,r:10,rpe:8}]},
    {name:'器械划船',sets:[{w:25,r:12,rpe:8},{w:25,r:12,rpe:8},{w:25,r:12,rpe:8}]},
    {name:'臉拉',sets:[{w:10,r:15,rpe:8},{w:10,r:15,rpe:8},{w:10,r:15,rpe:8}]},
  ],
  6:[
    {name:'腿推舉',sets:[{w:25,r:10,rpe:8},{w:25,r:10,rpe:8},{w:25,r:10,rpe:8},{w:25,r:10,rpe:8}]},
    {name:'腿彎舉',sets:[{w:15,r:12,rpe:8},{w:15,r:12,rpe:8},{w:15,r:12,rpe:8}]},
    {name:'腿外展',sets:[{w:32,r:12,rpe:8},{w:32,r:12,rpe:8},{w:32,r:12,rpe:8}]},
  ],
};

const WEEK_CYCLE = [
  {type:'push',label:'DAY1 推A',short:'推A',day:1,color:'push'},
  {type:'pull',label:'DAY2 拉A',short:'拉A',day:2,color:'pull'},
  {type:'legs',label:'DAY3 腿A',short:'腿A',day:3,color:'legs'},
  {type:'rest',label:'休息日',  short:'休', day:0,color:'rest'},
  {type:'push',label:'DAY4 推B',short:'推B',day:4,color:'push'},
  {type:'pull',label:'DAY5 拉B',short:'拉B',day:5,color:'pull'},
  {type:'legs',label:'DAY6 腿B',short:'腿B',day:6,color:'legs'},
];

const ACHIEVEMENTS_DEF = [
  {id:'first_workout',name:'第一次訓練',desc:'完成你的第一次訓練',icon:'🏋️'},
  {id:'streak_3',     name:'連續3天',  desc:'連續訓練3天',      icon:'🔥'},
  {id:'streak_7',     name:'連續7天',  desc:'連續訓練7天',      icon:'⚡'},
  {id:'streak_14',    name:'連續14天', desc:'連續訓練14天',     icon:'💪'},
  {id:'streak_30',    name:'連續30天', desc:'連續訓練30天',     icon:'👑'},
  {id:'level_5',      name:'達到5級',  desc:'升到第5級',        icon:'⭐'},
  {id:'level_10',     name:'達到10級', desc:'升到第10級',       icon:'🌟'},
  {id:'level_20',     name:'達到20級', desc:'升到第20級',       icon:'💫'},
  {id:'level_52',     name:'達到52級', desc:'達到最高等級！',    icon:'🏆'},
];

// ─── State ───────────────────────────────────────────────────
let gameState      = {xp:0,level:1,streak:0,lastDate:'',achievements:[]};
let sessions       = [];
let templates      = {};
let currentSection = 'workout';
let currentDay     = 1;
let currentSession = {};  // day -> {ei -> [{w,r,rpe},...]}
let confirmedSets  = {};  // day -> {ei -> lastConfirmedIndex}

// ─── Init ────────────────────────────────────────────────────
function init(){
  const gs = localStorage.getItem(GYM_GAME);
  if(gs) try{ gameState = JSON.parse(gs); }catch(e){}
  const ss = localStorage.getItem(GYM_SESSIONS);
  if(ss) try{ sessions = JSON.parse(ss); }catch(e){}
  templates = getTemplates();

  const sched = getTodaySchedule();
  if(sched.hasplan && sched.schedule && sched.schedule.type !== 'rest'){
    currentDay = sched.schedule.day;
  }

  renderHeader();
  renderAll();
}

function getTemplates(){
  const saved = localStorage.getItem(GYM_TEMPLATES);
  const custom = saved ? JSON.parse(saved) : {};
  const merged = {};
  for(let d=1;d<=6;d++){
    merged[d] = custom[d]
      ? JSON.parse(JSON.stringify(custom[d]))
      : JSON.parse(JSON.stringify(DEFAULT_TEMPLATES[d]));
  }
  return merged;
}

// ─── Schedule ────────────────────────────────────────────────
function getTodaySchedule(){
  const planStr = localStorage.getItem(GYM_PLAN);
  if(!planStr) return {hasplan:false};
  let startDate;
  try{ startDate = new Date(JSON.parse(planStr).startDate); }catch(e){ return {hasplan:false}; }
  const today = new Date();
  today.setHours(0,0,0,0);
  startDate.setHours(0,0,0,0);
  const diffDays = Math.floor((today - startDate)/86400000);
  const cyclePos = ((diffDays % 7)+7)%7;
  return {hasplan:true, schedule:WEEK_CYCLE[cyclePos], cyclePos};
}

// ─── Header ──────────────────────────────────────────────────
function renderHeader(){
  document.getElementById('level-badge').textContent = 'LV.'+gameState.level;
  const xpInLevel = gameState.xp - (gameState.level-1)*XP_PER_LEVEL;
  const pct = Math.min(100,(xpInLevel/XP_PER_LEVEL)*100);
  document.getElementById('xp-bar').style.width = pct+'%';
  document.getElementById('xp-text').textContent = xpInLevel+' / '+XP_PER_LEVEL+' XP';
  document.getElementById('streak-val').textContent = gameState.streak;
}

// ─── Section routing ─────────────────────────────────────────
function showSection(sec){
  currentSection = sec;
  ['workout','map','achievements','settings'].forEach(s=>{
    document.getElementById('section-'+s).style.display = s===sec ? '' : 'none';
    document.getElementById('nav-'+s).classList.toggle('active', s===sec);
  });
  renderAll();
}

function renderAll(){
  if(currentSection==='workout')      renderWorkout();
  else if(currentSection==='map')     renderMap();
  else if(currentSection==='achievements') renderAchievements();
  else if(currentSection==='settings')    renderSettings();
}

// ─── Workout ─────────────────────────────────────────────────
function renderWorkout(){
  const wrap = document.getElementById('section-workout');
  const sched = getTodaySchedule();

  if(sched.hasplan && sched.schedule && sched.schedule.type==='rest'){
    wrap.innerHTML = '<div id="rest-msg"><div class="rest-icon">🌙</div><h2>今天是休息日</h2><p>好好休息，明天繼續加油！</p></div>';
    return;
  }

  let html = '';
  html += renderDayTabsHTML(sched);

  if(!sched.hasplan){
    html += '<div id="no-plan-notice">尚未設定訓練計畫，請到「設定」設定開始日期，或直接選擇日次訓練</div>';
  }

  const dayInfo = WEEK_CYCLE.find(w=>w.day===currentDay) || WEEK_CYCLE[0];
  html += '<div class="day-header"><strong>'+escHtml(dayInfo.label)+'</strong></div>';
  html += '<div id="ex-list">'+renderExercisesHTML()+'</div>';
  html += '<div id="complete-btn-wrap"><button id="complete-btn" onclick="completeWorkout()">完成訓練 🏁</button></div>';

  wrap.innerHTML = html;
}

function renderDayTabsHTML(sched){
  if(sched.hasplan && sched.schedule && sched.schedule.type!=='rest'){
    const sc = sched.schedule;
    return '<div id="day-tabs"><div class="day-tab '+sc.color+' active">'+escHtml(sc.label)+'</div></div>';
  }
  let html = '<div id="day-tabs">';
  WEEK_CYCLE.filter(w=>w.type!=='rest').forEach(w=>{
    const active = w.day===currentDay;
    html += '<div class="day-tab '+w.color+(active?' active':'')+'" onclick="selectDay('+w.day+')">'+escHtml(w.label)+'</div>';
  });
  html += '</div>';
  return html;
}

function renderExercisesHTML(){
  const exList = templates[currentDay] || [];
  if(!currentSession[currentDay]) currentSession[currentDay] = {};
  if(!confirmedSets[currentDay])  confirmedSets[currentDay]  = {};

  let html = '';
  exList.forEach((ex, ei)=>{
    if(!currentSession[currentDay][ei]){
      currentSession[currentDay][ei] = ex.sets.map(s=>({w:s.w, r:s.r, rpe:s.rpe}));
    }
    const sess = currentSession[currentDay][ei];
    const lastConfirmed = (confirmedSets[currentDay][ei] !== undefined) ? confirmedSets[currentDay][ei] : -1;

    html += '<div class="ex-card">';
    html += '<div class="ex-name">'+escHtml(ex.name)+'<span>'+sess.length+' 組</span></div>';

    sess.forEach((set, si)=>{
      const isConfirmed = si <= lastConfirmed;
      const isActive    = si === lastConfirmed + 1;

      if(isConfirmed){
        html += '<div class="set-row confirmed">';
        html += '<div class="set-num">'+(si+1)+'</div>';
        html += setInputsHTML(ei,si,set,true);
        html += '<div class="confirmed-icon">✅</div>';
        html += '</div>';
      } else if(isActive){
        html += '<div class="set-row" id="setrow-'+ei+'-'+si+'">';
        html += '<div class="set-num">'+(si+1)+'</div>';
        html += setInputsHTML(ei,si,set,false);
        html += '<button class="confirm-btn" onclick="confirmSet('+ei+','+si+')">✓</button>';
        html += '</div>';
      } else {
        html += '<div class="set-row locked">';
        html += '<div class="set-num">'+(si+1)+'</div>';
        html += '<div class="set-inp"><label>重量kg</label><input disabled value="'+escHtml(String(set.w))+'"></div>';
        html += '<div class="set-inp"><label>次數</label><input disabled value="'+escHtml(String(set.r))+'"></div>';
        html += '<div class="set-inp"><label>RPE</label><input disabled value="'+escHtml(String(set.rpe))+'"></div>';
        html += '<div class="lock-icon">🔒</div>';
        html += '</div>';
      }
    });

    html += '<button class="add-set-btn" onclick="addSet('+ei+')">+ 新增一組</button>';
    html += '</div>';
  });
  return html;
}

function setInputsHTML(ei,si,set,disabled){
  const d = disabled ? ' disabled' : '';
  const vw  = (set.w  !== '' && set.w  !== undefined) ? escHtml(String(set.w))  : '';
  const vr  = (set.r  !== '' && set.r  !== undefined) ? escHtml(String(set.r))  : '';
  const vrpe= (set.rpe!== '' && set.rpe!== undefined) ? escHtml(String(set.rpe)): '';
  return '<div class="set-inp"><label>重量kg</label><input type="number" inputmode="decimal"'+d+' value="'+vw+'" onchange="updateSet('+ei+','+si+',\'w\',this.value)"></div>'+
         '<div class="set-inp"><label>次數</label><input type="number" inputmode="numeric"'+d+' value="'+vr+'" onchange="updateSet('+ei+','+si+',\'r\',this.value)"></div>'+
         '<div class="set-inp"><label>RPE</label><input type="number" inputmode="decimal"'+d+' value="'+vrpe+'" onchange="updateSet('+ei+','+si+',\'rpe\',this.value)"></div>';
}

function selectDay(d, silent){
  if(currentDay === d) return;
  if(!silent){
    const hasProgress = confirmedSets[currentDay] &&
      Object.values(confirmedSets[currentDay]).some(v=>v>=0);
    if(hasProgress){
      if(!confirm('切換訓練日（已確認的組數資料仍會保留）。確定切換？')) return;
    }
  }
  currentDay = d;
  renderWorkout();
}

function updateSet(ei,si,field,val){
  if(!currentSession[currentDay] || !currentSession[currentDay][ei]) return;
  currentSession[currentDay][ei][si][field] = (val==='' ? '' : parseFloat(val));
}

function confirmSet(ei, si){
  if(!currentSession[currentDay] || !currentSession[currentDay][ei]) return;
  const set = currentSession[currentDay][ei][si];
  if(set.w==='' || set.r==='' || set.rpe==='' ||
     set.w===undefined || set.r===undefined || set.rpe===undefined){
    showToast('請填寫重量、次數和RPE');
    return;
  }
  if(!confirmedSets[currentDay]) confirmedSets[currentDay]={};
  confirmedSets[currentDay][ei] = si;
  awardXP(XP_PER_SET);
  renderWorkout();
}

function addSet(ei){
  if(!currentSession[currentDay]) currentSession[currentDay]={};
  if(!currentSession[currentDay][ei]) return;
  currentSession[currentDay][ei].push({w:'',r:'',rpe:''});
  renderWorkout();
}

function completeWorkout(){
  const exList = templates[currentDay] || [];
  let allDone = true;
  exList.forEach((_,ei)=>{
    const sess = currentSession[currentDay] && currentSession[currentDay][ei];
    if(!sess || sess.length===0){ allDone=false; return; }
    const lastConf = (confirmedSets[currentDay] && confirmedSets[currentDay][ei]!==undefined)
      ? confirmedSets[currentDay][ei] : -1;
    if(lastConf < sess.length-1) allDone=false;
  });
  if(!allDone){
    showToast('請確認所有組數後再完成訓練！');
    return;
  }

  const today = todayStr();
  const dayInfo = WEEK_CYCLE.find(w=>w.day===currentDay) || WEEK_CYCLE[0];
  const sessionData = {
    date:today, day:currentDay, type:dayInfo.type,
    exercises: exList.map((ex,ei)=>({
      name:ex.name,
      sets:(currentSession[currentDay][ei]||[]).filter((_,si)=>{
        const lc=(confirmedSets[currentDay]&&confirmedSets[currentDay][ei]!==undefined)
          ?confirmedSets[currentDay][ei]:-1;
        return si<=lc;
      })
    }))
  };
  sessions.push(sessionData);
  localStorage.setItem(GYM_SESSIONS, JSON.stringify(sessions));

  updateStreak(today);
  awardXP(XP_COMPLETE);
  checkAchievements();

  // Reset only this day's session
  currentSession[currentDay]={};
  confirmedSets[currentDay]={};

  // Auto-advance plan
  const sched = getTodaySchedule();
  if(sched.hasplan){
    const nextPos = (sched.cyclePos+1)%7;
    const next = WEEK_CYCLE[nextPos];
    if(next.type!=='rest') currentDay=next.day;
  }

  showToast('訓練完成！+'+XP_COMPLETE+' XP 🎉');
  renderHeader();
  renderAll();
}

function updateStreak(today){
  const last = gameState.lastDate;
  if(!last){
    gameState.streak=1;
  } else {
    const diff = dateDiffDays(last, today);
    if(diff===1)       gameState.streak++;
    else if(diff===0)  { /* same day */ }
    else               gameState.streak=1;
  }
  gameState.lastDate=today;
  localStorage.setItem(GYM_GAME, JSON.stringify(gameState));
}

// ─── XP & Level ──────────────────────────────────────────────
function awardXP(n){
  const prevLevel = gameState.level;
  gameState.xp += n;
  const newLevel = Math.min(MAX_LEVEL, Math.floor(gameState.xp/XP_PER_LEVEL)+1);
  if(newLevel > prevLevel){
    gameState.level = newLevel;
    showLevelUp(newLevel);
  }
  localStorage.setItem(GYM_GAME, JSON.stringify(gameState));
  renderHeader();
}

function showLevelUp(lv){
  document.getElementById('lvl-title').innerHTML = 'LEVEL UP!<br>LV.'+lv;
  document.getElementById('lvl-overlay').classList.add('show');
}

function closeLvlOverlay(){
  document.getElementById('lvl-overlay').classList.remove('show');
}

// ─── Achievements ────────────────────────────────────────────
function checkAchievements(){
  const unlocked = new Set(gameState.achievements);
  const newOnes = [];

  if(sessions.length>=1 && !unlocked.has('first_workout')) newOnes.push('first_workout');
  [3,7,14,30].forEach(n=>{
    if(gameState.streak>=n && !unlocked.has('streak_'+n)) newOnes.push('streak_'+n);
  });
  [5,10,20,52].forEach(n=>{
    if(gameState.level>=n && !unlocked.has('level_'+n)) newOnes.push('level_'+n);
  });

  newOnes.forEach(id=>{
    gameState.achievements.push(id);
    const def = ACHIEVEMENTS_DEF.find(a=>a.id===id);
    if(def) showToast('成就解鎖：'+def.icon+' '+def.name);
  });
  if(newOnes.length) localStorage.setItem(GYM_GAME, JSON.stringify(gameState));
}

function renderAchievements(){
  const wrap = document.getElementById('section-achievements');
  const unlocked = new Set(gameState.achievements);
  let html = '<div id="ach-section">';
  ACHIEVEMENTS_DEF.forEach(a=>{
    const done = unlocked.has(a.id);
    html += '<div class="ach-card'+(done?' unlocked':'')+'">';
    html += '<div class="ach-icon">'+a.icon+'</div>';
    html += '<div class="ach-info"><div class="ach-name">'+escHtml(a.name)+'</div><div class="ach-desc">'+escHtml(a.desc)+'</div></div>';
    if(!done) html += '<div class="ach-lock">🔒</div>';
    html += '</div>';
  });
  html += '</div>';
  wrap.innerHTML = html;
}

// ─── Map ─────────────────────────────────────────────────────
function renderMap(){
  const wrap = document.getElementById('section-map');
  const planStr = localStorage.getItem(GYM_PLAN);
  if(!planStr){
    wrap.innerHTML = '<div style="padding:20px;color:#7f8c8d;text-align:center">請先在「設定」設定訓練計畫開始日期</div>';
    return;
  }
  let startDate;
  try{ startDate = new Date(JSON.parse(planStr).startDate); }catch(e){
    wrap.innerHTML = '<div style="padding:20px;color:#e74c3c">計畫資料錯誤</div>'; return;
  }
  startDate.setHours(0,0,0,0);

  const doneMap = {};
  sessions.forEach(s=>{ doneMap[s.date]=s.type; });

  const today = new Date(); today.setHours(0,0,0,0);

  let html = '<div id="map-section"><div class="map-title">52 WEEK MAP</div>';
  for(let week=0;week<52;week++){
    html += '<div class="map-week-row"><div class="week-label">W'+(week+1)+'</div><div class="week-dots">';
    for(let d=0;d<7;d++){
      const dayOffset = week*7+d;
      const dt = new Date(startDate); dt.setDate(dt.getDate()+dayOffset);
      const ds = dt.toISOString().slice(0,10);
      const cyclePos = ((dayOffset%7)+7)%7;
      const sched = WEEK_CYCLE[cyclePos];
      let cls = 'day-dot-sm ';
      if(dt > today)           cls += 'map-future';
      else if(sched.type==='rest') cls += 'rest-day';
      else if(doneMap[ds])     cls += doneMap[ds]+'-done';
      else                     cls += 'missed';
      html += '<div class="'+cls+'" title="'+ds+'"></div>';
    }
    html += '</div></div>';
  }
  html += '</div>';
  wrap.innerHTML = html;
}

// ─── Settings ────────────────────────────────────────────────
function renderSettings(){
  const wrap = document.getElementById('section-settings');
  const planStr = localStorage.getItem(GYM_PLAN);
  let startVal = '';
  if(planStr) try{ startVal = JSON.parse(planStr).startDate||''; }catch(e){}

  wrap.innerHTML =
    '<div id="set-section">'+
    '<div class="set-group">'+
    '<h3>訓練計畫</h3>'+
    '<div class="set-row-item">'+
    '<label>計畫開始日期</label>'+
    '<input type="date" id="plan-date" value="'+escHtml(startVal)+'">'+
    '</div>'+
    '<button class="save-btn" onclick="savePlan()">儲存計畫</button>'+
    '</div>'+
    '<div class="set-group">'+
    '<h3>資料管理</h3>'+
    '<button class="danger-btn" onclick="resetTemplates()">重設課表</button>'+
    '<button class="danger-btn" onclick="resetAll()">重設所有資料</button>'+
    '</div>'+
    '</div>';
}

function savePlan(){
  const val = document.getElementById('plan-date').value;
  if(!val){ showToast('請選擇日期'); return; }
  localStorage.setItem(GYM_PLAN, JSON.stringify({startDate:val}));
  const sched = getTodaySchedule();
  if(sched.hasplan && sched.schedule && sched.schedule.type!=='rest'){
    currentDay = sched.schedule.day;
  }
  showToast('計畫已儲存！');
  renderAll();
}

function resetTemplates(){
  if(!confirm('確定要重設課表？自訂課表將遺失。')) return;
  localStorage.removeItem(GYM_TEMPLATES);
  templates = getTemplates();
  currentSession = {};
  confirmedSets  = {};
  showToast('課表已重設');
}

function resetAll(){
  if(!confirm('確定要清除所有資料？此操作無法復原！')) return;
  [GYM_SESSIONS,GYM_GAME,GYM_TEMPLATES,GYM_PLAN].forEach(k=>localStorage.removeItem(k));
  gameState     = {xp:0,level:1,streak:0,lastDate:'',achievements:[]};
  sessions      = [];
  templates     = getTemplates();
  currentSession= {};
  confirmedSets = {};
  renderHeader();
  showToast('所有資料已清除');
  renderAll();
}

// ─── Helpers ─────────────────────────────────────────────────
function todayStr(){
  return new Date().toISOString().slice(0,10);
}

function dateDiffDays(a,b){
  return Math.round((new Date(b)-new Date(a))/86400000);
}

function escHtml(s){
  return String(s)
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;');
}

let toastTimer=null;
function showToast(msg){
  const t=document.getElementById('toast');
  t.textContent=msg;
  t.classList.add('show');
  if(toastTimer) clearTimeout(toastTimer);
  toastTimer=setTimeout(()=>t.classList.remove('show'),2500);
}

// ─── Boot ────────────────────────────────────────────────────
init();
</script>
</body>
</html>"""

# Inject font
html = html.replace('FONT_B64_PLACEHOLDER', font_b64)

out_path = r'C:\Users\raymond\gym-tracker\game.html'
with open(out_path, 'w', encoding='utf-8', newline='') as f:
    f.write(html)
print('Written:', len(html), 'chars to', out_path)
