from todoist_api_python.api import TodoistAPI
from functools import cache
import re
from task import JobItem


class TaskSourceTodoist:
    def __init__(self, api_token, project_id):
        self._api = TodoistAPI(api_token)
        self._project_id = project_id

        self._sections = {}

    @cache
    def get_section_name(self, section_id):
        return self._api.get_section(section_id).name

    def get_current_tasks(self):
        for t in self._api.get_tasks(project_id=self._project_id):
            if not t.section_id:
                continue

            section_name = self.get_section_name(t.section_id)

            comments = self._api.get_comments(task_id=t.id)
            if comments and re.match("^failed", comments[-1].content):
                print('skipping failed task', t.url)
                return

            yt_re = "(?P<url>(https://www.youtube.com/watch\?v=|https://youtu.be/)[a-zA-Z0-9-]+)"
            urls = [x.group('url') for x in re.finditer(yt_re, t.content)]
            yield JobItem(urls=urls, folder=section_name.strip(), refid=t.id)

    def progress(self, ref, message):
        self._api.add_comment(task_id=ref, content=message)

    def success(self, ref):
        self._api.add_comment(task_id=ref, content="finished successfully")
        self._api.close_task(task_id=ref)

    def failed(self, ref):
        self._api.add_comment(task_id=ref, content="failed")
