"""
Compose canonical 7-block icons into a system design PNG.

Reads a structured design (nodes + edges), uses networkx for auto-layout,
and PIL to composite icons + labels + arrows into a single PNG that
matches the visual identity of the Systems Thinking Lab videos.

CLI:
    python render.py design.json -o architecture.png
    cat design.json | python render.py - -o architecture.png

Library:
    from render import render
    render(design, "architecture.png")
"""
from PIL import Image, ImageDraw, ImageFont
import networkx as nx
from pathlib import Path
import math
import json
import sys
import argparse

ICON_DIR = Path(__file__).parent / "icons"

ICON_FILES = {
    "service": "service.png",
    "worker": "worker.png",
    "queue": "queue.png",
    "key_value_store": "key_value_store.png",
    "file_store": "file_store.png",
    "relational_database": "relational_db.png",
    "vector_database": "vector_db.png",
    "user": "user.png",
    "external_service": "external_service.png",
    "time": "time.png",
}

BLOCK_NAMES = {
    "service": "Service",
    "worker": "Worker",
    "queue": "Queue",
    "key_value_store": "Key-Value Store",
    "file_store": "File Store",
    "relational_database": "Relational Database",
    "vector_database": "Vector Database",
    "user": "User",
    "external_service": "External Service",
    "time": "Time",
}

# Categories in the legend: each category gets its own row(s) so the
# type grouping is visually obvious.
LEGEND_CATEGORIES = [
    ("Task", ["service", "worker"]),
    ("Storage", ["queue", "key_value_store", "file_store", "relational_database", "vector_database"]),
    ("External Forces", ["user", "external_service", "time"]),
]
LEGEND_ORDER = [t for _, ts in LEGEND_CATEGORIES for t in ts]

LEGEND_ICON_SIZE = 48
LEGEND_LABEL_FONT_SIZE = 16
LEGEND_GAP_X = 24
LEGEND_GAP_Y = 16
LEGEND_LABEL_GAP = 10
LEGEND_TOP_PAD = 30
LEGEND_BOTTOM_PAD = 30

TECH_TABLE_TITLE_FONT_SIZE = 17
TECH_TABLE_FONT_SIZE = 15
TECH_TABLE_ROW_GAP = 8
TECH_TABLE_COL_GAP = 50
TECH_TABLE_TOP_PAD = 16
TECH_TABLE_BOTTOM_PAD = 50
TECH_TABLE_HEADER_COLOR = (130, 130, 130, 255)
TECH_TABLE_DIVIDER_COLOR = (210, 210, 210, 255)

ICON_SIZE = 130
LABEL_GAP = 18
LABEL_FONT_SIZE = 20
CANVAS_PAD = 80
HORIZONTAL_GAP = 80   # between nodes in same rank
VERTICAL_GAP = 130    # between ranks (room for label + arrow)
ARROW_HEAD = 14
ARROW_WIDTH = 3
ARROW_COLOR = (60, 60, 60, 255)
LABEL_COLOR = (40, 40, 40, 255)
BG_COLOR = (255, 255, 255, 255)
LABEL_HEIGHT = 40     # reserved vertical space for label under each icon


_icon_cache = {}

def load_icon(block_type, size=ICON_SIZE):
    cache_key = (block_type, size)
    if cache_key in _icon_cache:
        return _icon_cache[cache_key]
    path = ICON_DIR / ICON_FILES[block_type]
    icon = Image.open(path).convert("RGBA")
    bbox = icon.getbbox()
    if bbox:
        icon = icon.crop(bbox)
    icon.thumbnail((size, size), Image.LANCZOS)
    _icon_cache[cache_key] = icon
    return icon


def layout_legend(types_used, font, max_width):
    """
    Group legend entries by category (Task / Storage / External Forces). Each
    category gets its own row, so the type grouping reads at a glance. If a
    category's row exceeds max_width, wrap within that category.
    Returns (rows, total_h) where rows is a list of lists of
    (block_type, entry_width, label_text).
    """
    types_set = set(types_used)
    rows = []
    for _, type_list in LEGEND_CATEGORIES:
        # entries in this category, in canonical order
        cat_entries = []
        for t in type_list:
            if t not in types_set:
                continue
            label = BLOCK_NAMES[t]
            bbox = font.getbbox(label)
            label_w = bbox[2] - bbox[0]
            entry_w = LEGEND_ICON_SIZE + LEGEND_LABEL_GAP + label_w
            cat_entries.append((t, entry_w, label))
        if not cat_entries:
            continue

        # wrap within category if needed
        current_row = []
        for entry in cat_entries:
            if current_row and (current_row_width(current_row) + LEGEND_GAP_X + entry[1] > max_width):
                rows.append(current_row)
                current_row = [entry]
            else:
                current_row.append(entry)
        if current_row:
            rows.append(current_row)

    row_h = LEGEND_ICON_SIZE
    total_h = len(rows) * row_h + (len(rows) - 1) * LEGEND_GAP_Y
    return rows, total_h


def current_row_width(row):
    return sum(e[1] for e in row) + LEGEND_GAP_X * (len(row) - 1)


def layout_tech_table(nodes_with_tech, font, title_font):
    """
    Compute dimensions for a 2-column tech-choices table.
    Returns (rows, total_h, col1_w, col2_w, title_h, row_h).
    """
    if not nodes_with_tech:
        return [], 0, 0, 0, 0, 0
    rows = [(n["label"], n["tech"]) for n in nodes_with_tech]
    col1_w = max((font.getbbox(label)[2] - font.getbbox(label)[0]) for label, _ in rows)
    col2_w = max((font.getbbox(tech)[2] - font.getbbox(tech)[0]) for _, tech in rows)

    sample_bbox = font.getbbox("Ay")
    row_h = (sample_bbox[3] - sample_bbox[1]) + TECH_TABLE_ROW_GAP

    title_bbox = title_font.getbbox("Technology choices")
    title_h = (title_bbox[3] - title_bbox[1]) + 14

    total_h = title_h + row_h * (len(rows) + 1) + 6
    return rows, total_h, col1_w, col2_w, title_h, row_h


def render_tech_table(canvas, draw, nodes_with_tech, top_y, region_left, region_right, font, title_font):
    """
    Draw a 2-column tech table centered within [region_left, region_right].
    Returns the y where the table ends.
    """
    if not nodes_with_tech:
        return top_y
    rows, _total_h, col1_w, col2_w, title_h, row_h = layout_tech_table(
        nodes_with_tech, font, title_font
    )
    region_w = region_right - region_left

    title = "Technology choices"
    title_bbox = title_font.getbbox(title)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(
        (region_left + (region_w - title_w) / 2, top_y),
        title,
        fill=LABEL_COLOR,
        font=title_font,
    )

    table_w = col1_w + TECH_TABLE_COL_GAP + col2_w
    x_start = region_left + (region_w - table_w) / 2
    y = top_y + title_h

    draw.text((x_start, y), "Block", fill=TECH_TABLE_HEADER_COLOR, font=font)
    draw.text((x_start + col1_w + TECH_TABLE_COL_GAP, y), "Technology",
              fill=TECH_TABLE_HEADER_COLOR, font=font)
    y += row_h

    draw.line(
        [(x_start - 10, y - 4), (x_start + table_w + 10, y - 4)],
        fill=TECH_TABLE_DIVIDER_COLOR,
        width=1,
    )

    for label, tech in rows:
        draw.text((x_start, y), label, fill=LABEL_COLOR, font=font)
        draw.text((x_start + col1_w + TECH_TABLE_COL_GAP, y), tech,
                  fill=LABEL_COLOR, font=font)
        y += row_h

    return y


def render_legend(canvas, draw, types_used, top_y, region_left, region_right, font):
    """
    Draw legend rows centered within [region_left, region_right] starting at
    top_y. Returns the y where the legend ends.
    """
    region_w = region_right - region_left
    rows, _total_h = layout_legend(types_used, font, region_w)
    y = top_y
    for row in rows:
        row_w = current_row_width(row)
        x = region_left + (region_w - row_w) / 2
        for block_type, entry_w, label in row:
            icon = load_icon(block_type, size=LEGEND_ICON_SIZE)
            ix = int(x + (LEGEND_ICON_SIZE - icon.width) / 2)
            iy = int(y + (LEGEND_ICON_SIZE - icon.height) / 2)
            canvas.paste(icon, (ix, iy), icon)

            label_x = x + LEGEND_ICON_SIZE + LEGEND_LABEL_GAP
            bbox = font.getbbox(label)
            label_h = bbox[3] - bbox[1]
            label_y = y + (LEGEND_ICON_SIZE - label_h) / 2 - 2
            draw.text((label_x, label_y), label, fill=LABEL_COLOR, font=font)

            x += entry_w + LEGEND_GAP_X
        y += LEGEND_ICON_SIZE + LEGEND_GAP_Y
    return y - LEGEND_GAP_Y


def get_font(size):
    for candidate in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ]:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def draw_arrowhead(draw, tip, direction, head=ARROW_HEAD):
    """direction: 'down', 'up', 'left', 'right'"""
    tx, ty = tip
    if direction == "down":
        pts = [(tx, ty), (tx - head / 2, ty - head), (tx + head / 2, ty - head)]
    elif direction == "up":
        pts = [(tx, ty), (tx - head / 2, ty + head), (tx + head / 2, ty + head)]
    elif direction == "right":
        pts = [(tx, ty), (tx - head, ty - head / 2), (tx - head, ty + head / 2)]
    else:  # left
        pts = [(tx, ty), (tx + head, ty - head / 2), (tx + head, ty + head / 2)]
    draw.polygon(pts, fill=ARROW_COLOR)


def pick_sides(s_pos, t_pos):
    """
    Heuristic for which icon side an edge exits/enters.
    - Same column (|dx| small): always vertical (top/bottom).
    - Different columns: only use vertical when dy is much larger than dx
      (>= 2.5x) so accidental near-vertical pairs still route horizontally.
    Returns (source_exit_side, target_entry_side).
    """
    sx, sy = s_pos
    tx, ty = t_pos
    dx = tx - sx
    dy = ty - sy

    SAME_COLUMN_THRESHOLD = 50
    VERTICAL_DOMINANCE = 2.5

    if abs(dx) < SAME_COLUMN_THRESHOLD:
        if dy > 0:
            return ("bottom", "top")
        return ("top", "bottom")

    if abs(dy) > abs(dx) * VERTICAL_DOMINANCE:
        if dy > 0:
            return ("bottom", "top")
        return ("top", "bottom")

    if dx >= 0:
        return ("right", "left")
    return ("left", "right")


def side_exit_point(node_pos, half_w, half_h, side, src_offset=0, label_clearance=LABEL_HEIGHT):
    """
    Compute the exit/entry pixel for a given side, with src_offset spreading
    along that edge so multiple edges on the same side don't overlap.
    For BOTTOM, the exit is past the label so the arrow doesn't run through it.
    """
    x, y = node_pos
    if side == "right":
        return (x + half_w + 4, y + src_offset)
    if side == "left":
        return (x - half_w - 4, y + src_offset)
    if side == "top":
        return (x + src_offset, y - half_h - 4)
    if side == "bottom":
        return (x + src_offset, y + half_h + label_clearance + 4)


_arrow_dir_for_entry_side = {
    "left": "right",   # entering left side → arrow points right (into icon)
    "right": "left",
    "top": "down",
    "bottom": "up",
}


def draw_orthogonal_arrow(
    draw, start, end, source_half, target_half,
    src_side, tgt_side, src_offset=0, tgt_offset=0, mid_offset=0,
    width=ARROW_WIDTH,
):
    """
    Manhattan-routed arrow that may exit/enter any of the 4 sides.
    src_side/tgt_side: 'left', 'right', 'top', 'bottom'.
    Routing pattern depends on the combination:
      - both horizontal sides → H-V-H Z-shape
      - both vertical sides   → V-H-V Z-shape
      - mixed                 → 2-segment L-shape
    """
    s_half_w, s_half_h = source_half
    t_half_w, t_half_h = target_half

    s_exit = side_exit_point(start, s_half_w, s_half_h, src_side, src_offset)
    t_entry = side_exit_point(end, t_half_w, t_half_h, tgt_side, tgt_offset)
    entry_dir = _arrow_dir_for_entry_side[tgt_side]

    s_horizontal = src_side in ("left", "right")
    t_horizontal = tgt_side in ("left", "right")

    if s_horizontal and t_horizontal:
        # H-V-H Z-shape with vertical jog at mid_x + offset
        mid_x = (s_exit[0] + t_entry[0]) / 2 + mid_offset
        pts = [s_exit, (mid_x, s_exit[1]), (mid_x, t_entry[1]), t_entry]
    elif (not s_horizontal) and (not t_horizontal):
        # V-H-V Z-shape with horizontal jog at mid_y + offset
        mid_y = (s_exit[1] + t_entry[1]) / 2 + mid_offset
        pts = [s_exit, (s_exit[0], mid_y), (t_entry[0], mid_y), t_entry]
    elif s_horizontal and not t_horizontal:
        # exit horizontally, enter vertically: L-shape via (target.x, source.y)
        pts = [s_exit, (t_entry[0], s_exit[1]), t_entry]
    else:
        # exit vertically, enter horizontally: L-shape via (source.x, target.y)
        pts = [s_exit, (s_exit[0], t_entry[1]), t_entry]

    for a, b in zip(pts, pts[1:]):
        # collapse zero-length segments
        if abs(a[0] - b[0]) > 0.5 or abs(a[1] - b[1]) > 0.5:
            draw.line([a, b], fill=ARROW_COLOR, width=width)

    draw_arrowhead(draw, t_entry, entry_dir)


def compute_edge_routing(edges, pos, icon_dims):
    """
    For every edge, decide:
      - which side of source it exits (left/right/top/bottom)
      - which side of target it enters
      - per-edge offsets along those sides so multiple edges sharing a
        source-side or target-side get distinct tracks
      - a globally unique mid-axis offset for the Z-shape jog so unrelated
        edges that share areas don't visually merge
    """
    from collections import defaultdict

    routing = {}
    for e in edges:
        src_side, tgt_side = pick_sides(pos[e["from"]], pos[e["to"]])
        routing[(e["from"], e["to"])] = {
            "src_side": src_side,
            "tgt_side": tgt_side,
            "src_offset": 0,
            "tgt_offset": 0,
            "mid_offset": 0,
        }

    # spread edges that share BOTH source and same exit side
    src_side_groups = defaultdict(list)
    for e in edges:
        key = (e["from"], routing[(e["from"], e["to"])]["src_side"])
        src_side_groups[key].append(e)

    for (src_id, side), group in src_side_groups.items():
        n = len(group)
        if n == 1:
            continue
        half_w, half_h = icon_dims[src_id]
        # for top/bottom, spread along x; for left/right, spread along y
        spread = (half_w if side in ("top", "bottom") else half_h) * 1.4
        # sort by where the edge is going so adjacent tracks go to adjacent targets
        if side in ("left", "right"):
            group.sort(key=lambda e: pos[e["to"]][1])  # by target y
        else:
            group.sort(key=lambda e: pos[e["to"]][0])  # by target x
        for i, e in enumerate(group):
            frac = i / (n - 1) - 0.5
            routing[(e["from"], e["to"])]["src_offset"] = frac * spread

    # spread edges that share BOTH target and same entry side
    tgt_side_groups = defaultdict(list)
    for e in edges:
        key = (e["to"], routing[(e["from"], e["to"])]["tgt_side"])
        tgt_side_groups[key].append(e)

    for (tgt_id, side), group in tgt_side_groups.items():
        n = len(group)
        if n == 1:
            continue
        half_w, half_h = icon_dims[tgt_id]
        spread = (half_w if side in ("top", "bottom") else half_h) * 1.4
        if side in ("left", "right"):
            group.sort(key=lambda e: pos[e["from"]][1])
        else:
            group.sort(key=lambda e: pos[e["from"]][0])
        for i, e in enumerate(group):
            frac = i / (n - 1) - 0.5
            routing[(e["from"], e["to"])]["tgt_offset"] = frac * spread

    # GLOBAL unique mid offset: every Z-shape jog gets its own lane
    sorted_edges = sorted(
        edges,
        key=lambda e: (pos[e["from"]][0], pos[e["from"]][1], pos[e["to"]][0]),
    )
    n_total = len(sorted_edges)
    pitch = 14
    for i, e in enumerate(sorted_edges):
        routing[(e["from"], e["to"])]["mid_offset"] = (i - (n_total - 1) / 2) * pitch

    return routing


def assign_ranks(G):
    """
    Layered layout: each node's rank is its longest-path depth from any source.
    Returns dict node_id -> rank int (0 = leftmost column).
    """
    rank = {}
    sources = [n for n in G.nodes if G.in_degree(n) == 0]
    if not sources:
        sources = [min(G.nodes, key=lambda n: G.in_degree(n))]
    for n in nx.topological_sort(G) if nx.is_directed_acyclic_graph(G) else G.nodes:
        preds = list(G.predecessors(n))
        rank[n] = max((rank[p] + 1 for p in preds if p in rank), default=0)
    return rank


ENTITY_TYPES = {"user", "external_service", "time"}


def relocate_entities(G, rank, nodes):
    """
    Pull external entity nodes (User, External Service, Time) next to whatever
    they connect to instead of forcing them into rank 0. Mirrors how Kay's
    videos draw them on a whiteboard: the entity sits adjacent to its
    connection point, not in a far-left "source" column.
    """
    type_by_id = {n["id"]: n["type"] for n in nodes}
    for nid, ntype in type_by_id.items():
        if ntype not in ENTITY_TYPES:
            continue
        outs = list(G.successors(nid))
        ins = list(G.predecessors(nid))
        if outs and not ins:
            # source-only entity → place one rank before its earliest target
            rank[nid] = max(0, min(rank[t] for t in outs) - 1)
        elif ins and not outs:
            # sink-only entity → place one rank after its latest source
            rank[nid] = max(rank[s] for s in ins) + 1
        # if entity has both incoming and outgoing edges, leave longest-path rank


def order_within_rank(G, rank):
    """Group nodes by rank, then for each rank sort by barycenter of parents'
    positions in the previous rank to reduce edge crossings."""
    layers = {}
    for n, r in rank.items():
        layers.setdefault(r, []).append(n)
    # initial sort: insertion order (stable across runs since we walk node list)
    ordered = {r: list(nodes) for r, nodes in layers.items()}
    # refine: barycenter sweep
    for _ in range(2):
        for r in sorted(ordered):
            if r == 0:
                continue
            prev = ordered[r - 1]
            prev_idx = {n: i for i, n in enumerate(prev)}
            def bary(n):
                preds = [p for p in G.predecessors(n) if p in prev_idx]
                if not preds:
                    return 0
                return sum(prev_idx[p] for p in preds) / len(preds)
            ordered[r].sort(key=bary)
    return ordered


def render(design, output_path):
    nodes = design["nodes"]
    edges = design["edges"]

    G = nx.DiGraph()
    for node in nodes:
        G.add_node(node["id"])
    for edge in edges:
        G.add_edge(edge["from"], edge["to"])

    rank = assign_ranks(G)
    relocate_entities(G, rank, nodes)
    layers = order_within_rank(G, rank)

    # left-to-right layout: each rank is a vertical column
    max_layer_height = max(len(nodes_in) for nodes_in in layers.values())
    num_layers = max(layers) + 1
    cell_w = ICON_SIZE + HORIZONTAL_GAP
    cell_h = ICON_SIZE + LABEL_HEIGHT + VERTICAL_GAP

    canvas_w = num_layers * cell_w + CANVAS_PAD * 2

    # bottom strip is split: legend on left half, tech table on right half.
    # Each gets ~half the canvas width minus padding and a center gap.
    legend_font = get_font(LEGEND_LABEL_FONT_SIZE)
    tech_font = get_font(TECH_TABLE_FONT_SIZE)
    tech_title_font = get_font(TECH_TABLE_TITLE_FONT_SIZE)
    types_used = sorted(
        {n["type"] for n in nodes},
        key=lambda t: LEGEND_ORDER.index(t) if t in LEGEND_ORDER else 999,
    )
    nodes_with_tech = [n for n in nodes if n.get("tech")]

    BOTTOM_CENTER_GAP = 80
    half_w = (canvas_w - 2 * CANVAS_PAD - BOTTOM_CENTER_GAP) / 2
    _, legend_h = layout_legend(types_used, legend_font, half_w)
    _, tech_h, _, _, _, _ = layout_tech_table(nodes_with_tech, tech_font, tech_title_font)

    bottom_strip_h = max(legend_h, tech_h)
    bottom_total_h = LEGEND_TOP_PAD + bottom_strip_h + LEGEND_BOTTOM_PAD if (legend_h or tech_h) else 0

    canvas_h = max(700, max_layer_height * cell_h + CANVAS_PAD * 2 + 100) + bottom_total_h

    # pixel positions: rank → x. y is computed via barycenter so each column's
    # nodes sit near their predecessors, preventing horizontal alignment with
    # neighboring columns by accident.
    pos = {}
    usable_h_top = CANVAS_PAD + 70
    usable_h_bottom = canvas_h - CANVAS_PAD - 50 - bottom_total_h
    usable_h = usable_h_bottom - usable_h_top
    min_node_spacing = ICON_SIZE + LABEL_HEIGHT + 40

    for r in sorted(layers.keys()):
        nodes_in = layers[r]
        px = CANVAS_PAD + 80 + r * cell_w
        n = len(nodes_in)

        if r == 0:
            # rank 0: evenly space along usable height
            spacing = usable_h / (n + 1)
            for i, nid in enumerate(nodes_in):
                py = usable_h_top + spacing * (i + 1)
                pos[nid] = (px, py)
        else:
            # for each node, compute a "preferred" y from its predecessors' actual y
            preferred = []
            for nid in nodes_in:
                pred_ys = [pos[p][1] for p in G.predecessors(nid) if p in pos]
                bary = sum(pred_ys) / len(pred_ys) if pred_ys else (usable_h_top + usable_h_bottom) / 2
                preferred.append((nid, bary))
            preferred.sort(key=lambda x: x[1])

            # place nodes evenly spaced but centered on average preferred y
            spacing = max(min_node_spacing, usable_h / (n + 1))
            total_h = (n - 1) * spacing
            avg = sum(b for _, b in preferred) / n
            start_y = avg - total_h / 2
            start_y = max(usable_h_top, min(usable_h_bottom - total_h, start_y))

            for i, (nid, _) in enumerate(preferred):
                pos[nid] = (px, start_y + i * spacing)

    canvas = Image.new("RGBA", (canvas_w, canvas_h), BG_COLOR)
    draw = ImageDraw.Draw(canvas)
    font = get_font(LABEL_FONT_SIZE)

    # cache icon dimensions so arrows know where icon edges actually are
    icon_dims = {}
    for node in nodes:
        icon = load_icon(node["type"])
        icon_dims[node["id"]] = (icon.width / 2, icon.height / 2)

    # compute per-edge routing (sides + offsets) for distinct tracks
    routing = compute_edge_routing(edges, pos, icon_dims)

    # arrows first so they sit behind icons
    for edge in edges:
        src_id = edge["from"]
        tgt_id = edge["to"]
        r = routing[(src_id, tgt_id)]
        draw_orthogonal_arrow(
            draw,
            pos[src_id],
            pos[tgt_id],
            icon_dims[src_id],
            icon_dims[tgt_id],
            src_side=r["src_side"],
            tgt_side=r["tgt_side"],
            src_offset=r["src_offset"],
            tgt_offset=r["tgt_offset"],
            mid_offset=r["mid_offset"],
        )

    # icons + labels (drawn on top so arrows don't show through icon transparency)
    # Labels get a white background rect to "mask out" any arrow lines passing
    # behind them so the type label always reads clearly.
    for node in nodes:
        nid = node["id"]
        icon = load_icon(node["type"])
        x, y = pos[nid]
        ix = int(x - icon.width / 2)
        iy = int(y - icon.height / 2)
        canvas.paste(icon, (ix, iy), icon)

        label = node.get("label", node["type"].replace("_", " ").title())
        bbox = draw.textbbox((0, 0), label, font=font)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        lx = int(x - lw / 2)
        ly = int(iy + icon.height + LABEL_GAP)
        # white pad behind label to mask any arrow lines crossing through
        draw.rectangle(
            [lx - 6, ly - 4, lx + lw + 6, ly + lh + 6],
            fill=BG_COLOR,
        )
        draw.text((lx, ly), label, fill=LABEL_COLOR, font=font)

    # title and footer
    title = design.get("title", "System Design")
    title_font = get_font(28)
    bbox = draw.textbbox((0, 0), title, font=title_font)
    draw.text(
        (canvas_w / 2 - (bbox[2] - bbox[0]) / 2, 20),
        title,
        fill=LABEL_COLOR,
        font=title_font,
    )

    # legend on left half, tech-choices table on right half
    bottom_y = usable_h_bottom + LEGEND_TOP_PAD
    left_l = CANVAS_PAD
    left_r = CANVAS_PAD + half_w
    right_l = CANVAS_PAD + half_w + BOTTOM_CENTER_GAP
    right_r = canvas_w - CANVAS_PAD

    render_legend(canvas, draw, types_used, bottom_y, left_l, left_r, legend_font)
    if nodes_with_tech:
        render_tech_table(
            canvas, draw, nodes_with_tech, bottom_y, right_l, right_r,
            tech_font, tech_title_font,
        )

    footer = "Designed with the 7 Building Blocks framework  ·  systemthinkinglab.ai"
    footer_font = get_font(14)
    bbox = draw.textbbox((0, 0), footer, font=footer_font)
    draw.text(
        (canvas_w / 2 - (bbox[2] - bbox[0]) / 2, canvas_h - 30),
        footer,
        fill=(120, 120, 120, 255),
        font=footer_font,
    )

    canvas.convert("RGB").save(output_path, "PNG", optimize=True)
    return output_path


SAMPLE = {
    "title": "Recipe App Architecture",
    "nodes": [
        {"id": "user", "type": "user", "label": "User"},
        {"id": "ext", "type": "external_service", "label": "Payments", "tech": "Stripe"},
        {"id": "time", "type": "time", "label": "Time", "tech": "Cron"},
        {"id": "recipe", "type": "service", "label": "Recipe Service", "tech": "Render Web Service"},
        {"id": "worker", "type": "worker", "label": "Photo Worker", "tech": "Render Background Worker"},
        {"id": "cache", "type": "key_value_store", "label": "Cache", "tech": "Redis"},
        {"id": "files", "type": "file_store", "label": "User Photos", "tech": "S3"},
        {"id": "pgsql", "type": "relational_database", "label": "Recipe DB", "tech": "Postgres"},
        {"id": "vec", "type": "vector_database", "label": "Embeddings", "tech": "pgvector"},
        {"id": "queue", "type": "queue", "label": "Photo Jobs", "tech": "BullMQ"},
    ],
    "edges": [
        {"from": "user", "to": "recipe"},
        {"from": "recipe", "to": "cache"},
        {"from": "recipe", "to": "pgsql"},
        {"from": "recipe", "to": "vec"},
        {"from": "recipe", "to": "queue"},
        {"from": "queue", "to": "worker"},
        {"from": "worker", "to": "files"},
        {"from": "worker", "to": "pgsql"},
        {"from": "recipe", "to": "ext"},
        {"from": "time", "to": "worker"},
    ],
}

def main():
    parser = argparse.ArgumentParser(
        description="Render a system design diagram as PNG using the 7 building blocks."
    )
    parser.add_argument(
        "design_path",
        nargs="?",
        default="-",
        help="Path to design JSON file. Use '-' (default) to read from stdin.",
    )
    parser.add_argument(
        "-o", "--output",
        default="architecture.png",
        help="Output PNG path (default: architecture.png).",
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Render the bundled sample design instead of reading input.",
    )
    args = parser.parse_args()

    if args.sample:
        design = SAMPLE
    elif args.design_path == "-":
        design = json.load(sys.stdin)
    else:
        with open(args.design_path) as f:
            design = json.load(f)

    out = render(design, args.output)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
