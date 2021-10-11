import json
import boto3
import constant

client = boto3.client('cognito-idp')

def migrateUser(event, context):
    print(f'migrateUser flow')
    
    user = client.admin_initiate_auth(
        UserPoolId=constant.USER_POOL_ID,
        ClientId=constant.CLIENT_ID,
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            'USERNAME': event['userName'],
            'PASSWORD': event['request']['password']
        }
    )
    
    userName=event['userName']
    if (user):
        print(f'- migrateUser: user {userName} authenticated')
        userAttributes = client.get_user(
            AccessToken=user['AuthenticationResult']['AccessToken']
        )
        for userAttribute in userAttributes['UserAttributes']:
            if userAttribute['Name'] == 'email':
                userEmail = userAttribute['Value']
                # print(userEmail)
                event['response']['userAttributes'] = {
                    "email": userEmail,
                    "email_verified": "true"
                }
                
        event['response']['messageAction'] = "SUPPRESS"
        # If you would like users to continue to use their existing passwords, set the attribute finalUserStatus = "CONFIRMED"
        event['response']['finalUserStatus'] = "CONFIRMED"
        print (event)
        return (event)
    else:
        print(f'- migrateUser: user {userName} NOT authenticated')
        return('Bad Password')
    

def forgotPassword(event, context):
    print ("Forgot password flow")
    user = client.admin_get_user(
        UserPoolId=constant.USER_POOL_ID,
        Username=event['userName']
    )
    print(f'- Got user {user}')
    if (user):
        for userAttribute in user['UserAttributes']:
            if userAttribute['Name'] == 'email':
                userEmail = userAttribute['Value']
                # print(userEmail)
                event['response']['userAttributes'] = {
                    "email": userEmail,
                    "email_verified": "true"
                }
        event['response']['messageAction'] = "SUPPRESS"
        print(event)
        return (event)
    else:
        return('Bad Password')