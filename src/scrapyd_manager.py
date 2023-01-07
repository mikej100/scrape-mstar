import os
import subprocess
import time
from scrapyd_api import ScrapydAPI

# check if scrapyd running

SHORT_WAIT = 1
MEDIUM_WAIT = 1.5

def wait_for_true(self,timeout, interval=SHORT_WAIT):
    """NOT IMPLEMENTED Decorator to wait until function retunrs complete.

    Will retry function call up to elapsed time <timeout>, repeating
    each <interval> time.

    :param timeout: Maximum time to wait in seconds
    :type timeout: Float
    :param interval: time to wait between attempts, in seconds, defaults to SHORT_WAIT
    :type interval: Float, optional
    """    
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
    """Class to manage scrapyd service, projects and jobs.

    When run as script will start the service and deploy the default project.
    """    
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

    def is_project_deployed(self, project="default"):
        if project == "default":
            project = self.project
        projects = self.scrapyd.list_projects()
        if project in projects:
            return True
        else:
            return False


    def start_service(self) -> bool:
        """Start scrapy server.

        If already running, return True quietly.

        :return: True if already running or started successfully, otherwise
        False
        :rtype: bool
        """        
        if self.is_running():
            return True
        else:
            #server_process = subprocess.Popen(["scrapyd"], cwd=f"{os.getcwd()}/src/morningstar")
            server_process = subprocess.Popen(["scrapyd"])
            time.sleep(SHORT_WAIT)
            result = self.is_running()
        return result
    
    def stop_service(self) -> bool:

        if self.is_running():
            stop_process = subprocess.Popen(["sudo", "killall", "scrapyd"])
            stop_process.wait()
            result = not self.is_running()
        else:
            result = True
        return result
        


    def deploy_default(self) -> bool:
        """Deploy default project to scrapyd service.

        If a project with the name is already deployed, return
        True quietly (does not re-deploy or overwrite).

        :return: is the project deployed? False if service not
        running or project not listed after deployment attempt.
        :rtype: bool
        """        
        if self.is_project_deployed():
            return True
        else:
            deploy_process = subprocess.Popen(["scrapyd-deploy", "default"], cwd=f"{os.getcwd()}/src")
            time.sleep(MEDIUM_WAIT)
            result = self.is_project_deployed("default")
        return result

    def delete_project(self, project="default") -> bool():
        """Delete project from server.
        
        If project not found, then returns silently with True.
        Default project is defined in the class python code.

        :param project: _description_, defaults to "default"
        :type project: str, optional
        """
        if project == "default":
            project = self.project
        if self.is_project_deployed(project):
            result = self.scrapyd.delete_project(project)
            time.sleep(SHORT_WAIT)
    #@wait_for_true(self, timeout=1, interval=0.2)
    #def wait_for_service(self):
     #   self.is_running()


    def schedule(self, symbols, crawl_id, feed_uri) -> str:
        settings = {
            "FEED_URI": feed_uri
        }
        result = self.scrapyd.schedule( 
            self.project,
            self.spider, 
            settings=settings,
            symbols=symbols
            )
        return result


if __name__ == "__main__":
    scrapyd = ScrapydManager()
    result = scrapyd.start_service()
    result = scrapyd.deploy_default()
