# Reel 56 — «Презентація з Клодом за 5 хвилин»

Drive folder «Presentation with Claude» (`18Lffz8he73KV5u0GHXzh4NvNvnbbgRkZ`), four phone
clips from 2026-11-17, portrait HEVC ~30 fps. Her brief: *"simple editing today, minimal
animations, just cutting+subtitles"*. The story: open a new chat → a base prompt so he starts
working → meanwhile record a voice note explaining what I want → give it to him → go away for
5 min → a ready, editable presentation → voila.

The first build to go in `RUTA/` (Ruta's pipeline moved there today, beside `Nika/`).

| clip | what | voice |
|---|---|---|
| `20261117_132849` | her to camera: the intro and the outro | yes |
| `20261117_132924` | Claude → New → the base prompt pasted and sent (no voice 4.3–18.4) → her dictating into earphones | partly |
| `20261117_134447` | the base deck, «Ось він мені вже приготував основу…», «Я відправляю йому свої голосові. І все.» | yes |
| `20261117_135042` | the finished deck, a slide edited in place | **none** (whisper hallucinated English over room noise) |

## The cut (`work/r56/mkplate.py`, 1431 frames, DUR 47.7)

| plate | piece | what |
|---|---|---|
| 0.0–11.1 | A | «Сьогодні ввечері в мене вебінар… ведення Threads з AI, але в моїй презентації ще не валявся кінь… з моїм Клодом. Погнали!» |
| 11.1–13.8 | B1 B2 | «Відкриваємо Клод. Натискаємо на New.» (the pause between trimmed) |
| 13.8–21.6 | C | the prompt on screen, sent at the end · **VO 1 + 2** |
| 21.6–29.3 | D1 D2 D3 | her dictating: «Я вважаю, що Клод трошки кращий, мені з ним простіше працювати.» · «Далі, у нас є рівні контексту…три основні рівні контексту.» (her self-correction and 18 s in between cut) |
| 29.3–36.6 | E1–E4 | «Ось він мені вже приготував основу для моєї презентації. Я відправляю йому свої голосові. І все.» («власне» and the pauses cut) |
| 36.6–45.1 | F1 F2 | the finished deck: title slide, «02», then «Що обрати?» edited with the text toolbar · **VO 3** |
| 45.1–47.7 | G | «Якщо було корисно, то обов'язково підпишись.» |

No graphics, no sound cues, no push on the plate. Captions: the word rail (STYLE §00, her
review of reel 41), spelled from her speech (`work/r56/captions.py`): whisper's «введення 3D за
яй» is «ведення Threads з AI» (re-decoded with a vocabulary prompt, `work/r56/redo2.py`),
«особні» → «основні», «колодом» → «Клодом».

## Voiceover (her offer: "if you need me to record on top ill record just give me a script")

1. «Даю йому базовий промт — і він уже починає працювати.» (C)
2. «А поки він працює, я записую голосове: пояснюю, що хочу бачити в презентації.» (C)
3. «Йду на п'ять хвилин. Повертаюсь — презентація готова, і її можна редагувати. Вуаля!» (F)

Until she records them, v1 runs them as caption text at a reading pace over the silent
stretches. When her recording lands:

```bash
python3 work/r56/vo.py <her recording>     # finds the lines, last take wins -> work/r56/vo.json
python3 work/r56/mkplate.py                # C / F grow if her lines are longer; VO levelled to her intro
python3 work/r56/captions.py               # her lines on her timing, later words shifted
cd reel-56 && python3 build.py && sh ../hf check && cd .. && python3 tools/hfrender.py reel-56
```
