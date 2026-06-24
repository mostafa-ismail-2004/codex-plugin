---
name: academic-posters
description: Guidelines and mathematical patterns for programmatically generating high-quality SVG/PDF academic posters in Python.
origin: custom
---

# Programmatic SVG/PDF Academic Posters in Python

A structured guideline and code patterns for building high-quality, lightweight, and completely vector-based academic posters in Python. This skill teaches how to handle layouts, card rendering, paragraph flow, and font wrapping math inside python code.

## When to Activate

Use this skill when:
- Designing or editing programmatic SVG/PDF academic poster generators.
- Writing Python code to draw coordinates, shapes, grids, and text boxes for posters.
- Troubleshooting text truncation, overlaps, column alignment, or font size scaling in vector posters.
- Modifying layout metrics or styling themes in a poster generator such as `build_poster.py`.

---

## 1. Canvas and Grid Architecture

To ensure print-ready vector quality at any scale (including A0 or A1 sizes), define the canvas using a high-resolution, unitless grid that conforms to standard landscape dimensions:

- **Dimensions**: Width $W = 1189$, Height $H = 841$ (matches the $1.414$ aspect ratio of ISO A-series).
- **SVG Root**: Use unitless dimensions for `width` and `height`, and configure the `viewBox` matching $1:1$ with the dimensions to prevent alignment shift.
  ```python
  W, H = 1189, 841
  svg_header = f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="DejaVu Sans, Arial, sans-serif">'
  ```

### The Three-Column Layout Grid
For standard multi-column layouts, use precise margin and gap spacing. The default grid configuration is:
- **Left Margin**: $22$ px.
- **Left Column**: $x = 22$, width $w = 308$.
- **Center Column**: $x = 345$, width $w = 500$ (extra-wide for central system architectures or methodologies).
- **Right Column**: $x = 860$, width $w = 307$.
- **Right Margin**: $22$ px ($1189 - (860 + 307) = 22$).
- **Column Gaps**: $15$ px ($345 - (22 + 308) = 15$ and $860 - (345 + 500) = 15$).

### Card Vertical Alignment and Packing
Cards in columns are vertically packed with an optimal spacing of $12$ px. Maintain vertical symmetry across all columns:
- **Header Box**: $x = 22$, $y = 22$, $w = 1145$, $h = 98$.
- **Columns Starting Y**: $132$ px ($22 \text{ margin} + 98 \text{ header} + 12 \text{ gap}$).
- **Columns Ending Y**: $819$ px (leaves a $22$ px bottom margin: $841 - 819 = 22$).

---

## 2. Text Width Estimation & Wrapping Math

Since Python SVG generation does not have a layout engine (like CSS or canvas context to measure text), text widths and line breaks must be calculated manually.

### Estimating Text Width
Estimate the text width in pixels by multiplying the character length, font size ($fs$), and a weight multiplier:
- **Regular Font Weight**: $W_{\text{est}} = \text{length} \times fs \times 0.55$
- **Bold Font Weight**: $W_{\text{est}} = \text{length} \times fs \times 0.60$

```python
def estimated_width(text: str, font_size: float, is_bold: bool = False) -> float:
    multiplier = 0.60 if is_bold else 0.55
    return len(text) * font_size * multiplier
```

### Proportional Line-Wrap Algorithm
To prevent text from overflowing cards, use a greedy wrap algorithm.
1. Determine the maximum character count per line: $C_{\text{max}} = \lfloor \frac{w_{\text{max}}}{fs \times \text{multiplier}} \rfloor$.
2. Split the text into words and incrementally join them.
3. If a word exceeds $C_{\text{max}}$ on its own, split it into chunks of $C_{\text{max}}$ size.

```python
def wrap_text(text: str, font_size: float, max_width: float, is_bold: bool = False) -> list[str]:
    char_width = font_size * (0.60 if is_bold else 0.55)
    max_chars = max(4, int(max_width / char_width))
    lines = []
    current_line = ""
    
    for word in text.split():
        candidate = word if not current_line else current_line + " " + word
        if len(candidate) <= max_chars:
            current_line = candidate
        else:
            if current_line:
                lines.append(current_line)
            # Handle exceptionally long words (e.g. URLs, compounds)
            while len(word) > max_chars:
                lines.append(word[:max_chars])
                word = word[max_chars:]
            current_line = word
            
    if current_line:
        lines.append(current_line)
    return lines
```

---

## 3. Modular SVG Component Layouts

### A. Text Nodes and Paragraph Flow
Write standard SVG `<text>` elements with precise escaping. Keep track of the current vertical position ($y$) and return the updated $y$ for subsequent elements.

```python
import html

def escape_xml(s: str) -> str:
    return html.escape(str(s), quote=True)

def render_text(x: float, y: float, text: str, font_size: float, fill: str, is_bold: bool = False, anchor: str = "start", italic: bool = False) -> str:
    style_attr = ' font-style="italic"' if italic else ''
    weight_attr = '700' if is_bold else '400'
    return f'<text x="{x:.2f}" y="{y:.2f}" font-size="{font_size:.2f}" font-weight="{weight_attr}" fill="{fill}" text-anchor="{anchor}"{style_attr}>{escape_xml(text)}</text>'

def render_paragraph(x: float, y: float, max_width: float, text: str, font_size: float, fill: str, is_bold: bool = False, line_height: float = None, anchor: str = "start", accumulator: list = None) -> float:
    lh = line_height or font_size * 1.34
    lines = wrap_text(text, font_size, max_width, is_bold)
    for line in lines:
        accumulator.append(render_text(x, y, line, font_size, fill, is_bold, anchor))
        y += lh
    return y
```

### B. Bulleted Lists
Draw bullets as SVG `<circle>` nodes placed relative to the text line. Apply indentation.

```python
def render_bullets(x: float, y: float, max_width: float, items: list[str], font_size: float, fill: str, bullet_color: str, line_height: float = None, gap: float = None, accumulator: list = None) -> float:
    lh = line_height or font_size * 1.32
    gap = gap if gap is not None else font_size * 0.7
    indent = font_size * 1.3
    
    for item in items:
        # Draw the bullet circle
        cx = x + font_size * 0.42
        cy = y - font_size * 0.34
        r = font_size * 0.21
        accumulator.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{bullet_color}"/>')
        
        # Render wrapped text
        lines = wrap_text(item, font_size, max_width - indent, False)
        for line in lines:
            accumulator.append(render_text(x + indent, y, line, font_size, fill))
            y += lh
        y += gap
    return y
```

### C. Tags and Pills
Tags or pills should align horizontally and wrap to the next line dynamically if they exceed the column width limit.

```python
def render_pills(x: float, y: float, max_width: float, items: list[str], font_size: float, bg_color: str, fg_color: str, pill_height: float = None, gap: float = 4, pad_x: float = 5, line_height: float = None, accumulator: list = None) -> float:
    ph = pill_height or font_size * 2.4
    lh = line_height or ph + 4
    current_x, current_y = x, y
    
    for item in items:
        pill_width = (len(item) * font_size * 0.55) + 2 * pad_x
        # Break line if width exceeded
        if current_x + pill_width > x + max_width and current_x > x:
            current_x = x
            current_y += lh
            
        accumulator.append(f'<rect x="{current_x:.2f}" y="{current_y:.2f}" width="{pill_width:.2f}" height="{ph:.2f}" rx="{ph/2:.2f}" fill="{bg_color}"/>')
        accumulator.append(render_text(current_x + pill_width/2, current_y + ph * 0.68, item, font_size, fg_color, anchor="middle"))
        current_x += pill_width + gap
        
    return current_y + ph
```

### D. Dynamic Cards with Rounded Top Bars
A card consists of a containing border box, a colored header bar with top-only rounded corners, and a title. It returns the coordinates of the *usable interior area* $(x_{\text{inner}}, y_{\text{inner}}, w_{\text{inner}})$ to keep card content clean and isolated.

```python
def render_topbar_path(x: float, y: float, w: float, h: float, radius: float, fill: str) -> str:
    # A path that curves at the top-left and top-right but is flat at the bottom
    return (f'<path d="M{x:.2f},{y+h:.2f} L{x:.2f},{y+radius:.2f} Q{x:.2f},{y:.2f} {x+radius:.2f},{y:.2f} '
            f'L{x+w-radius:.2f},{y:.2f} Q{x+w:.2f},{y:.2f} {x+w:.2f},{y+radius:.2f} L{x+w:.2f},{y+h:.2f} Z" fill="{fill}"/>')

def render_card(x: float, y: float, w: float, h: float, title: str, header_bar_color: str, card_bg: str = "#FFFFFF", border_color: str = "#D2DCE1", header_height: float = 15, accumulator: list = None) -> tuple[float, float, float]:
    # Main outer rectangle
    accumulator.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="5" fill="{card_bg}" stroke="{border_color}" stroke-width="0.5"/>')
    # Header bar
    accumulator.append(render_topbar_path(x, y, w, header_height, 5, header_bar_color))
    # Header title text
    accumulator.append(render_text(x + 6.5, y + 10.4, title, 6.5, "#FFFFFF", is_bold=True))
    
    # Return inner bounds: x_inner, y_inner, w_inner
    return x + 7, y + header_height + 6.5, w - 14
```

### E. Flowcharts and Process Pipeling
Draw step blocks connected sequentially by lines and arrowheads.

```python
def render_flowchart(x: float, y: float, w: float, steps: list[str], bg_color: str, fg_color: str, arrow_color: str, block_height: float = 15, font_size: float = 3.7, arrow_width: float = 7, accumulator: list = None) -> float:
    n = len(steps)
    block_width = (w - (n - 1) * arrow_width) / n
    current_x = x
    
    for i, step in enumerate(steps):
        # Draw step block
        accumulator.append(f'<rect x="{current_x:.2f}" y="{y:.2f}" width="{block_width:.2f}" height="{block_height:.2f}" rx="3" fill="{bg_color}"/>')
        
        # Draw wrapped text inside step block
        lines = wrap_text(step, font_size, block_width - 2, False)
        text_y = y + block_height/2 - (len(lines) - 1) * font_size * 0.62 + font_size * 0.36
        for line in lines:
            accumulator.append(render_text(current_x + block_width/2, text_y, line, font_size, fg_color, anchor="middle"))
            text_y += font_size * 1.24
            
        # Draw connector arrow to the next block
        if i < n - 1:
            ax = current_x + block_width
            ay = y + block_height / 2
            # Line
            accumulator.append(f'<line x1="{ax+1:.2f}" y1="{ay:.2f}" x2="{ax+arrow_width-1:.2f}" y2="{ay:.2f}" stroke="{arrow_color}" stroke-width="1.1"/>')
            # Arrow tip
            tip_x = ax + arrow_width - 1
            accumulator.append(f'<path d="M{tip_x:.2f},{ay:.2f} l-2.4,-1.6 l0,3.2 Z" fill="{arrow_color}"/>')
            
        current_x += block_width + arrow_width
        
    return y + block_height
```

---

## 4. Visual Themes & Assets

### Safe Base64 Asset Ingestion
Always provide a fallback mechanism when loading external png/jpg assets so that the build script never crashes if files are relocated or missing.

```python
import os
import base64

def load_base64_image(file_path: str) -> str:
    if not os.path.exists(file_path):
        # 1x1 transparent pixel placeholder
        return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()
```

### Color Palette Consistency
Ensure all components adhere to a defined theme palette. Use dark colors for titles/headers, vibrant accents for chips/pills/bullets, and light shades for background colors:
```python
# Theme Palette Definition
NAVY     = "#1E4A57"  # Main headers & card bar
GREEN    = "#149E7E"  # Accent green
GREEN_D  = "#0E7D63"  # Highlight dark green
BLUE     = "#2E6E8E"  # Secondary accents (figures/stats)
PAGE     = "#EDF2F4"  # Background page color
CARD     = "#FFFFFF"  # Card background
BORDER   = "#D2DCE1"  # Structural border gray
TEXT     = "#243B43"  # High-contrast readable body text
MUTED    = "#5A6B72"  # Supporting text
WHITE    = "#FFFFFF"  # Bright white
LTEAL    = "#A7DACD"  # Header metadata teal
SUBT     = "#D7E8EC"  # Header subtitle
CHIP     = "#EEF4F5"  # Stat chip background
SLATE    = "#6E8B98"  # Flowchart arrow neutral
```

---

## 5. Build and Export Workflow

1. **Write Output File**: Save the accumulated SVG elements wrapped in the SVG header and footer tags.
   ```python
   with open("poster.svg", "w") as f:
       f.write("\n".join(accumulator_list))
   ```
2. **Convert to PDF**: Print the generated `poster.svg` to a high-quality PDF.
   - For perfect outputs, open in a browser (like Firefox) and choose **Print to PDF** with **Background Graphics** enabled and margins set to **None**.

---

## 6. Anti-Patterns to Avoid

- **No physical units in SVG Root**: Never write `width="1189mm"` or `height="841mm"`. Always keep them unitless (`width="1189" viewBox="0 0 1189 841"`) to prevent browsers from resizing or clipping coordinates.
- **Hardcoded Paragraph Line Ends**: Do not hardcode line breaks in paragraphs. Always use the `wrap_text` algorithm to handle wrapping dynamically based on column widths.
- **No Unescaped XML Characters**: Writing raw `&`, `<`, or `>` inside a text node will break XML formatting. Always run text through an escape function (e.g. `html.escape()`).
- **Unsafely Loading Image Files**: Running `open(path, 'rb')` without a check will crash the script if the image is missing. Always use a fallback base64 string helper.
- **Fixed/Overlapping Y Layouts**: Do not hardcode Y coordinates for consecutive paragraphs or bullet points inside a card. Always calculate and pass the returned Y coordinate from the helper layout functions.
