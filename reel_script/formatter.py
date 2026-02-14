"""台本の出力フォーマッター"""

import json
from datetime import datetime

from .models import ReelScript


def format_text(script: ReelScript) -> str:
    """台本をテキスト形式で出力"""
    lines: list[str] = []
    sep = "=" * 50

    lines.append(sep)
    lines.append(f"  {script.title}")
    lines.append(sep)
    lines.append("")
    lines.append(f"トピック:       {script.topic}")
    lines.append(f"スタイル:       {script.style.label}")
    lines.append(f"動画の長さ:     {script.duration.label}")
    lines.append(f"ターゲット:     {script.target_audience}")
    lines.append(f"合計時間:       約{script.total_duration}秒")
    lines.append(f"BGM:            {script.bgm_note}")
    lines.append("")
    lines.append("-" * 50)
    lines.append("  台本")
    lines.append("-" * 50)

    for i, section in enumerate(script.all_sections, 1):
        lines.append("")
        lines.append(f"[{i}] {section.name}（{section.duration_sec}秒）")
        lines.append(f"    セリフ: {section.content}")
        if section.caption:
            lines.append(f"    テロップ: {section.caption}")
        if section.visual_note:
            lines.append(f"    映像メモ: {section.visual_note}")

    lines.append("")
    lines.append("-" * 50)
    lines.append("  ハッシュタグ")
    lines.append("-" * 50)
    lines.append("")
    lines.append(" ".join(script.hashtags))

    lines.append("")
    lines.append(sep)
    lines.append(f"  生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(sep)
    lines.append("")

    return "\n".join(lines)


def format_json(script: ReelScript) -> str:
    """台本をJSON形式で出力"""
    data = {
        "title": script.title,
        "topic": script.topic,
        "style": script.style.label,
        "duration_sec": script.duration.value,
        "target_audience": script.target_audience,
        "total_duration_sec": script.total_duration,
        "bgm_note": script.bgm_note,
        "sections": [
            {
                "number": i,
                "name": s.name,
                "duration_sec": s.duration_sec,
                "content": s.content,
                "caption": s.caption,
                "visual_note": s.visual_note,
            }
            for i, s in enumerate(script.all_sections, 1)
        ],
        "hashtags": script.hashtags,
        "generated_at": datetime.now().isoformat(),
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def format_markdown(script: ReelScript) -> str:
    """台本をMarkdown形式で出力"""
    lines: list[str] = []

    lines.append(f"# {script.title}")
    lines.append("")
    lines.append(f"| 項目 | 内容 |")
    lines.append(f"|------|------|")
    lines.append(f"| トピック | {script.topic} |")
    lines.append(f"| スタイル | {script.style.label} |")
    lines.append(f"| 動画の長さ | {script.duration.label} |")
    lines.append(f"| ターゲット | {script.target_audience} |")
    lines.append(f"| 合計時間 | 約{script.total_duration}秒 |")
    lines.append(f"| BGM | {script.bgm_note} |")
    lines.append("")
    lines.append("## 台本")
    lines.append("")

    for i, section in enumerate(script.all_sections, 1):
        lines.append(f"### [{i}] {section.name}（{section.duration_sec}秒）")
        lines.append("")
        lines.append(f"**セリフ:** {section.content}")
        lines.append("")
        if section.caption:
            lines.append(f"**テロップ:** {section.caption}")
            lines.append("")
        if section.visual_note:
            lines.append(f"**映像メモ:** {section.visual_note}")
            lines.append("")

    lines.append("## ハッシュタグ")
    lines.append("")
    lines.append(" ".join(script.hashtags))
    lines.append("")

    return "\n".join(lines)
