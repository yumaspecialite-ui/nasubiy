"""スタイル別の台本構成テンプレート"""

from dataclasses import dataclass


@dataclass
class SectionTemplate:
    """セクションのテンプレート"""

    name: str
    ratio: float  # 全体に対する時間の割合
    prompt: str  # ユーザーへのガイド文
    visual_hint: str  # 映像のヒント


@dataclass
class StructureTemplate:
    """台本構成テンプレート"""

    style: str
    description: str
    hook_ratio: float
    sections: list[SectionTemplate]
    cta_ratio: float


STRUCTURE_TEMPLATES: dict[str, StructureTemplate] = {
    "tips": StructureTemplate(
        style="tips",
        description="視聴者に役立つ情報をテンポよく伝える構成",
        hook_ratio=0.15,
        sections=[
            SectionTemplate(
                name="問題提起",
                ratio=0.15,
                prompt="視聴者が抱えている悩み・課題を提示してください",
                visual_hint="テキスト表示 or 問いかけの表情",
            ),
            SectionTemplate(
                name="ポイント解説",
                ratio=0.50,
                prompt="メインのノウハウ・Tipsを具体的に説明してください",
                visual_hint="ステップごとの映像 or テロップでポイント表示",
            ),
            SectionTemplate(
                name="まとめ",
                ratio=0.10,
                prompt="要点を短くまとめてください",
                visual_hint="まとめテロップ",
            ),
        ],
        cta_ratio=0.10,
    ),
    "story": StructureTemplate(
        style="story",
        description="体験談やストーリーで共感を呼ぶ構成",
        hook_ratio=0.15,
        sections=[
            SectionTemplate(
                name="背景・きっかけ",
                ratio=0.20,
                prompt="ストーリーの背景やきっかけを説明してください",
                visual_hint="過去の写真・映像 or ナレーション",
            ),
            SectionTemplate(
                name="展開・転機",
                ratio=0.35,
                prompt="何が起きたか、転機となった出来事を語ってください",
                visual_hint="臨場感のある映像 or 表情のクローズアップ",
            ),
            SectionTemplate(
                name="結果・学び",
                ratio=0.20,
                prompt="結果どうなったか、何を学んだかを伝えてください",
                visual_hint="ビフォーアフター or 感情の表現",
            ),
        ],
        cta_ratio=0.10,
    ),
    "ranking": StructureTemplate(
        style="ranking",
        description="ランキング形式でテンポよく紹介する構成",
        hook_ratio=0.10,
        sections=[
            SectionTemplate(
                name="第3位",
                ratio=0.25,
                prompt="3位のアイテム・ポイントを紹介してください",
                visual_hint="商品映像 + ランキング表示",
            ),
            SectionTemplate(
                name="第2位",
                ratio=0.25,
                prompt="2位のアイテム・ポイントを紹介してください",
                visual_hint="商品映像 + ランキング表示",
            ),
            SectionTemplate(
                name="第1位",
                ratio=0.30,
                prompt="1位のアイテム・ポイントを紹介してください（最も詳しく）",
                visual_hint="商品映像 + 1位演出 + テロップ",
            ),
        ],
        cta_ratio=0.10,
    ),
    "before_after": StructureTemplate(
        style="before_after",
        description="変化の過程を見せて驚きを与える構成",
        hook_ratio=0.10,
        sections=[
            SectionTemplate(
                name="ビフォー（変化前）",
                ratio=0.20,
                prompt="変化する前の状態を説明してください",
                visual_hint="ビフォーの映像・写真",
            ),
            SectionTemplate(
                name="プロセス（やったこと）",
                ratio=0.35,
                prompt="何をしたか、変化のプロセスを説明してください",
                visual_hint="過程のタイムラプス or ステップ映像",
            ),
            SectionTemplate(
                name="アフター（変化後）",
                ratio=0.25,
                prompt="変化後の状態を見せ、感想を述べてください",
                visual_hint="アフターの映像 + リアクション",
            ),
        ],
        cta_ratio=0.10,
    ),
    "tutorial": StructureTemplate(
        style="tutorial",
        description="手順を分かりやすく説明する構成",
        hook_ratio=0.10,
        sections=[
            SectionTemplate(
                name="準備・必要なもの",
                ratio=0.15,
                prompt="必要なものや前提条件を説明してください",
                visual_hint="材料・道具の一覧表示",
            ),
            SectionTemplate(
                name="ステップ解説",
                ratio=0.50,
                prompt="手順をステップごとに説明してください",
                visual_hint="手元のクローズアップ + 手順テロップ",
            ),
            SectionTemplate(
                name="完成・ポイント",
                ratio=0.15,
                prompt="完成形を見せ、成功のポイントを伝えてください",
                visual_hint="完成品の映像 + ポイントテロップ",
            ),
        ],
        cta_ratio=0.10,
    ),
    "vlog": StructureTemplate(
        style="vlog",
        description="日常の一場面を切り取るナチュラルな構成",
        hook_ratio=0.10,
        sections=[
            SectionTemplate(
                name="導入（場面設定）",
                ratio=0.15,
                prompt="今日の場面・シチュエーションを紹介してください",
                visual_hint="場所の全体映像 or 朝の映像",
            ),
            SectionTemplate(
                name="メインシーン",
                ratio=0.45,
                prompt="メインの活動・出来事を見せてください",
                visual_hint="自然体の映像、複数カット",
            ),
            SectionTemplate(
                name="感想・締め",
                ratio=0.20,
                prompt="感想やその日の気づきを語ってください",
                visual_hint="カメラに向かってトーク or テロップ",
            ),
        ],
        cta_ratio=0.10,
    ),
}
