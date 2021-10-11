import json
import boto3
import constant

client = boto3.client('cognito-idp')

def initializeGroups(event, context):
    # print(f'PrintEvent: {event}')
    # print(event)
    print('initializeGroups')
    response = client.list_groups(
        UserPoolId=constant.USER_POOL_ID,
        Limit=10
    )

    for g in response['Groups']:
        # print(f'group: {g}')
        groupName=g['GroupName']
        try:
            response = client.get_group(
                GroupName=groupName,
                UserPoolId=constant.MIGRATED_USER_POOL_ID
            )
            print(f'- Group {groupName} does exist in new pool. ok')
        except:
            
            if 'Precedence' in g:
                print(f'- Group {groupName} does not exist in new pool.')
                response = client.create_group(
                    GroupName=groupName,
                    UserPoolId=constant.MIGRATED_USER_POOL_ID,
                    Description=g['Description'],
                    RoleArn=g['RoleArn'],
                    Precedence=g['Precedence']
                )
                print(f'- Group {groupName} created. Response: {response}')
            else:
                print(f'- Group {groupName} skipped (no precedence)')
    return event;

def addUserToGroups(event, context):
    userName = event['userName']
    try:
        response = client.admin_list_groups_for_user(
            Username=userName,
            UserPoolId=constant.USER_POOL_ID,
            Limit=10
        )
        print(f'- admin_list_groups_for_user response: {response}')
        for g in response['Groups']:
            # print(f'group: {g}')
            groupName=g['GroupName']

            print(f'- add user {userName} to group {groupName}')
            response = client.admin_add_user_to_group(
                UserPoolId=constant.MIGRATED_USER_POOL_ID,
                Username=userName,
                GroupName=groupName
            )
            print(f'- admin_add_user_to_group response: {response}')

    except:
        print(f'- User not found in old pool (could be a new user). Continued')

    return (event)
