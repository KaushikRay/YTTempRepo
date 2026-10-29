# Reusable thumbnail prompts

Fill placeholders and supply the approved source frame to the actual image tool.
For strict literal fidelity, use an actual frame with a permitted exact editing
workflow; generative edits may alter fine detail. Tool-specific rules take priority.

## Shared instruction

```text
Create ONE finished professional YouTube thumbnail for [VERSION ID], landscape
16:9, targeting 1280×720. Use the supplied approved scene as the foundation.
Preserve its architecture, plants, geography, lighting relationship and actual
subjects. No mockup, border or contact sheet. Do not invent people, animals,
lightning, extraordinary water or other absent content. Restrained photograph-like
finish; no cartoon/plastic surfaces. Keep all text inside safe margins, avoid the
bottom-right duration overlay, and spell the supplied wording exactly. No logo
unless supplied, no ad-free claim, no medical guarantee. Output only the cover.
```

## A — wide topic cover

```text
Keep the wide approved composition and readable focal subject. Put the short
headline [EXACT TOPIC WORDING] in the available negative space, using high-contrast
clean typography. Add [EXACT DURATION LABEL] and, only when applicable,
[EXACT DARK-SCREEN TIMING]. Do not obscure the subject. Make the wording readable
around 320 px image width.
```

## B — focal-subject cover

```text
Use a tasteful closer composition centered on [EXISTING FOCAL SUBJECT]. Retain
enough authentic surrounding context. No large headline. Use one legible restrained
badge with [EXACT DURATION LABEL] and [DARK-SCREEN TIMING IF APPLICABLE]. Preserve
the actual subject and scene; do not invent a new building or perspective.
```

## C — alternative message/composition

```text
Use a distinct, balanced framing of the same scene, emphasizing [EXISTING DETAIL].
Add the short headline [EXACT ALTERNATIVE WORDING] with restrained type and
[ACCURATE DURATION / DARK-SCREEN LABEL]. Maintain the approved atmosphere and
clear focal point. Differentiate this option without introducing absent content.
```

After generation: read every word, compare with the source, verify duration/dark
behavior, export/check dimensions and size, inspect at 320 px width, and include
real files plus comparison/ZIP/manifest. Do not treat prompts as finished images.
