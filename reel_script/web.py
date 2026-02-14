"""Webアプリケーション"""

import os

from flask import Flask, render_template, request

from .formatter import format_markdown, format_text
from .generator import generate_script
from .models import ReelDuration, ReelStyle

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates_html"),
)


@app.route("/", methods=["GET"])
def index():
    """入力フォーム"""
    styles = [(s.value, s.label) for s in ReelStyle]
    durations = [(d.value, d.label) for d in ReelDuration]
    return render_template("index.html", styles=styles, durations=durations)


@app.route("/generate", methods=["POST"])
def generate():
    """台本を生成して結果を表示"""
    topic = request.form.get("topic", "").strip()
    style_value = request.form.get("style", "tips")
    duration_value = int(request.form.get("duration", 30))
    target = request.form.get("target", "").strip() or "指定なし"
    custom_hook = request.form.get("hook", "").strip()

    if not topic:
        styles = [(s.value, s.label) for s in ReelStyle]
        durations = [(d.value, d.label) for d in ReelDuration]
        return render_template(
            "index.html",
            styles=styles,
            durations=durations,
            error="トピックを入力してください",
        )

    style = ReelStyle(style_value)
    duration = ReelDuration(duration_value)

    script = generate_script(
        topic=topic,
        style=style,
        duration=duration,
        target_audience=target,
        custom_hook=custom_hook,
    )

    text_output = format_text(script)
    md_output = format_markdown(script)

    return render_template(
        "result.html",
        script=script,
        text_output=text_output,
        md_output=md_output,
    )


def run():
    """Webサーバーを起動"""
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    run()
