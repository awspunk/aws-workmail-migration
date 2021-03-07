PASSWORD_LENGTH = 13

import argparse
import boto3
import secrets

parser = argparse.ArgumentParser()


parser.add_argument("--orgOld",help="Organization ID of Old Workmail Directory")
parser.add_argument("--orgNew",help="Organization ID of New Workmail Directory")
parser.add_argument("--profileSource",help="Profile for Old Account in ($HOME/.aws/credentials)")
parser.add_argument("--profileDest",help="Profile for New Account in ($HOME/.aws/credentials)")
parser.add_argument("--regionOld",help="Old Region for Workmail")
parser.add_argument("--regionNew",help="New Region For Workmail")


args = parser.parse_args()

session_old = boto3.Session(profile_name=args.profileSource)
session_new = boto3.Session(profile_name=args.profileDest)

client_old = session_old.client('workmail',region_name=args.regionOld)
client_new = session_new.client('workmail',region_name=args.regionNew)


def passwd():

    password_length = 13

    return secrets.token_urlsafe(PASSWORD_LENGTH)



def createUsers():
    print("Creating Users.......")
    response = client_old.list_users(
            OrganizationId = args.orgOld
            )
    users = response['Users']
    for user in users:
        try:
            password = passwd()
            if ( user['UserRole'] == "USER" and user['State'] == "ENABLED"):
                createUserResponse = client_new.create_user(
                        OrganizationId = args.orgNew,
                        Name = user['Name'],
                        DisplayName = user['DisplayName'],
                        Password = password
                        )
                registerUserReponse = client_new.register_to_work_mail(
                        OrganizationId = args.orgNew,
                        EntityId = createUserResponse['UserId'],
                        Email = user['Email']
                        )
                listAliasesResponse = client_old.list_aliases(
                        OrganizationId = args.orgOld,
                        EntityId = user['Id']
                        )
                aliases = listAliasesResponse['Aliases']
                for alias in aliases:
                    client_new.create_alias(
                            OrganizationId = args.orgNew,
                            EntityId = createUserResponse['UserId'],
                            Alias = alias
                            )
                print("Created " + user['Name'])
                with open("./users.txt",'a') as f:
                    f.write(user['Name'] +  " : " + password + "\n")
        except Exception as e:
            print(e)

def createGroups():
    print("Creating Groups.......")
    response = client_old.list_groups(
            OrganizationId = args.orgOld
            )
    users = client_new.list_users(
            OrganizationId = args.orgNew
            )
    users = users['Users']
    groups = response['Groups']
    oldGroupResponse = client_old.list_group_members(
                OrganizationId = args.orgOld,
                GroupId = groups[0]['Id']
                        )
    members = oldGroupResponse['Members']
    for group in groups:
        try:
            if ( group['State'] == "ENABLED" ) :
                createGroupResponse = client_new.create_group(
                        OrganizationId = args.orgNew,
                        Name = group['Name']
                        )
                client_new.register_to_work_mail(
                        OrganizationId = args.orgNew,
                        EntityId = createGroupResponse['GroupId'],
                        Email = group['Email']
                        )
                listAliasesResponse = client_old.list_aliases(
                        OrganizationId = args.orgOld,
                        EntityId = group['Id']
                    )
                aliases = listAliasesResponse['Aliases']
                for alias in aliases:
                    client_new.create_alias(
                            OrganizationId = args.orgNew,
                            EntityId = createGroupResponse['GroupId'],
                            Alias = alias
                            )
                oldGroupResponse = client_old.list_group_members(
                OrganizationId = args.orgOld,
                GroupId = group['Id']
                        )
                members = oldGroupResponse['Members']
                
                for member in members:
                    if (member['Type'] == "USER"):
                        for user in users:
                            if ( user['Name'] == member['Name'] and user['State'] == "ENABLED"):
                                resp = client_new.associate_member_to_group(
                                    OrganizationId = args.orgNew,
                                    GroupId = createGroupResponse['GroupId'],
                                    MemberId = user['Id']
                                    )
                print("Created " + group['Name'])

        except Exception as e:
            print(e)


            

createUsers()
createGroups()

