# UDC tutorial — UDC tutorial: автоматизація звітності з контенту через Claude

Not a reel: her 14:50 horizontal take (4K, `20261027_153024.mp4`, Drive folder
1U2wL_hXneL0INfvePcEezkY8l5hfaFoO) for UDC. Her calls, 2026-10-27:
16:9 horizontal · pauses and retakes cut · simple subtitles, kept above
YouTube's progress bar · the hands-on part animated from her screenshots as a
smooth demo (big cursor, hand-drawn rings, personal details blurred) with her in
a rounded box, framed wide.

## Pipeline (all in the cloud container, no paid render)

1. `asr_fw.py` — faster-whisper medium, word timings -> `segs.jsonl`
2. `cut-fix.json` — the seven retakes, by hand from the transcript
3. `tools/cutlong.py work/udc-tutorial --render` -> `plate.mp4` (1920x1080, 100/108 % framing steps)
4. `tools/subs.py work/udc-tutorial` (+ `fix.json`, `merge.json` for whisper's spelling) -> `subs.ass`
5. `finish.sh` — `tools/demo.py` over `demo.json` (plate 516.9–674.3 s), then
   plate | demo | plate + subtitles -> `UDC-tutorial.mp4`

## Demo beats (plate seconds)

| at | screen | ring / click |
|---|---|---|
| 516.9 | Claude home | screen rises, she shrinks into the box |
| 535.3 | home | Customize («кнопку customize») |
| 538.2 | Customize → Connectors | Connectors tab 541.7, search 543.7 |
| 545.9 | search «metricool» | Metricool row 550.6, + 554.6 |
| 563.9 | Connectors | search 568.8, Notion 571.0, its button 572.8 |
| 583.6 | home | Scheduled («routines», clock icon) 592.6 |
| 597.7 | Scheduled tasks | New task 601.9 |
| 604.0 | New scheduled task | «Set up with Claude instead» 608.6, big field 635.8, Daily 641.6 |
| 648.3 | … Notifications tab | tab 650.6, Email ticked 655.1, Create 671.5 |
| 674.3 | — | she grows back to full frame |
