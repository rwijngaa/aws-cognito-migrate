"""
    Migrate user from old Cognito pool to new Cognito pool
    New user (attributes) are returned, cognito will add the user to the pool.
    
    - UserMigration event: only called when user does not exists (in the new pool)
    - PostAuthentication: for adding the user to the groups it had in the original pool
"""
import json
import boto3
import constant
from groups import initializeGroups, addUserToGroups
from migrate import migrateUser, forgotPassword

def Handler(event, context):
    
    print(f'MigrateUser flow called {event}')
    newEvent = event
    
    if (event['triggerSource'] == 'UserMigration_Authentication'):
        # initializeGroups(event, context)
        newEvent = migrateUser(event, context)
        print(f'MigrateUser returned:  {newEvent}')
    elif (event["triggerSource"] == "UserMigration_ForgotPassword"):
        # initializeGroups(event, context)
        newEvent = forgotPassword(event, context)
        print(f'forgotPassword returned:  {newEvent}')
    elif (event['triggerSource'] == 'PostAuthentication_Authentication'):
        newEvent = addUserToGroups(event, context)
        print(f'addUserToGroups returned:  {newEvent}')
        
    return (newEvent)        
