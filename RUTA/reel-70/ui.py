# -*- coding: utf-8 -*-
"""Reel 70 — the two rebuilt UIs (Claude «Customize → Connectors», a Notion CRM
database) as clean HTML, plus their CSS. Imported by build.py."""

CLAUDE = u"""
        <div id="stage1" class="stage">
          <div id="win1" class="win">
            <div class="cl-side">
              <div class="cl-brand">%(claude)s<span>Claude</span></div>
              <div class="cl-nav">New chat</div>
              <div class="cl-nav">Chats</div>
              <div class="cl-nav">Projects</div>
              <div id="cl-cust" class="cl-nav">Customize</div>
            </div>
            <div class="cl-main">
              <div class="cl-h">Customize</div>
              <div class="cl-tabs"><span>Skills</span><span id="cl-conn">Connectors</span></div>
              <div id="cl-search" class="cl-search"><span class="cl-mag"></span><span id="cl-q"></span><span id="cl-caret" class="caret"></span></div>
              <div id="cl-row" class="cl-row">
                <div class="cl-logo">%(notion)s</div>
                <div class="cl-txt"><b>Notion</b></div>
                <div id="cl-btn" class="cl-btn"><span class="a">Connect</span><span class="b">✓ Connected</span></div>
              </div>
              <div class="cl-row ghost"><div class="cl-logo g"></div><div class="cl-txt"><b>Google Drive</b></div><div class="cl-btn off"><span class="a">Connect</span></div></div>
              <div class="cl-row ghost"><div class="cl-logo g"></div><div class="cl-txt"><b>Gmail</b></div><div class="cl-btn off"><span class="a">Connect</span></div></div>
              <div class="cl-row ghost"><div class="cl-logo g"></div><div class="cl-txt"><b>Calendar</b></div><div class="cl-btn off"><span class="a">Connect</span></div></div>
            </div>
          </div>
        </div>"""

# Notion database: only what she names (leads and past clients), generic
# names, no money, no stats.
ROWS = [(u"Клієнтка 1", u"Instagram", u"Клієнт", "s3"),
        (u"Клієнтка 2", u"Сайт", u"Клієнт", "s3"),
        (u"Клієнтка 3", u"Telegram", u"Лід", "s1"),
        (u"Клієнтка 4", u"Instagram", u"Новий лід", "s1")]

NOTION = u"""
        <div id="stage2" class="stage">
          <div id="win2" class="win nt">
            <div class="nt-top"><span class="nt-ic">%(notion)s</span>CRM<span class="nt-sh">Share</span></div>
            <div class="nt-title">CRM</div>
            <div class="nt-views"><span class="on">▦ Table</span><span>Board</span></div>
            <div class="nt-table">
              <div class="nt-r nt-hd"><span class="c1">Aa Ім'я</span><span class="c2">Звідки</span><span class="c3">Статус</span></div>
%(rows)s
              <div class="nt-r nt-new"><span class="c1">+ New</span></div>
            </div>
          </div>
        </div>"""


def notion_rows():
    out = []
    for i, (n, src, st, cls) in enumerate(ROWS):
        out.append(u'              <div id="nr%d" class="nt-r%s"><span class="c1">%s</span><span class="c2">%s</span>'
                   u'<span class="c3"><em class="%s">%s</em></span></div>'
                   % (i, " hid" if i == 3 else "", n, src, cls, st))
    return "\n".join(out)


CSS = u"""
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    .stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2400px; }
    .win { position: absolute; left: 0; top: 0; background: #fff; border-radius: 36px;
           font-family: "Google Sans", sans-serif; color: #1f1f1f; overflow: hidden;
           box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 30px 80px rgba(36,25,25,.22);
           will-change: transform; }
    /* Claude, Customize -> Connectors (960 x 920) */
    #win1 { width: 960px; height: 920px; background: #FAF9F5; display: flex; }
    .cl-side { width: 290px; background: #F3F1EA; padding: 40px 22px; border-right: 2px solid #E6E2D8; box-sizing: border-box; }
    .cl-brand { font-size: 42px; font-weight: 700; display: flex; align-items: center; gap: 14px; margin: 0 0 40px 14px; }
    .cl-brand .mark { color: #7A1424; fill: currentColor; }
    .cl-nav { font-size: 32px; color: #3d3929; padding: 18px 18px; border-radius: 16px; margin-bottom: 6px; }
    .cl-main { flex: 1; padding: 44px 40px; box-sizing: border-box; }
    .cl-h { font-size: 52px; font-weight: 700; margin-bottom: 22px; }
    .cl-tabs { display: flex; gap: 36px; font-size: 32px; color: #73716a; border-bottom: 2px solid #E6E2D8; margin-bottom: 28px; }
    .cl-tabs span { padding: 0 2px 16px; border-bottom: 4px solid transparent; }
    .cl-search { height: 84px; border: 2px solid #DAD6CB; border-radius: 20px; background: #fff; display: flex;
                 align-items: center; gap: 18px; padding: 0 24px; font-size: 34px; margin-bottom: 24px; box-sizing: border-box; }
    .cl-mag { width: 24px; height: 24px; border: 4px solid #8a877d; border-radius: 50%; flex: none; }
    .caret { display: inline-block; width: 3px; height: 38px; background: #1f1f1f; margin-left: -14px; }
    .cl-row { height: 120px; border: 2px solid #E6E2D8; border-radius: 22px; background: #fff; display: flex;
              align-items: center; gap: 20px; padding: 0 22px; margin-bottom: 16px; box-sizing: border-box; }
    .cl-row.ghost { opacity: .45; }
    .cl-logo { width: 72px; height: 72px; border-radius: 16px; border: 2px solid #E6E2D8; display: flex;
               align-items: center; justify-content: center; color: #1f1f1f; flex: none; box-sizing: border-box; }
    .cl-logo .mark { fill: currentColor; }
    .cl-logo.g { background: #EFEDE6; }
    .cl-txt { flex: 1; } .cl-txt b { display: block; font-size: 36px; font-weight: 500; }
    .cl-btn { position: relative; width: 200px; height: 68px; border-radius: 16px; background: #1f1f1f; color: #fff;
              font-size: 30px; font-weight: 500; overflow: hidden; flex: none; }
    .cl-btn.off { background: #EFEDE6; color: #73716a; }
    .cl-btn span { position: absolute; left: 0; right: 0; top: 0; line-height: 68px; text-align: center; white-space: nowrap; }
    .cl-btn .b { opacity: 0; color: #1f1f1f; }
    /* Notion database (960 x 860) */
    #win2 { width: 960px; height: 860px; }
    .nt-top { height: 80px; display: flex; align-items: center; gap: 14px; padding: 0 30px; font-size: 28px; color: #37352f;
              border-bottom: 2px solid #EDECE9; }
    .nt-ic { display: inline-flex; color: #37352f; } .nt-ic .mark { fill: currentColor; }
    .nt-sh { margin-left: auto; color: #787774; }
    .nt-title { font-size: 76px; font-weight: 700; color: #37352f; padding: 44px 50px 18px; }
    .nt-views { display: flex; gap: 34px; padding: 0 50px; font-size: 28px; color: #9b9a97; border-bottom: 2px solid #EDECE9; }
    .nt-views span { padding-bottom: 14px; } .nt-views .on { color: #37352f; border-bottom: 4px solid #37352f; }
    .nt-table { padding: 0 50px; }
    .nt-r { display: flex; height: 100px; align-items: center; border-bottom: 2px solid #EDECE9; font-size: 34px; color: #37352f; }
    .nt-hd { height: 74px; font-size: 28px; color: #9b9a97; }
    .nt-new { height: 84px; font-size: 28px; color: #9b9a97; border-bottom: none; }
    .nt-r span { padding: 0 14px; white-space: nowrap; overflow: hidden; }
    .nt-r .c1 { width: 330px; font-weight: 500; } .nt-r .c2 { width: 230px; } .nt-r .c3 { flex: 1; }
    .nt-hd .c1, .nt-new .c1 { font-weight: 400; }
    .nt-r em { font-style: normal; font-size: 30px; border-radius: 10px; padding: 6px 18px; }
    em.s1 { background: #F4DFDF; color: #7A1424; } em.s3 { background: #7A1424; color: #fff; }

    /* above me */
    .tab { left: 140px; top: 310px; width: 800px; padding: 18px 22px 22px; }
    .tab .bar { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; font-size: 22px; color: #574142; }
    .tab .dots i { display: inline-block; width: 13px; height: 13px; border-radius: 50%; background: #DEBFBF; margin-right: 7px; }
    .tab .t { background: rgba(255,255,255,.9); border-radius: 12px 12px 0 0; padding: 8px 18px; }
    .tab .addr { height: 76px; border-radius: 38px; background: rgba(255,255,255,.95); display: flex; align-items: center;
                 gap: 18px; padding: 0 28px; font-size: 38px; color: #241919; }
    .tab .addr .mark { color: #7A1424; }
    .tab .go { margin-left: auto; background: #241919; color: #fff; border-radius: 26px; font-size: 26px; padding: 10px 24px; }
    .ask { left: 120px; top: 300px; width: 840px; padding: 24px 28px; }
    .ask .who { display: flex; align-items: center; gap: 10px; font-size: 24px; color: #574142; margin-bottom: 12px; }
    .ask .who .st { color: #7A1424; font-size: 28px; }
    .ask .in { background: rgba(255,255,255,.95); border-radius: 22px; padding: 16px 86px 16px 22px; font-size: 30px; line-height: 1.3;
               color: #241919; min-height: 128px; position: relative; }
    .ask .send { position: absolute; right: 16px; bottom: 14px; width: 48px; height: 48px; border-radius: 14px;
                 background: #A2676F; color: #fff; font-size: 28px; text-align: center; line-height: 48px; }
    .dm { left: 150px; top: 300px; width: 780px; padding: 24px 28px; }
    .dm .hd { display: flex; align-items: center; gap: 14px; font-size: 26px; font-weight: 500; color: #574142; margin-bottom: 16px; }
    .dm .hd b { width: 40px; height: 40px; border-radius: 50%; background: #7A1424; display: inline-block; }
    .bub { display: inline-block; border-radius: 26px; padding: 16px 24px; font-size: 32px; font-weight: 500; line-height: 1.25; }
    .bub.me { background: #7A1424; color: #fff; border-bottom-right-radius: 8px; }
    .rowr { display: flex; justify-content: flex-end; align-items: center; gap: 14px; }
    .sendb { margin-top: 14px; margin-left: auto; width: max-content; background: #241919; color: #fff; border-radius: 22px;
             font-size: 26px; padding: 10px 26px; }
"""
