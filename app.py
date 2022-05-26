import boto3
import json
from flask import Flask, jsonify, request
app = Flask(__name__)

dynamodb = boto3.client('dynamodb', region_name='ap-south-1')

iamUserInDynamodb = []

iam = boto3.client('iam')

@app.route("/")
def hello():
    return "Hello World!"


def listIamUser():
    iamUsers = []
    response = iam.list_users(
        PathPrefix='/')

    for user in response['Users']:
        print(user['UserName'], end='\n\n')
        iamUsers.append(user['UserName'])
    return iamUsers

@app.route('/addusers')
def putUserIntoDynamodb():
    retrievedIamUsers = listIamUser()
    for iamUser in retrievedIamUsers:
        response = dynamodb.put_item(
            TableName='table1',
            Item={
                'users': {
                    'S': iamUser
                }
            }
        )
    return jsonify({'Current IAM Users': retrievedIamUsers})


@app.route('/getuser')
def get_data_from_dynamodb():
    response=dynamodb.scan(TableName='table1')
    for item in response['Items']:
        print(item['users']['S'])
        iamUserInDynamodb.append(item['users']['S'])

    print(json.dumps({"users": iamUserInDynamodb}))
    return jsonify({"users_in_db": iamUserInDynamodb})


@app.route('/showdetails/<string:user_id>', methods=['GET'])
def show_single_details_from_dynamodb(user_id):
    
    response = iam.get_user(
        UserName=user_id
    )
    return jsonify({
        'userArn': response['User']['Arn']
    })


@app.route('/resetuserlist')
def deleteUserFromDynamodb():
    deletedUsers = []
    userList = dynamodb.scan(TableName='table1')
    for userDict in userList['Items']:
        print(userDict)

        res = dynamodb.delete_item(
            TableName='table1',
            Key=userDict
        )
        deletedUsers.append(userDict['users']['S'])
    currentIamUserList = putUserIntoDynamodb()
    return currentIamUserList



@app.route('/createiamuser', methods=["POST"])
def create_user():
    IamUserName = request.json.get('iamusername')
    create_iam_user = iam.create_user(
        UserName=IamUserName
    )
    return jsonify({"iam user arn": create_iam_user['User']['Arn']})
