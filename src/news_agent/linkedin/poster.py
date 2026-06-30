"""Generate a Sugansa LinkedIn poster end-to-end with OpenAI's gpt-image-2.

The image model renders the whole poster from the LinkedIn post content. We
then guarantee brand accuracy by overlaying the REAL Sugansa logo over the
top-left (the model is told not to draw one). Hashtags are kept off the poster
- they belong in the post text. Requires OPENAI_API_KEY in the environment.
"""

from __future__ import annotations

import base64
import io
from pathlib import Path

from openai import OpenAI
from PIL import Image

# Brand assets (see memory: sugansa-brand). The horizontal lockup is recoloured
# to white for placement on the dark poster, per the on-dark brand rule.
BRAND_DIR = Path.home() / "sugansa-linkedin" / "brand"
LOGO_LOCKUP = BRAND_DIR / "sugansa-horizontal-mono-indigo.png"

DEFAULT_MODEL = "gpt-image-2"

STYLE = (
    "STYLE: premium enterprise-consulting infographic, design-studio quality, "
    "executive-ready (CIO / CDO / data & AI leaders). One strong visual "
    "metaphor that explains the business point (e.g. an iceberg: a small "
    "visible AI model above the waterline, a large hidden foundation of "
    "semantic context, trusted data, governance and engineering below). Deep "
    "navy background with blue and gold accents; clean hierarchy; generous "
    "spacing; crisp, correctly-spelled, highly readable text. Not generic AI "
    "art, no cartoon robots, no clutter."
)


def build_poster_prompt(
    post: str,
    brand: str = "Sugansa Solutions",
    tagline: str = "Data Simplified and AI Amplified",
) -> str:
    """Assemble the gpt-image-2 prompt from the LinkedIn post content."""

    return (
        f"Create a premium, square (1:1) LinkedIn infographic poster for the "
        f"Data & AI thought-leadership post below, by {brand} - an enterprise "
        f"Data & AI consulting company (tagline: '{tagline}').\n\n"
        f"{STYLE}\n\n"
        f"STRICT RULES:\n"
        f"- Reserve a clean empty horizontal band across the VERY TOP of the "
        f"poster (about 12% of the height), solid dark background, with "
        f"absolutely NO text, graphics, headline or logo in it. The headline "
        f"and all content must start BELOW this band. A real logo is placed in "
        f"this top band afterwards.\n"
        f"- Do NOT draw any company logo, wordmark, icon, or brand mark "
        f"anywhere.\n"
        f"- Do NOT include any hashtags (#...) anywhere on the poster.\n"
        f"- Spell every word correctly; keep the copy faithful to the post.\n\n"
        f"POST:\n{post}"
    )


def _white_logo(src: str | Path, height: int) -> Image.Image:
    """Load the mono lockup, recolour visible pixels to white, scale to height."""

    img = Image.open(src).convert("RGBA")
    white = Image.new("RGBA", img.size, (255, 255, 255, 0))
    white.putalpha(img.getchannel("A"))  # keep shape, paint it white
    w, h = white.size
    return white.resize(
        (max(1, round(w * height / h)), height), Image.Resampling.LANCZOS
    )


def generate_poster(
    post: str,
    out_path: str | Path,
    *,
    model: str = DEFAULT_MODEL,
    size: str = "1024x1024",
    quality: str = "high",
    final_px: int = 1200,
    logo_src: str | Path | None = LOGO_LOCKUP,
) -> Path:
    """Generate the poster via ``model`` and overlay the real logo; return path."""

    client = OpenAI()
    resp = client.images.generate(  # type: ignore[call-overload]
        model=model,
        prompt=build_poster_prompt(post),
        size=size,
        quality=quality,
    )
    raw = base64.b64decode(resp.data[0].b64_json)
    img = Image.open(io.BytesIO(raw)).convert("RGBA")

    # Normalise to the requested square size.
    if img.size != (final_px, final_px):
        img = img.resize((final_px, final_px), Image.Resampling.LANCZOS)

    # Guarantee the brand mark: overlay the real logo top-left.
    if logo_src and Path(logo_src).exists():
        logo = _white_logo(logo_src, height=round(final_px * 0.055))
        img.alpha_composite(logo, (round(final_px * 0.040), round(final_px * 0.040)))

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out)
    return out
