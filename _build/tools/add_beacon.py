"""Insert the Cloudflare Web Analytics beacon before </body> in every site page and generator template."""
import glob, io, os
B = """<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "9b34e71be0224e769409a669b329971e"}'></script>\n"""
files = [f for f in glob.glob("*medipicker.com/**/*.html", recursive=True)]
files += ["_build/build_site.py", "_build/home_template.html", "_build/tools/gen_page.py"]
n = 0
for f in files:
    s = io.open(f, encoding="utf-8").read()
    if "cloudflareinsights" in s or "</body>" not in s:
        continue
    i = s.rfind("</body>")
    io.open(f, "w", encoding="utf-8", newline="").write(s[:i] + B + s[i:])
    n += 1
print("patched", n, "of", len(files))
