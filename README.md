# reel-editor-machine

Reel pipelines, one folder per person. The path says whose reel it is.

| folder | whose | contract |
|---|---|---|
| [`RUTA/`](RUTA/README.md) | **Ruta's own reels** (`RUTA/reel-NN/`). The look is **locked** (STYLE §00 + her reel-61 review) — see `CLAUDE.md` | `RUTA/STYLE.md` |
| [`Nika/`](Nika/README.md) | Nika's UNLOCK ad reels. A different person and a different style | `Nika/README.md` |

Nothing crosses between them: Ruta's tools live in `RUTA/tools/`, Nika's in
`Nika/tools/`, and neither imports the other's. If a session can't tell whose
reel it is, it asks before touching anything.

`.claude/` stays at the root so the `/reel` skill and the `reel-verify` agent
load from anywhere in the repo; both work inside `RUTA/`.

Moved 2026-11-17: everything of Ruta's used to sit at the root. Footage and
renders are gitignored, so on a machine that still has them under the old
`reel-NN/assets/` paths they stay where they were — move them by hand into
`RUTA/reel-NN/assets/` if an old reel needs re-rendering.
