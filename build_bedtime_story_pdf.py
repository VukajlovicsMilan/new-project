from pathlib import Path

TITLE = "The Little Lantern and the Moonbeam Path"
OUTPUT = Path("bedtime_story_children_book.pdf")

pages = [
    ("Page 1 — A Soft, Starry Night", "Mina, a tiny fox, lived at the edge of Whispering Woods. Each night she carried a little lantern to walk home after helping her grandma. Tonight the wind was gentle, and the stars blinked like sleepy fireflies.", "Illustration prompt: A small orange fox with a glowing lantern on a forest path at dusk, soft stars in the sky, warm bedtime colors."),
    ("Page 2 — The Lantern Goes Dim", "As Mina crossed the mossy bridge, her lantern flickered and grew dim. \"Oh dear,\" she whispered, \"I can barely see the path.\" She hugged the lantern close and took very careful steps.", "Illustration prompt: Tiny fox on a wooden bridge over a stream, lantern light fading, calm night scene with moonlight."),
    ("Page 3 — A Lost Little Beetle", "Near a fern, Mina heard a tiny sniffle. A little blue beetle was turned around and could not find his leaf home. Mina knelt down and said, \"I will help you.\"", "Illustration prompt: Fox kneeling beside a small blue beetle near big green ferns, dim lantern glow, gentle expressions."),
    ("Page 4 — Sharing the Light", "Mina pointed her lantern so the beetle could see a shiny trail of dew. The beetle followed the sparkling drops and smiled. \"Thank you, Mina,\" he said, bowing politely.", "Illustration prompt: Dew drops glowing in lantern light, beetle happily walking toward a leaf, fox smiling kindly."),
    ("Page 5 — A Nervous Bunny", "Farther down the path, Mina found a bunny with trembling ears. \"I heard an owl hoot,\" said the bunny, \"and now I am scared to hop alone.\" Mina offered, \"Come beside me. We can be brave together.\"", "Illustration prompt: Small bunny beside fox on a forest path, cozy lantern between them, trees and moon above."),
    ("Page 6 — Two Friends, One Path", "The bunny and Mina walked slowly, listening to crickets sing. They counted their breaths: one, two, three, and the bunny felt calmer. Soon, the bunny's home burrow came into view.", "Illustration prompt: Fox and bunny walking side by side, calm forest sounds implied, warm lantern glow leading to a burrow."),
    ("Page 7 — A Heavy Basket", "At the hill, Mina met old Mrs. Hedgehog carrying berries in a basket. The basket was so heavy that she had to stop and rest. Mina and the bunny each carried a small handful to help.", "Illustration prompt: Friendly hedgehog with berry basket, fox and bunny helping carry berries up a little hill, moonlit night."),
    ("Page 8 — The Moonbeam Path", "When they reached the top, clouds drifted away and the moon shone bright. Silver moonbeams stretched across the trail like ribbons. \"Look,\" said Mrs. Hedgehog, \"your kindness made more light than one lantern.\"", "Illustration prompt: Forest hilltop with bright moonbeams across path, three friends looking amazed, magical but gentle mood."),
    ("Page 9 — A Circle of Helpers", "The beetle returned and offered to guide them around puddles. The bunny listened for safe sounds ahead. Mrs. Hedgehog shared sweet berries for everyone.", "Illustration prompt: Beetle, bunny, fox, and hedgehog moving together as a team, tiny details of berries and puddles, cozy harmony."),
    ("Page 10 — Home at Last", "At last Mina reached her little den under the oak tree. Her lantern was almost out, but her heart felt bright and full. She thanked her friends and waved goodnight.", "Illustration prompt: Fox at a cozy den doorway under a big oak, friends waving goodbye, lantern nearly out, warm bedtime feeling."),
    ("Page 11 — A Gentle Promise", "Before sleeping, Mina looked out her window at the moonbeam path. \"Tomorrow,\" she whispered, \"I will help again whenever I can.\" The stars twinkled as if they agreed.", "Illustration prompt: Fox tucked in bed by a window, moonlit path visible outside, stars twinkling softly, peaceful bedtime room."),
    ("Page 12 — Goodnight, Whispering Woods", "In Whispering Woods, everyone rested safely that night. One small lantern, shared with love, had guided many feet home. And that is how kindness became the brightest light of all.", "Illustration prompt: Wide view of peaceful forest homes at night, soft moon and stars, a gentle glow connecting all homes."),
]


def pdf_escape(s: str) -> str:
    return s.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')


def wrap_text(text: str, max_chars: int):
    words = text.split()
    lines = []
    current = []
    length = 0
    for w in words:
        add = len(w) if not current else len(w) + 1
        if length + add <= max_chars:
            current.append(w)
            length += add
        else:
            lines.append(" ".join(current))
            current = [w]
            length = len(w)
    if current:
        lines.append(" ".join(current))
    return lines


contents = []

for title, body, prompt in pages:
    lines = [
        "BT /F1 24 Tf",
        "72 760 Td",
        f"({pdf_escape(TITLE)}) Tj",
        "0 -36 Td",
        "BT /F1 18 Tf 72 700 Td",
        f"({pdf_escape(title)}) Tj",
        "ET",
        "BT /F1 13 Tf 72 660 Td",
    ]
    first = True
    for ln in wrap_text(body, 78):
        if not first:
            lines.append("0 -20 Td")
        lines.append(f"({pdf_escape(ln)}) Tj")
        first = False
    lines += ["ET", "BT /F1 12 Tf 72 560 Td"]
    first = True
    for ln in wrap_text(prompt, 85):
        if not first:
            lines.append("0 -18 Td")
        lines.append(f"({pdf_escape(ln)}) Tj")
        first = False
    lines.append("ET")
    stream = "\n".join(lines) + "\n"
    contents.append(stream)

objects = []

# 1 Catalog
objects.append("<< /Type /Catalog /Pages 2 0 R >>")

# 2 Pages (kids references filled later)
kids = [f"{4 + i*2} 0 R" for i in range(len(contents))]
objects.append(f"<< /Type /Pages /Count {len(contents)} /Kids [{' '.join(kids)}] >>")

# 3 Font
objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

# page + content objects
for i, stream in enumerate(contents):
    page_obj_num = 4 + i * 2
    content_obj_num = page_obj_num + 1
    page_obj = (
        "<< /Type /Page /Parent 2 0 R "
        "/MediaBox [0 0 612 792] "
        "/Resources << /Font << /F1 3 0 R >> >> "
        f"/Contents {content_obj_num} 0 R >>"
    )
    objects.append(page_obj)
    content_obj = f"<< /Length {len(stream.encode('cp1252'))} >>\nstream\n{stream}endstream"
    objects.append(content_obj)

pdf = ["%PDF-1.4\n"]
offsets = [0]

for idx, obj in enumerate(objects, start=1):
    offsets.append(sum(len(part.encode("cp1252")) for part in pdf))
    pdf.append(f"{idx} 0 obj\n{obj}\nendobj\n")

xref_pos = sum(len(part.encode("cp1252")) for part in pdf)
pdf.append(f"xref\n0 {len(objects)+1}\n")
pdf.append("0000000000 65535 f \n")
for off in offsets[1:]:
    pdf.append(f"{off:010d} 00000 n \n")

pdf.append(
    f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n"
)

OUTPUT.write_bytes("".join(pdf).encode("cp1252"))
print(f"Wrote {OUTPUT}")
