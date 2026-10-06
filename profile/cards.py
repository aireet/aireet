#!/usr/bin/env python3
"""Renders the project and contribution cards of the profile README as SVG, in a light and
a dark variant. Run it after editing the content below: python3 profile/cards.py"""

import base64
import html
import pathlib

HERE = pathlib.Path(__file__).parent

PROJECTS = [
    ("kube-bmc", "Server BMCs as Kubernetes resources: in-band discovery without credentials, "
     "hardware health, power control, a web dashboard, a kubectl plugin and Grafana. An MCP "
     "endpoint lets AI agents inspect and operate the servers."),
    ("SAC", "Sandbox Agent Cluster: Claude Code in the browser for everyone, with an isolated "
     "Kubernetes environment per user, a skill marketplace and a shared knowledge base."),
    ("flashvsr-sm89-ops", "4K video super-resolution on a 24 GB RTX 4090: a ComfyUI FlashVSR "
     "node and a Triton/FP8 operator pack, about 1.3× faster, no CUDA build."),
    ("viggle-animate-workflow", "Viggle-Animate in one ComfyUI node, on an INT8 checkpoint with "
     "automatic attention routing."),
]

CONTRIBUTIONS = [
    ("NVIDIA", "NVIDIA NVSentinel", "Fault detection and remediation for GPU clusters", [
        ("#648", "Make the Helm chart's PodMonitor optional and configurable"),
        ("#649", "Read the systemd runtime journal for syslog monitoring"),
    ]),
    ("apache", "Apache RocketMQ Client Go", "Go client of the Apache RocketMQ messaging platform", [
        ("#923", "Give each push consumer its own rate-limit channel"),
        ("#863", "Check the context safely in the trace producer"),
        ("#886", "Fix messages not found by query"),
        ("#888", "Count client instances once"),
    ]),
    ("istio", "Istio", "Service mesh", [
        ("#39526", "Release the WaitGroup with defer in crane"),
    ]),
]

THEMES = {
    "light": dict(card="#ffffff", border="#d1d9e0", fg="#1f2328", muted="#59636e", accent="#0969da", chip="#f6f8fa"),
    "dark": dict(card="#151b23", border="#3d444d", fg="#f0f6fc", muted="#9198a1", accent="#4493f8", chip="#212830"),
}

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"


def wrap(text, size, width):
    """Breaks text into lines that fit width, estimating glyph widths."""
    per_line = int(width / (size * 0.54))
    lines, line = [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > per_line:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + [line] if line else lines


def svg(width, height, body, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" font-family="{html.escape(FONT)}">'
            f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" '
            f'fill="{t["card"]}" stroke="{t["border"]}"/>{body}</svg>\n')


def project_card(name, desc, t, height):
    lines = wrap(desc, 13.5, 352)
    body = f'<text x="24" y="40" font-size="17" font-weight="600" fill="{t["accent"]}">{html.escape(name)}</text>'
    for i, line in enumerate(lines):
        body += f'<text x="24" y="{70 + i * 21}" font-size="13.5" fill="{t["muted"]}">{html.escape(line)}</text>'
    return svg(400, height, body, t)


def contribution_card(org, name, desc, prs, t):
    avatar = base64.b64encode((HERE / f"{org}.png").read_bytes()).decode()
    height = 92 + len(prs) * 26 + 10
    # Logos sit on a white plate so that dark marks stay visible in the dark theme.
    body = (f'<rect x="23.5" y="23.5" width="41" height="41" rx="9" fill="#ffffff" stroke="{t["border"]}"/>'
            f'<clipPath id="a"><rect x="28" y="28" width="32" height="32" rx="6"/></clipPath>'
            f'<image x="28" y="28" width="32" height="32" clip-path="url(#a)" href="data:image/png;base64,{avatar}"/>'
            f'<text x="80" y="40" font-size="16" font-weight="600" fill="{t["fg"]}">{html.escape(name)}</text>'
            f'<text x="80" y="60" font-size="13" fill="{t["muted"]}">{html.escape(desc)}</text>')
    for i, (num, title) in enumerate(prs):
        y = 96 + i * 26
        w = 10 + len(num) * 7.8
        body += (f'<rect x="80" y="{y - 15}" width="{w:.0f}" height="21" rx="6" fill="{t["chip"]}"/>'
                 f'<text x="85" y="{y}" font-size="12.5" font-family="{html.escape(MONO)}" fill="{t["accent"]}">{num}</text>'
                 f'<text x="{80 + w + 10:.0f}" y="{y}" font-size="14" fill="{t["fg"]}">{html.escape(title)}</text>')
    return svg(830, height, body, t)


def main():
    height = 70 + max(len(wrap(d, 13.5, 352)) for _, d in PROJECTS) * 21 + 6
    for theme, t in THEMES.items():
        for name, desc in PROJECTS:
            (HERE / f"project-{name.lower()}-{theme}.svg").write_text(project_card(name, desc, t, height))
        for org, name, desc, prs in CONTRIBUTIONS:
            (HERE / f"contrib-{org.lower()}-{theme}.svg").write_text(contribution_card(org, name, desc, prs, t))


if __name__ == "__main__":
    main()
