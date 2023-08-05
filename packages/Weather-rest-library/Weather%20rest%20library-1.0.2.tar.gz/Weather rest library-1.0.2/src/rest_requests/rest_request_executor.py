
import requests
class RequestExecutor():

    def execute_query(self,url,headers,querystring):
        return requests.request("GET", url, headers=headers, params=querystring)

if __name__ == "__main__":
    r=RequestExecutor()
    print(r.execute_query().text)
