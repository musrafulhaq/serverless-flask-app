## User management

## Software
1. Install node version (v12.22.12) and npm version (6.14.16)
2. Install python version (3.8.10)
3. Install serverless `npm install -g serverless`
    > serverless --version
    ```
    Framework Core: 3.18.2
    Plugin: 6.2.2
    SDK: 4.3.2
    ```
4. Install virtualenv package `apt install python3-virtualenv`
5. Create and activate virtual environment
    ```bash
    virtualenv venv --python=python3
    source /venv/bin/activate
    ```

6. Install dependencies `pip install -r requirements.txt`
7. Install boto3 package ```pip install boto3==1.23.8```
8. Run serverless locally
    ```bash
    sls wsgi serve
    ```
9. Install and configure AWS cli ```aws configure```
10. Deploy serverless
    ```
    sls deploy
    ```