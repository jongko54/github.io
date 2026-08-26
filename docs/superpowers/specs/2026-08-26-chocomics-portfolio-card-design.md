# ChoComics Portfolio Card Design

## Goal

Add ChoComics to the portfolio's `WEB/APP` category as a prominent, live-linked project card using two current screenshots from the deployed service.

## Placement and content

- Add a wide ChoComics card at the top of `work-category-web-app`.
- Increase the `WEB/APP` tab count from 5 to 6.
- Use the title `ChoComics · AI 웹툰 플랫폼` and link it to `https://chocomics.keiailab.com/`.
- Describe the visible product scope: featured webtoons, real-time ranking, monthly releases, and weekday serialization.
- Identify the implementation as a React-based web platform without adding unverified operational claims.

## Screenshot composition

The approved direction is the two-image layout (option B):

1. A desktop capture of the home hero and real-time ranking.
2. A desktop capture of monthly releases and weekday serialization.

Both captures come from the current live homepage, use the same viewport and theme, and are saved under `assets/work-repos/` with descriptive filenames. Each figure receives concise alt text and a caption. The image group links to the live ChoComics site.

## Responsive behavior

Reuse the existing `repo-shots` and `repo-shot` portfolio patterns. The two captures appear side-by-side at desktop widths and follow the page's existing responsive rule to stack vertically on smaller screens. No new global visual system or unrelated card refactor is introduced.

## Failure handling

- Images are checked locally before commit so corrupt or blank captures are not published.
- The live URL is smoke-tested before and after deployment.
- Existing `loading="lazy"`, alt text, and caption conventions are retained so a delayed image does not remove the project description or link context.
- If the live page cannot be captured consistently, the existing verified first capture is retained and the second capture is retried without changing the card design.

## Verification

- A structural test asserts that the `WEB/APP` count is 6, the ChoComics title and URL are present, both image paths exist in the HTML, and both image files exist on disk.
- A local browser check verifies the Web/App tab, two-image desktop layout, mobile stacking, captions, and live-link target.
- After pushing `main`, verify the remote commit and reload `https://jongko54.github.io/github.io/` until the deployed ChoComics card and both images are observable.

## Out of scope

- Changes to the ChoComics application itself.
- New portfolio navigation or styling systems.
- Login-only ChoComics screens, admin screens, or user data.
- Reordering or rewriting unrelated portfolio projects.
