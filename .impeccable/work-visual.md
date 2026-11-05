# Working activity visual

Operate surface, preserving the warm-paper/olive shell. Reference: user's October 24 screen recording, showing a rotating point cloud changing shape beside a live task trail.

The authored moment is a 3,000-point canvas, changing between stacked sheets (sources), a cube (audit), columns (experiment), and a ring (response preparation). Shape changes are driven by server-recorded phases. The geometry is decorative, never a model-reasoning trace or measured data chart. No fabricated percent complete or ETA.

A short trail shows actual completed/failed/blocked tool steps. A collapsible record remains after completion. Elapsed time uses the response timestamp and is excluded from live accessibility announcements. Fixed labels contain no tool arguments, credentials, source excerpts, or private reasoning.

Budget: one visible 240px canvas, capped device-pixel ratio 2 and roughly 30 frames/second. Canvas survives phase rerenders, stops offscreen/hidden or when leaving chat, and is removed on completion. Pause is retained locally; reduced-motion uses a static pose. Static mode only updates elapsed text once per second. Mobile stacks the 185px visual above status text.

Standalone `/work-preview.html` is explicitly labeled illustrative, makes no API calls, and lets a user inspect each phase and completion. Production activity is independent of this preview. Verification: desktop/mobile preview, pause/resume, completion cleanup, successful/failed live tool events, JavaScript syntax, design detector, 47 Python tests. Reduced-motion behavior checked in code; OS emulation was not used.
