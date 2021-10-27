# WMigrate
A tool for migrating AWS Workmail Users and Groups cross region and cross accounts. It also creates user and group aliases and adds the users to correspoding groups based on the source.

### Current Limitation
- Only creates "ENABLED" Users and Groups
- The script doesn't delete old Workmail Resources


### Install Dependencies

```pip install -r requirements```

### Usage

```
python3 WMigrate.py --orgOld m-6xyz --orgNew m-9xyz --profileSource $profileSource --profileDest $profileDest --regionOld us-east-1 --regionNew us-west-2
```
- orgOld - The source's organization Id
- orgNew - The destination's organization Id
- profileSource : Name of the profile for the source aws account in $HOME/.aws/credentials
- profileDest : Name of the profile for the destination aws account in $HOME/.aws/credentials
( If cross region in same account , profileSource and profileDest will be same )

**Username and Password of new users will be in - users.txt**
**You can change the Password Length by changing the value of the PASSWORD_LENGTH variable , default is 13**

### Assumptions

- The script assumes you've set up an organization on the Destination account/region
- The profiles provided have the necessary permissions 
- The script assumes you've enabled all the users and groups that needs to be migrated
- The script assumes you're migrating across same Domain Names 

### Further Improvments 
- Progress Bar
- Cross Domain Migration
- Migration from other E-mail providers
