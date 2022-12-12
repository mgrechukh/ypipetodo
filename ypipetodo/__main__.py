from emby import EmbyConnector
from downloader import YtdlpConnector
from todoist import TaskSourceTodoist

import configargparse
import time
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    p = configargparse.ArgParser()

    p.add('-c', '--config', is_config_file=True, help='config file path')

    p.add("--datadir", required=True)
    p.add("--resolution", default=720, type=int,
          help="max resolution in pixels to download (usually it is 720/480/360/240/...)")

    p.add("--project-id", required=True, help="Project ID in todoist")
    p.add("--todoist-token", required=True, help="Api token for Todoist")

    p.add("--emby-url", default="http://127.0.0.1:8096")
    p.add("--emby-token", required=False)
    p.add("--emby-folder", required=False,
          help="parent_id of the datadir in Emby")

    p.add("-s", "--sleep", default="30", type=int,
          help="delay in seconds between queue scan iterations")
    p.add("--oneshot", action="store_true", default=False,
          help="break loop after tasks completed")

    args = p.parse_args()

    queue = TaskSourceTodoist(args.todoist_token, args.project_id)
    worker = YtdlpConnector(args.datadir, args.resolution)
    emby = EmbyConnector(args.emby_url, args.emby_token, args.emby_folder)

    while 1:
        for task in queue.get_current_tasks():
            def _progress(message):
                logging.debug(message)
                queue.progress(task.refid, message)

            if worker.yt(task.urls, task.folder, progress = _progress):
                queue.success(task.refid)
                emby.refresh()
            else:
                queue.failed(task.refid)

        logging.info("-- iteration completed")
        if args.oneshot:
            break
        else:
            time.sleep(args.sleep)
