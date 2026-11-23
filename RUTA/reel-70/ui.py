# -*- coding: utf-8 -*-
"""Reel 70 — the two rebuilt UIs (Claude «Customize → Connectors», a Notion CRM
database) as clean HTML, plus their CSS. Imported by build.py."""

CLAUDE = u"""
        <div id="stage1" class="stage">
          <div id="win1" class="win">
            <div class="cl-side">
              <div class="cl-brand"><span class="cl-star">✳</span>Claude</div>
              <div class="cl-nav">Новий чат</div>
              <div class="cl-nav">Чати</div>
              <div class="cl-nav">Проєкти</div>
              <div id="cl-cust" class="cl-nav">Customize</div>
            </div>
            <div class="cl-main">
              <div class="cl-h">Customize</div>
              <div class="cl-tabs"><span>Skills</span><span id="cl-conn">Connectors</span></div>
              <div id="cl-search" class="cl-search"><span class="cl-mag"></span><span id="cl-q"></span><span id="cl-caret" class="caret"></span></div>
              <div id="cl-row" class="cl-row">
                <div class="cl-logo">%(notion)s</div>
                <div class="cl-txt"><b>Notion</b><span>Сторінки, бази даних, нотатки</span></div>
                <div id="cl-btn" class="cl-btn"><span class="a">Connect</span><span class="b">✓ Connected</span></div>
              </div>
              <div class="cl-row ghost"><div class="cl-logo g"></div><div class="cl-txt"><b>Google Drive</b><span>Файли та документи</span></div><div class="cl-btn off"><span class="a">Connect</span></div></div>
              <div class="cl-row ghost"><div class="cl-logo g"></div><div class="cl-txt"><b>Gmail</b><span>Пошта</span></div><div class="cl-btn off"><span class="a">Connect</span></div></div>
            </div>
          </div>
        </div>"""

# Notion database: example rows, labelled as such — no money, no real people
ROWS = [(u"Ліда (приклад)", u"Instagram", u"Новий лід", "s1"),
        (u"Олег (приклад)", u"Telegram", u"Дзвінок", "s2"),
        (u"Марта (приклад)", u"Сайт", u"Клієнт", "s3"),
        (u"Ірина (приклад)", u"Instagram", u"Новий лід", "s1")]

NOTION = u"""
        <div id="stage2" class="stage">
          <div id="win2" class="win nt">
            <div class="nt-top"><span class="nt-ic">%(notion)s</span>CRM</div>
            <div class="nt-title">CRM</div>
            <div class="nt-views"><span class="on">▦ Усі ліди</span><span>Дошка</span></div>
            <div class="nt-table">
              <div class="nt-r nt-hd"><span class="c1">Aa Ім'я</span><span class="c2">Звідки</span><span class="c3">Статус</span><span class="c4">Наступний крок</span></div>
%(rows)s
            </div>
          </div>
        </div>"""


def notion_rows():
    out = []
    steps = [u"Відповісти в DM", u"Дзвінок у четвер", u"Повторна покупка", u"Написати"]
    for i, (n, src, st, cls) in enumerate(ROWS):
        out.append(u'              <div id="nr%d" class="nt-r%s"><span class="c1">%s</span><span class="c2">%s</span>'
                   u'<span class="c3"><em class="%s">%s</em></span><span class="c4">%s</span></div>'
                   % (i, " hid" if i == 3 else "", n, src, cls, st, steps[i]))
    return "\n".join(out)


CSS = u"""
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    .stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2200px; }
    .win { position: absolute; left: 0; top: 0; background: #fff; border-radius: 16px;
           font-family: "Google Sans", sans-serif; color: #1f1f1f; overflow: hidden;
           box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 30px 80px rgba(36,25,25,.22);
           transform-origin: 0 0; will-change: transform; }
    /* Claude, Customize -> Connectors (800 x 520) */
    #win1 { width: 800px; height: 520px; background: #FAF9F5; display: flex; }
    .cl-side { width: 190px; background: #F3F1EA; padding: 20px 14px; border-right: 1px solid #E6E2D8; }
    .cl-brand { font-size: 19px; font-weight: 700; display: flex; align-items: center; gap: 8px; margin-bottom: 22px; }
    .cl-star { color: #C15F3C; font-size: 20px; }
    .cl-nav { font-size: 14px; color: #3d3929; padding: 9px 10px; border-radius: 8px; margin-bottom: 2px; }
    .cl-main { flex: 1; padding: 26px 30px; }
    .cl-h { font-size: 24px; font-weight: 700; margin-bottom: 14px; }
    .cl-tabs { display: flex; gap: 22px; font-size: 14px; color: #73716a; border-bottom: 1px solid #E6E2D8; margin-bottom: 18px; }
    .cl-tabs span { padding: 0 2px 10px; border-bottom: 2px solid transparent; }
    .cl-search { height: 38px; border: 1px solid #DAD6CB; border-radius: 10px; background: #fff; display: flex;
                 align-items: center; gap: 10px; padding: 0 12px; font-size: 15px; margin-bottom: 14px; }
    .cl-mag { width: 13px; height: 13px; border: 2px solid #8a877d; border-radius: 50%; flex: none; }
    .caret { display: inline-block; width: 2px; height: 18px; background: #1f1f1f; margin-left: -8px; }
    .cl-row { height: 64px; border: 1px solid #E6E2D8; border-radius: 12px; background: #fff; display: flex;
              align-items: center; gap: 14px; padding: 0 14px; margin-bottom: 10px; }
    .cl-row.ghost { opacity: .45; }
    .cl-logo { width: 38px; height: 38px; border-radius: 9px; border: 1px solid #E6E2D8; display: flex;
               align-items: center; justify-content: center; color: #1f1f1f; flex: none; }
    .cl-logo.g { background: #EFEDE6; }
    .cl-txt { flex: 1; } .cl-txt b { display: block; font-size: 15px; } .cl-txt span { font-size: 12px; color: #73716a; }
    .cl-btn { position: relative; width: 118px; height: 32px; border-radius: 8px; background: #1f1f1f; color: #fff;
              font-size: 13px; font-weight: 500; overflow: hidden; flex: none; }
    .cl-btn.off { background: #EFEDE6; color: #73716a; }
    .cl-btn span { position: absolute; left: 0; right: 0; top: 0; line-height: 32px; text-align: center; }
    .cl-btn .b { opacity: 0; color: #1f1f1f; }
    /* Notion database (860 x 470) */
    #win2 { width: 860px; height: 470px; padding: 0 0 20px; }
    .nt-top { height: 40px; display: flex; align-items: center; gap: 8px; padding: 0 16px; font-size: 13px; color: #37352f;
              border-bottom: 1px solid #EDECE9; }
    .nt-ic { display: inline-flex; color: #37352f; }
    .nt-title { font-size: 36px; font-weight: 700; color: #37352f; padding: 26px 40px 10px; }
    .nt-views { display: flex; gap: 18px; padding: 0 40px; font-size: 13px; color: #9b9a97; border-bottom: 1px solid #EDECE9; }
    .nt-views span { padding-bottom: 8px; } .nt-views .on { color: #37352f; border-bottom: 2px solid #37352f; }
    .nt-table { padding: 0 40px; }
    .nt-r { display: flex; height: 50px; align-items: center; border-bottom: 1px solid #EDECE9; font-size: 15px; color: #37352f; }
    .nt-hd { height: 38px; font-size: 13px; color: #9b9a97; }
    .nt-r span { padding: 0 10px; white-space: nowrap; overflow: hidden; }
    .nt-r .c1 { width: 220px; font-weight: 500; } .nt-r .c2 { width: 140px; } .nt-r .c3 { width: 160px; } .nt-r .c4 { flex: 1; color: #6b6964; }
    .nt-hd .c1 { font-weight: 400; }
    .nt-r em { font-style: normal; font-size: 13px; border-radius: 5px; padding: 3px 9px; }
    em.s1 { background: #F4DFDF; color: #7A1424; } em.s2 { background: #F5EBDD; color: #6b4a1c; } em.s3 { background: #E4EEE7; color: #2d5a3c; }

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
    .ask .who .st { color: #C15F3C; font-size: 28px; }
    .ask .in { background: rgba(255,255,255,.95); border-radius: 22px; padding: 18px 22px; font-size: 30px; line-height: 1.35;
               color: #241919; min-height: 128px; position: relative; }
    .ask .send { position: absolute; right: 16px; bottom: 14px; width: 48px; height: 48px; border-radius: 14px;
                 background: #DEBFBF; color: #fff; font-size: 28px; text-align: center; line-height: 48px; }
    .dm { left: 150px; top: 300px; width: 780px; padding: 24px 28px; }
    .dm .hd { display: flex; align-items: center; gap: 14px; font-size: 26px; font-weight: 500; color: #574142; margin-bottom: 16px; }
    .dm .hd b { width: 40px; height: 40px; border-radius: 50%; background: #7A1424; display: inline-block; }
    .bub { display: inline-block; border-radius: 26px; padding: 16px 24px; font-size: 32px; font-weight: 500; line-height: 1.25; }
    .bub.me { background: #7A1424; color: #fff; border-bottom-right-radius: 8px; }
    .rowr { display: flex; justify-content: flex-end; align-items: center; gap: 14px; }
    .sendb { margin-top: 14px; margin-left: auto; width: max-content; background: #241919; color: #fff; border-radius: 22px;
             font-size: 26px; padding: 10px 26px; }
"""
