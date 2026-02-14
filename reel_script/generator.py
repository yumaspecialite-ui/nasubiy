"""台本生成ロジック"""

import random

from .models import ReelDuration, ReelScript, ReelStyle, ScriptSection
from .templates.hooks import HOOK_TEMPLATES
from .templates.structures import STRUCTURE_TEMPLATES


def pick_hook_text(style: ReelStyle, topic: str) -> str:
    """スタイルに合ったフックテキストをランダムに選択"""
    templates = HOOK_TEMPLATES.get(style.value, HOOK_TEMPLATES["tips"])
    template = random.choice(templates)
    return template.format(topic=topic)


def generate_script(
    topic: str,
    style: ReelStyle,
    duration: ReelDuration,
    target_audience: str = "",
    custom_hook: str = "",
) -> ReelScript:
    """台本を生成する

    Args:
        topic: リールのトピック・テーマ
        style: リールのスタイル
        duration: リールの長さ
        target_audience: ターゲット層
        custom_hook: カスタムフック（空の場合はテンプレートから生成）
    """
    structure = STRUCTURE_TEMPLATES[style.value]
    total_sec = duration.value

    # フック
    hook_sec = max(2, int(total_sec * structure.hook_ratio))
    hook_text = custom_hook if custom_hook else pick_hook_text(style, topic)
    hook = ScriptSection(
        name="フック（つかみ）",
        duration_sec=hook_sec,
        content=hook_text,
        visual_note="視聴者の手を止める演出。テロップ大きめ。",
        caption=hook_text,
    )

    # メインセクション
    sections: list[ScriptSection] = []
    for tmpl in structure.sections:
        sec_duration = max(2, int(total_sec * tmpl.ratio))
        sections.append(
            ScriptSection(
                name=tmpl.name,
                duration_sec=sec_duration,
                content=f"【{tmpl.prompt}】",
                visual_note=tmpl.visual_hint,
                caption="",
            )
        )

    # CTA
    cta_sec = max(2, int(total_sec * structure.cta_ratio))
    cta = ScriptSection(
        name="CTA（行動喚起）",
        duration_sec=cta_sec,
        content="いいね・保存・フォローよろしくお願いします！",
        visual_note="フォローボタンのアニメーション or テロップ",
        caption="フォローで最新情報をチェック！",
    )

    # ハッシュタグ提案
    hashtags = _suggest_hashtags(topic, style)

    script = ReelScript(
        title=f"{topic}｜{style.label}リール台本",
        topic=topic,
        style=style,
        duration=duration,
        target_audience=target_audience or "指定なし",
        hook=hook,
        sections=sections,
        cta=cta,
        hashtags=hashtags,
        bgm_note=_suggest_bgm(style),
    )
    return script


def _suggest_hashtags(topic: str, style: ReelStyle) -> list[str]:
    """ハッシュタグを提案"""
    base_tags = ["#リール", "#reels", "#インスタ", "#instagram"]
    style_tags = {
        "tips": ["#豆知識", "#ライフハック", "#裏ワザ"],
        "story": ["#体験談", "#ストーリー", "#エピソード"],
        "ranking": ["#ランキング", "#おすすめ", "#ベスト3"],
        "before_after": ["#ビフォーアフター", "#beforeafter", "#変化"],
        "tutorial": ["#やり方", "#howto", "#チュートリアル"],
        "vlog": ["#vlog", "#日常", "#ルーティン"],
    }
    topic_tag = f"#{topic.replace(' ', '')}"
    return [topic_tag] + style_tags.get(style.value, []) + base_tags


def _suggest_bgm(style: ReelStyle) -> str:
    """BGMの雰囲気を提案"""
    suggestions = {
        "tips": "テンポの良いポップ系BGM（120BPM前後）",
        "story": "エモーショナルなピアノ or アコースティック系",
        "ranking": "ワクワク感のあるアップテンポBGM",
        "before_after": "ドラマチックな展開のある楽曲（静→動）",
        "tutorial": "落ち着いたローファイ系BGM",
        "vlog": "おしゃれなカフェ系BGM or ローファイ",
    }
    return suggestions.get(style.value, "トレンドのBGMを使用")
