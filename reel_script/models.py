"""台本のデータモデル"""

from dataclasses import dataclass, field
from enum import Enum


class ReelDuration(Enum):
    """リール動画の長さ"""

    SHORT = 15  # 15秒
    MEDIUM = 30  # 30秒
    LONG = 60  # 60秒
    MAX = 90  # 90秒

    @property
    def label(self) -> str:
        return f"{self.value}秒"

    @property
    def char_count(self) -> int:
        """目安の文字数（日本語で1秒あたり約4〜5文字）"""
        return self.value * 4


class ReelStyle(Enum):
    """リール動画のスタイル"""

    TIPS = "tips"  # ノウハウ・Tips系
    STORY = "story"  # ストーリー・体験談系
    RANKING = "ranking"  # ランキング・まとめ系
    BEFORE_AFTER = "before_after"  # ビフォーアフター系
    TUTORIAL = "tutorial"  # チュートリアル・やり方系
    VLOG = "vlog"  # Vlog・日常系

    @property
    def label(self) -> str:
        labels = {
            "tips": "ノウハウ・Tips",
            "story": "ストーリー・体験談",
            "ranking": "ランキング・まとめ",
            "before_after": "ビフォーアフター",
            "tutorial": "チュートリアル・やり方",
            "vlog": "Vlog・日常",
        }
        return labels[self.value]


@dataclass
class ScriptSection:
    """台本のセクション"""

    name: str
    duration_sec: int
    content: str
    visual_note: str = ""  # 映像の補足メモ
    caption: str = ""  # テロップ・字幕


@dataclass
class ReelScript:
    """リール動画の台本"""

    title: str
    topic: str
    style: ReelStyle
    duration: ReelDuration
    target_audience: str
    hook: ScriptSection
    sections: list[ScriptSection] = field(default_factory=list)
    cta: ScriptSection | None = None
    hashtags: list[str] = field(default_factory=list)
    bgm_note: str = ""

    @property
    def total_duration(self) -> int:
        total = self.hook.duration_sec
        total += sum(s.duration_sec for s in self.sections)
        if self.cta:
            total += self.cta.duration_sec
        return total

    @property
    def all_sections(self) -> list[ScriptSection]:
        result = [self.hook]
        result.extend(self.sections)
        if self.cta:
            result.append(self.cta)
        return result
