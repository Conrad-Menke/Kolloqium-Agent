# Kolloqium-Agent

An opencode skill that turns a corpus of PDFs into an **NRW Kolloquium** coach.
Built for the second-state exam (`Vorbereitungsdienst` / `Referendariat`).

The skill runs in three modes:

- **Mode A — Simulation**: a dynamic examiner conversation calibrated to the
  real NRW format. You open with a self-chosen *Kurzvortrag*; the agent picks
  up the "lose Enden" you leave and develops a flowing conversation across the
  Handlungsfelder, weaving empirical grounding with practical experience.
- **Mode B — Karteikarten**: produces study flashcards. Each card has a
  fictional examiner question, 3–5 answer keywords, and the exact source
  passage from your PDFs.
- **Mode C — Aufbau (Build-your-own tutor)**: the agent switches hats from
  examiner → coach/mentor and walks you through how this skill was built and
  how to fork it for your own use case (other exam format, other language,
  research papers instead of PDFs, Anki export, …). Mode C reads this repo's
  actual files rather than reciting from memory.

Every question and every card is **anchored in retrieved passages**. If the
corpus does not support a question, the agent says so instead of inventing one.
This skill enforces grounding by giving the agent access to **only** the
passages a retrieval step returns.

## Layout

```
.
├── AGENTS.md                       # Agent instructions (repo-level)
├── opencode.json                   # opencode config + permission rules
├── skills/
│   └── kolloquium/
│       ├── SKILL.md                # The examiner skill (persona + rules)
│       ├── scripts/
│       │   ├── index_corpus.py     # Parse + chunk + embed PDF/DOCX → Chroma
│       │   ├── retrieve.py         # Query → JSON passages
│       │   └── requirements.txt
│       ├── data/                   # PDFs/DOCX land here (gitignored)
│       └── index/                  # Chroma DB (gitignored)
```

## Quickstart

Von null bis zur ersten Kolloquiumssession in fünf Schritten.

### 1. opencode installieren

Ein Befehl lädt die neueste Version herunter und installiert sie:

```bash
curl -fsSL https://opencode.ai/install | bash
```

Danach `opencode` im Terminal aufrufen können. Auf macOS alternativ
`brew install opencode`, auf Arch `paru -S opencode`. Details siehe
<https://opencode.ai/docs>.

### 2. Repo klonen

```bash
git clone https://github.com/Conrad-Menke/Kolloqium-Agent.git
cd Kolloqium-Agent
```

### 3. Skill in opencode bekannt machen

Entweder per Symlink in das opencode-Konfigurationsverzeichnis (empfohlen,
danach ist der Skill in jedem Projekt verfügbar):

```bash
ln -s "$(pwd)/skills/kolloquium" \
      "$HOME/.config/opencode/skills/kolloquium"
```

…oder opencode einfach aus dem Repo-Root heraus starten — dann wird der
Skill über seinen relativen Pfad gefunden.

### 4. Erste Session starten

```bash
opencode
```

Im Chat den Skill mit einer Trigger-Phrase aktivieren, z. B.:

> "Führe ein Kolloquium mit mir."

### 5. Mode wählen

Der Skill läuft dann eine **Aktivierungsrunde**:

1. Fragt nach dem Ordner oder den PDF-/DOCX-Dateien (Ordner werden rekursiv
   durchsucht).
2. Legt ein Python-Venv an und installiert die Abhängigkeiten (nur beim
   ersten Mal).
3. Indiziert alle gefundenen Dateien in den lokalen Chroma-Store und
   meldet die Anzahl.
4. Fragt **welcher Modus** (A — Simulation, B — Karteikarten, C — Aufbau)
   plus modusspezifisches Setup.
5. Startet den gewählten Modus.

### Optional: Abhängigkeiten vorab installieren

Wer nicht warten will, bis die Aktivierungsrunde das Venv anlegt, kann es
auch von Hand machen (die Aktivierungsrunde überspringt diesen Schritt
dann):

```bash
cd skills/kolloquium/scripts
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running a Kolloquium

Nach der Aktivierungsrunde (siehe Quickstart Schritt 5) läuft der gewählte
Modus. Was in der Session passiert, steckt in `skills/kolloquium/SKILL.md`:
Mode A führt ein fließendes Gespräch, Mode B erzeugt Karteikarten im
gewünschten Format, Mode C erklärt und adaptiert den Agenten.

Fortsetzen: mit "weiter" / "continue" ohne Neu-Indizierung in dieselbe
Session zurückkehren. Abbrechen: "stop" / "exit exam" / "ich will aufhören".

## How grounding works

Each turn, before asking anything, the agent runs:

```bash
python retrieve.py "<concept>" --k 5
```

The returned JSON (`page`, `source`, `text`, `score`) is the closed universe
for that question. If no passage scores above the grounding threshold, the
agent refuses to fabricate a question and says so. Full rules in
`skills/kolloquium/SKILL.md`.

## Status

Skeleton scaffolded — index and retrieval scripts are functional Python. The
examiner persona lives entirely in the SKILL.md prompt. No server, no daemon,
no external API key required (embeddings run locally via
`sentence-transformers`; the LLM is whatever opencode is already using).
