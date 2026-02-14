"""インタラクティブCLIインターフェース"""

import argparse
import sys

from .formatter import format_json, format_markdown, format_text
from .generator import generate_script
from .models import ReelDuration, ReelStyle


def _select_option(prompt: str, options: list[tuple[str, str]]) -> str:
    """選択肢を表示してユーザーに選ばせる"""
    print(f"\n{prompt}")
    for i, (key, label) in enumerate(options, 1):
        print(f"  {i}. {label}")

    while True:
        try:
            choice = input("\n番号を入力 > ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx][0]
        except (ValueError, EOFError):
            pass
        print("正しい番号を入力してください")


def _input_text(prompt: str, default: str = "") -> str:
    """テキスト入力を受け付ける"""
    suffix = f"（デフォルト: {default}）" if default else ""
    try:
        value = input(f"\n{prompt}{suffix}\n> ").strip()
    except EOFError:
        value = ""
    return value if value else default


def interactive_mode() -> None:
    """対話モードで台本を作成"""
    print()
    print("=" * 50)
    print("  Instagram リール台本メーカー")
    print("=" * 50)

    # トピック入力
    topic = _input_text("リールのトピック・テーマを入力してください")
    if not topic:
        print("トピックが入力されませんでした。終了します。")
        sys.exit(1)

    # スタイル選択
    style_options = [(s.value, s.label) for s in ReelStyle]
    style_key = _select_option("リールのスタイルを選んでください:", style_options)
    style = ReelStyle(style_key)

    # 長さ選択
    duration_options = [(str(d.value), d.label) for d in ReelDuration]
    duration_key = _select_option("動画の長さを選んでください:", duration_options)
    duration = ReelDuration(int(duration_key))

    # ターゲット
    target = _input_text("ターゲット層を入力してください", "指定なし")

    # カスタムフック
    custom_hook = _input_text(
        "フック（冒頭のつかみ）を自分で書きますか？（空欄で自動生成）"
    )

    # 出力フォーマット
    format_options = [
        ("text", "テキスト"),
        ("markdown", "Markdown"),
        ("json", "JSON"),
    ]
    fmt = _select_option("出力フォーマットを選んでください:", format_options)

    # 生成
    print("\n台本を生成中...\n")
    script = generate_script(
        topic=topic,
        style=style,
        duration=duration,
        target_audience=target,
        custom_hook=custom_hook,
    )

    # 出力
    formatters = {
        "text": format_text,
        "markdown": format_markdown,
        "json": format_json,
    }
    output = formatters[fmt](script)
    print(output)

    # ファイル保存の確認
    save_path = _input_text("ファイルに保存しますか？パスを入力（空欄でスキップ）")
    if save_path:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\n保存しました: {save_path}")


def cli_mode(args: argparse.Namespace) -> None:
    """コマンドライン引数モードで台本を作成"""
    style = ReelStyle(args.style)
    duration = ReelDuration(args.duration)

    script = generate_script(
        topic=args.topic,
        style=style,
        duration=duration,
        target_audience=args.target or "指定なし",
        custom_hook=args.hook or "",
    )

    formatters = {
        "text": format_text,
        "markdown": format_markdown,
        "json": format_json,
    }
    output = formatters[args.format](script)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"保存しました: {args.output}")
    else:
        print(output)


def main() -> None:
    """エントリーポイント"""
    parser = argparse.ArgumentParser(
        description="Instagram リール動画の台本作成ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 対話モード
  reel-script

  # コマンドライン引数モード
  reel-script --topic "朝のルーティン" --style vlog --duration 30
  reel-script --topic "Python入門" --style tutorial --duration 60 --format markdown -o script.md
        """,
    )
    parser.add_argument("--topic", "-t", help="リールのトピック・テーマ")
    parser.add_argument(
        "--style",
        "-s",
        choices=[s.value for s in ReelStyle],
        help="リールのスタイル",
    )
    parser.add_argument(
        "--duration",
        "-d",
        type=int,
        choices=[d.value for d in ReelDuration],
        help="動画の長さ（秒）",
    )
    parser.add_argument("--target", help="ターゲット層")
    parser.add_argument("--hook", help="カスタムフック（冒頭のつかみ）")
    parser.add_argument(
        "--format",
        "-f",
        choices=["text", "markdown", "json"],
        default="text",
        help="出力フォーマット（デフォルト: text）",
    )
    parser.add_argument("--output", "-o", help="出力ファイルパス")

    args = parser.parse_args()

    # 必須引数が揃っていれば CLI モード、なければ対話モード
    if args.topic and args.style and args.duration:
        cli_mode(args)
    else:
        interactive_mode()
