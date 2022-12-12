import os
import subprocess
import sys
import shlex


class YtdlpConnector:
    def __init__(self, basedir, default_resolution):
        self._basedir = os.path.abspath(basedir)
        self._default_resolution = default_resolution

    def yt(self, video_urls, folder, progress=print, **params):
        target_path = os.path.join(self._basedir, folder)
        tmp_path = os.path.join(target_path, '.tmp')
        tmp_mark = os.path.join(tmp_path, '.ignore')
        if not os.path.isfile(tmp_mark):
            os.makedirs(tmp_path)
            with open(tmp_mark, "w") as f:
                pass

        params.setdefault('resolution', self._default_resolution)
        video_format = f'bestvideo[height<={params["resolution"]}][ext=mp4]+bestaudio[ext=m4a]/best[height<={params["resolution"]}]'

        command = ["yt-dlp", "--no-warnings", "--recode", "mp4", "--no-progress", "-P",
                   target_path, "-P", f"temp:{tmp_path}", "-f", video_format] + video_urls[:1]
        print("starting download:", " ".join(
            [shlex.quote(a) for a in command]))

        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as proc:
            for line in proc.stdout:
                progress(line)

            progress("exit code %s" % proc.poll())
            if proc.wait() == 0:
                return True
