"""One-off: replace emojis in game.html with pixel icons from preview/icons.js."""
import io, os

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
p = os.path.join(root, 'game.html')
s = io.open(p, encoding='utf-8').read()
icons_js = io.open(os.path.join(root, 'preview', 'icons.js'), encoding='utf-8').read()


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, (n, old[:80])
    s = s.replace(old, new, 1)


# 1) icon module
module = """// ─── Pixel icons (16x16, replace emojis) ─────────────────────
""" + icons_js + """const EMOJI_PX = {
  '🥉':['medal3'],'🥈':['medal2'],'🥇':['medal1'],'👹':['beast'],'🦁':['beast'],
  '⚡':['bolt'],'💥':['bolt'],'🦵':['leg'],'🦵🦵':['leg','leg'],'🏃':['run'],
  '📅':['calendar'],'📆':['calendar'],'🗓️':['calendar'],'💯':['hundred'],'🤖':['robot'],
  '🔥':['fire'],'🔥🔥':['fire','fire'],'👑':['crown'],'⭐':['star'],'🌟':['star'],'💫':['star'],
  '🔮':['orb'],'🏆':['trophy'],'💪':['muscle'],'💪💪':['muscle','muscle'],'🦾':['muscle'],
  '💀':['skull'],'💎':['gem'],'💎💎':['gem','gem'],'💠':['gem'],'🌈':['rainbow'],
  '🦉':['owl'],'🌅':['sun'],'🔄':['loop'],'🔁':['loop'],'🎯':['target']
};

function pxSVG(grid, scale){
  const n = grid.length;
  let r='';
  grid.forEach((row,y)=>{
    for(let x=0;x<row.length;x++){
      const f = SPRITE_PAL[row[x]];
      if(f) r += '<rect x="'+x+'" y="'+y+'" width="1" height="1" fill="'+f+'"/>';
    }
  });
  return '<svg class="px" width="'+(n*scale)+'" height="'+(n*scale)+'" viewBox="0 0 '+n+' '+n+'" shape-rendering="crispEdges">'+r+'</svg>';
}
function pxIcon(name, scale){ return PX_ICONS[name] ? pxSVG(PX_ICONS[name], scale||1) : ''; }

// Achievement emoji -> pixel tile (two icons side by side for doubled emojis)
function achIconHTML(emoji){
  const names = EMOJI_PX[emoji] || ['star'];
  return '<span class="px-tile">'+names.map(n=>pxIcon(n, names.length>1?1:2)).join('')+'</span>';
}

"""
rep('// ─── Exercise sprites (Game Boy style, 20x20)', module + '// ─── Exercise sprites (Game Boy style, 20x20)')

# 2) static HTML emojis -> placeholders filled on init
rep('<div class="coach-header">📊 教練分析</div>', '<div class="coach-header"><span data-px="chart"></span> 教練分析</div>')
rep('<div class="ach-notif-label">🏆 成就解鎖！</div>', '<div class="ach-notif-label"><span data-px="trophy"></span> 成就解鎖！</div>')
rep('<div id="streak-bar">🔥 連續', '<div id="streak-bar"><span data-px="fire"></span> 連續')
rep("  loadDraft();\n  renderHeader();",
    "  document.querySelectorAll('[data-px]').forEach(el=>{ el.innerHTML = pxIcon(el.dataset.px, 1); });\n  loadDraft();\n  renderHeader();")

# 3) workout buttons
rep("""onclick="completeWorkout()">完成訓練 🏁</button>""", """onclick="completeWorkout()">完成訓練 '+pxIcon('flag',1)+'</button>""")
rep("""title="改名">✏️</button>""", """title="改名">'+pxIcon('pencil',1)+'</button>""")
rep("""title="刪除動作">🗑</button>""", """title="刪除動作">'+pxIcon('trash',1)+'</button>""")
rep("""font-size:16px;cursor:pointer;flex-shrink:0;">✕</button>""",
    """font-size:16px;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;">'+pxIcon('x',1)+'</button>""")
rep("""' XP 🎉');""", """' XP！');""")

# 4) achievements
rep("""      html += '<div class="ach-icon">'+(isSecret?'❓':a.icon)+'</div>';""",
    """      html += '<div class="ach-icon">'+(isSecret?'<span class="px-tile">'+pxIcon('question',2)+'</span>':achIconHTML(a.icon))+'</div>';""")
rep("""if(!done) html += '<div class="ach-lock">🔒</div>';""", """if(!done) html += '<div class="ach-lock">'+pxIcon('lock',2)+'</div>';""")
rep("""document.getElementById('ach-notif-icon').textContent = def.icon;""",
    """document.getElementById('ach-notif-icon').innerHTML = achIconHTML(def.icon);""")
cats = [('bench', '🏋️ 臥推挑戰', 'barbell', '臥推挑戰'), ('pull', '🔙 滑輪下拉', 'barbell', '滑輪下拉'),
        ('legs', '🦵 腿推舉', 'leg', '腿推舉'), ('squat', '🏋️ 深蹲挑戰', 'barbell', '深蹲挑戰'),
        ('dead', '⛏️ 硬拉挑戰', 'barbell', '硬拉挑戰'), ('attend', '📅 出勤紀錄', 'calendar', '出勤紀錄'),
        ('streak', '🔥 連續挑戰', 'fire', '連續挑戰'), ('upper', '💪 上肢戰士', 'muscle', '上肢戰士'),
        ('lower', '🦵 下肢英雄', 'leg', '下肢英雄'), ('level', '⭐ 等級成長', 'star', '等級成長'),
        ('xp', '💎 XP 累積', 'gem', 'XP 累積'), ('secret', '💀 隱藏成就', 'skull', '隱藏成就')]
for key, old_label, icon, label in cats:
    pad = ' ' * (7 - len(key))
    rep("{key:'%s',%slabel:'%s'}" % (key, pad, old_label),
        "{key:'%s',%sicon:'%s', label:'%s'}" % (key, pad, icon, label))
rep("""padding:0 2px;">'+cat.label+' <span""",
    """padding:0 2px;display:flex;align-items:center;gap:6px;">'+pxIcon(cat.icon,1)+cat.label+' <span""")

# 5) progress
rep("""letter-spacing:1px;">📈 重量進步紀錄</div>';""",
    """letter-spacing:1px;display:flex;align-items:center;gap:6px;">'+pxIcon('chart',1)+'重量進步紀錄</div>';""")
rep("""const diffStr = diff > 0 ? '+'+diff+'kg ⬆️' : diff < 0 ? diff+'kg ⬇️' : '持平 ➡️';""",
    """const diffStr = diff > 0 ? '+'+diff+'kg '+pxIcon('up',1) : diff < 0 ? diff+'kg '+pxIcon('down',1) : '持平 '+pxIcon('right',1);""")

# 6) diet headers (template literal)
rep("""margin-bottom:12px;">📊 每日目標</div>""", """margin-bottom:12px;display:flex;align-items:center;gap:6px;">${pxIcon('chart',1)}每日目標</div>""")
rep("""margin-bottom:12px;">🥩 食材營養素</div>""", """margin-bottom:12px;display:flex;align-items:center;gap:6px;">${pxIcon('meat',1)}食材營養素</div>""")
rep("""margin-bottom:12px;">🍽 範例菜單</div>""", """margin-bottom:12px;display:flex;align-items:center;gap:6px;">${pxIcon('bowl',1)}範例菜單</div>""")

# 7) CSS
rep('.ex-tile .ex-icon{margin-right:0;}', """.ex-tile .ex-icon{margin-right:0;}
.px{vertical-align:middle;flex-shrink:0;}
.px-tile{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;background:#9bbc0f;border:3px solid #0f380f;box-shadow:2px 2px 0 #306230;}
.ach-card:not(.unlocked) .px-tile{opacity:.55;}
.ach-lock{opacity:.7;}""")

io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
