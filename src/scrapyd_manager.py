import os
import subprocess
import time
from scrapyd_api import ScrapydAPI

# check if scrapyd running

def wait_for_true(self,timeout, interval=0.5):
    def the_real_decorator(function):
        def wrapper(*args, **kwargs):
            timeleft = timeout
            while timeleft > 0:
                try:
                    value=function(self, *args,**kwargs)
                    if value == True:
                        return True
                except:
                    pass
                timeleft = timeleft - interval
                time.sleep(interval)
            return False
        return wrapper
    return the_real_decorator


class ScrapydManager:
    def __init__(self):
        self.project = "morningstar"
        self.spider = "funds1"
        self.scrapyd = ScrapydAPI("http://localhost:6800")


    def is_running(self):
        try:
            projects = self.scrapyd.list_projects()
            return True
        except:
            return False

    def is_project_deployed(self, project=self.project):
        projects = self.scrapyd.list_projects()
        if project in projects:
            return True
        else:
            return False


    def start_service(self):
        # Start only if service not already running
        if self.is_running():
            return True
        else:
            server_process = subprocess.Popen(["scrapyd"], cwd=f"{os.getcwd()}/src/morningstar")
            time.sleep(0.5)
            result = self.is_running()
        return result

    def deploy_default(self):
        # Deploy only if service not already running
        if not self.is_running():
            return False
        else:
            deploy_process = subprocess.Popen(["scrapyd-deploy default"], cwd=f"{os.getcwd()}/src")
            time.sleep(0.5)
            result = self.is_project_deployed(project)
        return result

    #@wait_for_true(self, timeout=1, interval=0.2)
    #def wait_for_service(self):
     #   self.is_running()


if __name__ == "__main__":
    scrapyd = ScrapydManager()
    result = scrapyd.start_service()
    result = scrapyd.deploy_default()
