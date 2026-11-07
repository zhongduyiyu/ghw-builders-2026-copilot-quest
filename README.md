# Builder Quest

A short, family-friendly command-line adventure built with **GitHub Copilot Chat** for MLH Global Hack Week: Builders Week 2026.

## Run

Requires Python 3.6 or newer. No third-party dependencies, accounts, API keys, or network access are needed.

```sh
python game.py
```

Choose numbered options to explore the fair entrance, workshop, creek, and summit. Collect a toolkit, build a safe crossing, and light the beacon. The game has win, loss, and retreat endings. Enter `q` to quit. Invalid choices are rejected without changing state; EOF ends gracefully.

Example winning route: `1`, `1`, `1`, `1`.

## Test

```sh
python -m unittest -v
python -m py_compile game.py test_game.py
```

All **18 unit tests** passed locally on November 7, 2026. CLI smoke tests also exercised a win, invalid input followed by a loss, and empty-input EOF. These are local execution results, not a claim that GitHub Actions ran.

## How Copilot was used

GitHub Copilot Chat generated `game.py` and the initial tests from a prompt specifying a small Python choose-your-own-adventure game, four scenes, multiple endings, inventory, and separated game logic/input-output. Running the initial tests exposed two contradictory expectations. A second Copilot prompt corrected the tests and expanded coverage. Final review then corrected two test routes and strengthened the all-scenes quit test before rerunning the suite.

The work was carried out with an AI assistant: Copilot supplied the game implementation and test drafts, and the assisting workflow downloaded, reviewed, executed, and published the files. No claim of manual attendance or completion of unrelated courses is made.

## Files

- `game.py`: game state and terminal runner.
- `test_game.py`: deterministic tests using Python's standard `unittest` module.
- `test-results.txt`: actual local test output.
- `demo-win.txt`: actual successful terminal playthrough.

Challenge: [Use GitHub Copilot to Build a Simple Application](https://www.mlh.com/events/global-hack-week-builders-week/challenges/01a1ad0d-16d0-b004-0e85-508eb8952e49)
