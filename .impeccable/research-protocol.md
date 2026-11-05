# Research protocol surface

## Overview

This surface extends the established [visual contract](../DESIGN.md) in operate mode. It retains the warm paper, olive controls, graphite text, Source Sans shell typography and fine dividing rules. It introduces no new visual identity or global design tokens.

Implementation evidence: `web/index.html`, `web/shell.js` and `web/shell.css`. Reviewed screenshots: [desktop](review/rigor-desktop.png) and [mobile](review/rigor-mobile.png). These screenshots establish the navigation, release gate and capability table appearance; the reader, report and recovery behaviors below are grounded in code.

## Layout

Research protocol is a first-class sidebar destination above Sources, with the shell's existing olive selected state and document icon. The page follows the content-view hierarchy: title and explanatory sentence, release blockers and next action, capability table, saved protocols, then plan and architecture reader. Maintain this order so release limitations precede implementation detail.

The sidebar collapses below the existing mobile breakpoint (700px). Content padding becomes 24px by 18px, while tables retain their columns inside locally scrollable wrappers. Keep long scope text available through scrolling rather than hiding or truncating it. Reader controls wrap and remain within the available width. Saved report content is capped at 850px; source sections wrap within an 80-character reading width.

## Components

### Release gate and capabilities

The release gate uses a plain heading, readable bullet list and next-step paragraph, separated from the capability table by a fine rule. The current heading explicitly says “Release gate: not passed.” Preserve the actual blocker language rather than converting it into a readiness score.

The capability table presents Plan area, Status and Current scope. Small olive status labels share the existing run-status styling; their words distinguish implemented, partial and not implemented. The explanatory scope column carries the limitations that a status alone cannot express.

### Saved protocols and reports

Saved protocols use a three-column table with hypothesis/design, status and registration. Keep protocol identifiers, unsupported-design reasons and registration notes visible. The empty state explains how to register through chat and that unsupported designs remain blocked.

Saved research reports open as a reading view with title, saved date, contract version, recorded status and a Research protocol return button. Structured fields use muted labels above readable values, fine separators, nested definition lists and ordinary lists. Null fields say “Not established”; empty arrays say “None recorded.” Long values wrap. These are audit records, so absence must remain explicit.

### Document section reader

Use separately labeled document and section selectors with an explicit Read section action. Changing either selection replaces the old section with an instruction to load the new selection. Display the original section as wrapped plain text followed by its document fingerprint. Retain the shell's reading font and fine top rule; this is a specification reader, not a code editor.

### Loading, recovery and stale responses

Protocol and report requests show a short contextual loading message. A failed request becomes an alert with a Try again button that repeats the same operation. Reader failures remain in the reading area and instruct the user to select Read section to retry.

Page-generation checks prevent a late protocol or report response from replacing a destination opened subsequently. The section reader also uses a request counter: selector changes and newer reads invalidate earlier responses, including errors. Preserve both protections when extending these views so the visible selection always agrees with displayed evidence.

All controls inherit the existing visible olive focus outline. The collapsed sidebar is inert and hidden from accessibility APIs, and the shell's reduced-motion rule continues to apply.
