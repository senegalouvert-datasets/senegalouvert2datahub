import json
import urllib
import ckanclient
from  ckanclient import datastore
base  = "https://raw.github.com/senegalouvert/data/master/%s/%s"
cc = ckanclient.CkanClient(
  base_location="http://datahub.io/api",
  api_key="xx",
  http_user = "xx",
  http_pass = "xx")
def run():
  datapackages =json.load(urllib.urlopen(
    "https://raw.github.com/senegalouvert/registry/master/datapackage-index.json")
  )
  print len(datapackages)
  for key, values in datapackages.items():
      pkg = {}
      pkg["name"] = "acces_internet_au_senegal"
      for value in values:
        
        if "resources" == value:
            resources  = values['resources']
            if len(resources):
               resource =resources[0]
               if "path" in resource:
                  resource_url  = base % (key, resource["path"])
                  pkg["resources"]   = [{
                     "format"  : "application/vnd.ms-excel",
                     "mimetype": "application/vnd.ms-excel", 
                     "url"     : resource_url
                  }
                  ]
                  pkg["download_url"]= resource_url
                  
        if "readme" == value:
           pkg["download_url"] = values['readme']
        
        pkg["tags"] =  [
          "ANSD",
          key,
          "donnees",
          "senegal",
          "publications"
          ]
        pkg["groups"]=['country-sn']

      print "cc" , cc
      try:
          pkg_old = cc.package_entity_get(pkg)
          cc.package_entity_put(pkg)
      except:
          cc.package_register_post(pkg)
      print cc.last_status, cc.last_message      
      break

if __name__ == "__main__":
  run()
  

