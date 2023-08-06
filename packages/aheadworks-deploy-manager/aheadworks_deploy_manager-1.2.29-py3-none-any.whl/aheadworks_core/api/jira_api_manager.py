from aheadworks_core.model.http.api_request import ApiRequest as Api
from jira import JIRA
import json


class JiraApiManager:
    """api manager for jira"""

    def __init__(self, config):
        self.config = config
        self.request = Api(config=self.config)
        self.jira = JIRA(
            server=self.config.url,
            basic_auth=(self.config.user, self.config.token)
        )

    def get_jira_instance(self):
        return self.jira

    def get_issue_url(self, task_key):
        return '{}/browse/{}'.format(self.config.url, task_key)

    def get_release_report_all_issues_url(self, project_key, version_id):
        return '{}/projects/{}/versions/{}/tab/release-report-all-issues'.format(
            self.config.url,
            project_key,
            version_id
        )

    # deprecated, use get_jira_instance
    def search_tasks_jql(self, jql):
        headers = {
            "Accept": "application/json"
        }
        url = '/rest/api/3/search?jql={}'.format(jql)
        data = self.request.request(location=url, headers=headers)

        return json.loads(data)

    # deprecated, use get_jira_instance
    def add_attachments_to_task(self, task_key, files):
        headers = {
            "Accept": "application/json",
            'X-Atlassian-Token': 'nocheck'
        }
        url = '/rest/api/3/issue/{}/attachments'.format(task_key)
        data = self.request.request(location=url, headers=headers, method='POST', files=files)

        return json.loads(data)
