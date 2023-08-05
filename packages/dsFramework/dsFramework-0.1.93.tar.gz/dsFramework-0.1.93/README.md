# ds-framework
data science framework

#how to install
pip install dsframework

#how to use
##list of commands:
* dsf-cli - to get all cli options


* dsf-cli generate project my-new-project - to generate new project named my-new-project

## inside generated project folder 
(cd my-new-folder)
* dsf-cli g forcer my-new-forcer - creating new forcer (will be automatically injected to pipeline after last exist forcer)


* dsf-cli g predictable my-new-predictable - creating new predictable (will be automatically injected to pipeline after last exist predictable)


* dsf-cli run-server - will run local server with port 8080\
  available endpoints depend on project\
  http://localhost:8080/parse, http://localhost:8080/predict \
  will validate input based on input scheme and execute pipeline\
  http://localhost:8080/test \
  will run mock test using Data science portal


* dsf-cli create-deploy-files - deploy files generated automatically when creating new project this is an option to create all non exist deploy files, 

  * if deploy file was deleted by mistake you can recreate it 

  * if dsframework version was update with updated deploy files you can delete deploy files and recreate them

* dsf-cli create-cloud-eval-files - cloud eval files this is an option to create all non exist cloud eval files
