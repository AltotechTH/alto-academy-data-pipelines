# alto-academy-data-pipelines
This repository is for all the collections of data pipelines that are going to be deployed in Mage.

### Steps to deploy Mage.ai
- Set up environment variable.
  - Create ```.env``` file in ```alto-academy-data-pipelines``` and paste the following two lines in it. (**Not secure. You have to change this behavior in production.**)
    - ```ENV=dev```
    - ```PROJECT_NAME=alto_academy_workshop```
- ```docker compose pull```
- ```docker compose build```
- ```docker compose up -d```
- After that, you can open Mage.ai UI by entering ```localhost:6789``` in your browser.
