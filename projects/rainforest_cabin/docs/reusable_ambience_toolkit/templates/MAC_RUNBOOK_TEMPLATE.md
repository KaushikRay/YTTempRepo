# Local Mac runbook — fill for the actual tested kit

This is a documentation template. The production launchers/scripts described here
are NOT supplied by this generic instruction pack. Implement and test the real
project-specific commands before telling a user to run them.

- Kit type: exact-download/join, timeline/audio rebuild, or Blender source render
- Tested OS/chip/software versions: TBD
- Actual test coverage: TBD (Linux smoke test is not real Mac execution)
- Free disk / RAM / source download / output sizes: TBD
- Official prerequisites and install steps: TBD
- Extract/move destination: e.g. ~/Movies/<Project>/
- Source/license/redistribution checks: TBD

Expected actual launchers once implemented:

1. 1_Setup.command — dependencies, package hashes, licensed source downloads
2. 2_Preview.command — local test and review
3. 3_Build.command — selected masters with resumable stages
4. 4_Check.command — real QA and reports

Example invocation AFTER the actual launcher exists (replace <Project>):

```bash
bash "$HOME/Movies/<Project>/1_Setup.command"
```

Actual status/log inspection command: TBD

Actual output folders: TBD

Safe stop/restart behavior: TBD

Benchmark-based estimate for each step: TBD

Keep the computer powered appropriately. Explain foreground/persistent job behavior
and what caffeinate does/does not guarantee. Do not disable Gatekeeper or claim
the chat automatically controls the Mac.
