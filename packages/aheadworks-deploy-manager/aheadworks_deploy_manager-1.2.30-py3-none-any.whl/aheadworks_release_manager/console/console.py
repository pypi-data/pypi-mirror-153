import os
from aheadworks_release_manager.api.release_manager import ReleaseManager
from aheadworks_core.model.data.jira import JiraConfig
import traceback


class Console:
    """
    this application needed next env variables
    JIRA_USER_EMAIL
    JIRA_TOKEN
    """

    def __init__(self):
        jira_config = JiraConfig(os.getenv('JIRA_USER_EMAIL'), os.getenv('JIRA_TOKEN'))
        self.release_manager = ReleaseManager(jira_config)

    # Release manager
    def jira_release(self, jira_project_key, composer_file, discord_bot_url, path_to_files, assign_to):
        try:
            self.release_manager.jira_release(
                jira_project_key,
                composer_file,
                discord_bot_url,
                path_to_files,
                assign_to
            )
            exit_code = 0
        except Exception as error:
            print('Error: ' + repr(error))
            exit_code = 1

        exit(exit_code)

    def build_swagger_web_api_doc(
            self,
            path_to_module,
            magento_url,
            magento_path_on_server='/var/www/html',
            ssh_port=22,
            ssh_user='root',
            ssh_pass='root'
    ):
        try:
            result = self.release_manager.build_swagger_web_api_doc(
                path_to_module,
                magento_url,
                magento_path_on_server,
                ssh_port,
                ssh_user,
                ssh_pass
            )
            print(result)
            exit_code = 0
        except Exception as error:
            print('Error: ' + repr(error))
            traceback.print_exc()
            exit_code = 1

        exit(exit_code)

    def build_ecommerce_pack(self, bitbucket_workspace, bitbucket_repo_slug):
        try:
            self.release_manager.build_ecommerce_pack(bitbucket_workspace, bitbucket_repo_slug)
            exit_code = 0
        except Exception as error:
            print('Error: ' + repr(error))
            traceback.print_exc()
            exit_code = 1

        exit(exit_code)
