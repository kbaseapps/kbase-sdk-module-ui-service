# Development

## Prerequisites

-   Java 8
-   NodeJS 11
-   NPM 6 or higher
-   Docker

> Note: these instructions were validated the the above versions; it is possible that other versions work as well.

## Install the SDK

You must install the KBase SDK on your local machine in order to conduct testing and development.

For this document, we'll assume that you have installed the KBase SDK in a sister directory to this one.

```
cd ..
git clone https://github.com/kbase/kb_sdk
```

You will need to compile the SDK in order to use it.

```
cd kb_sdk
make
```

Now, in order to use the KBase SDK from the command line to work with the `ui-service` repo, you need to add the `kb-sdk` executable to your shell's execution path.

```
cd ../kbase-ui-module-ui-service
export PATH=`pwd`/kb_sdk/bin:$PATH
```

## install mongo image

These instructions are for macOS. Your mileage, may vary.

Assuming you are using Docker Desktop, open Kitematic from the Docker menu.

The `ui-service` dynamic service utilize the mongo document database for persistence. In order for `ui-service` to operate, therefore, a mongo instance must be available and the test configuration appropriate modified.

First, let's get the mongo instance running.

(1) Use Kitematic to get the version in the 3 series closest to the KBase deployments. Currently KBase is at 3.4, and the closest Mongo image is 3.6.

In Kitematic, search for mongo.

Using the official distribution, click the ellipsis menu at the bottom and of the repository card. Click the "SELECTED TAG", which by default reads "latest". KBase is using mongo 3, and in fact mongo 3.4, but for testing purpose the available 3.x distribution should be fine.

> E.g. at this moment, I'm using the 3.6 tag.

There is more to configure, but we'll leave that for a moment.

(2) Change image settings:

**Settings > General**

Add the environment variables:

| KEY                        | VALUE    |
| -------------------------- | -------- |
| MONGO_INITDB_ROOT_USERNAME | dev_root |
| MONGO_INITDB_ROOT_PASSWORD | dev_r00t |
|                            |          |

Click the `SAVE` button.

**Settings > Volumes**

For each DOCKER FOLDER set the LOCAL FOLDER

| DOCKER FOLDER  | LOCAL FOLDER          |
| -------------- | --------------------- |
| /data/db       | SPRINT/mongo/db       |
| /data/configdb | SPRINT/mongo/configdb |
|                |                       |

> where SPRINT is your sprint or working directory

**Settings > Network**

Enable the `kbase-dev` network if it is available, then click the `SAVE` button.

> If the `kbase-dev` network is not available, you should start the kbase-ui development image first in order to establish the kbase-dev network, or simply issue `docker network create kbase-dev`.

(3) Stop the container, then clear the database directories

    rm -rf SPRINT/mongo/*

then start the container.

This is required because the root user image settings only take effect when the container is first created, and it is automatically created when you add the image through Kitematic.

(4) Add ui_service user and database

now log in from the command line (host) as the root user

```
mongo --host localhost --port PORT --username dev_root --password dev_r00t admin
```

> Where PORT is the port assigned to mongo by Docker. See **PUBLISHED IP:PORT** in the **Settings > Hostname/Ports** tab.

> If you don't have mongo installed locally, use your favorite method for doing this. E.g. `sudo port install mongodb` to install with macports (my favorite).

Now create a user with read/write permissions

```
> use ui_service
> db.createUser({user: "ui_service", pwd: "ui_service", passwordDigestor: "server", roles: [{role: "readWrite", db: "ui_service"}]})
```

These settings will match the defaults for the UIService development configuration used in `scripts/run-docker-image-dev.sh`

Finally, exit the mongo client with `Ctrl D`.

## initialize test directory

After cloning, you should perform a basic sanity test by running the test suite:

```
kb-sdk test
```

the first test will emit the message

```
WARNING! 'kbase_endpoint' property was not found in <module>/test_local/test.cfg so validation is done against NMS in appdev

Validating module in (/Users/erikpearson/work/kbase/sprints/2019Q1S2/kbase-sdk-module-ui-service)


Congrats- this module is valid.

Set KBase account credentials in test_local/test.cfg and then test again
```

Regardless of these strange error messages, this is quite normal. The first time running `kb-sdk test` a test directory is created in `test_local`. It contains, amongst other things, a test configuration file which has not yet been populated. (Thus the error message above.)

## set up test configuration

To get tests working we need to populate the test configuration file `test_local/test.cfg`.

### Token

The tests can run against any KBase deployment environment, but these instructions will focus on CI only.

The `test_token` property in the configuration file should be set to a currently valid KBase login token. The easiest way to obtain one is to use a browser to log into https://ci.kbase.us, and then:

-   open your browser's javascript console
-   in the Javcascript command line, enter `document.cookie`.
-   you should see a line line `kbase_session=XXX`. The `XXX` is your KBase login token.
-   copy this token
-   paste into test.cfg so that the line

```
test_token=
```

becomes

```
test_token=XXX
```

### Endpoint

Set the urls to reflect that we are operating against CI;

The lines

```
kbase_endpoint=https://appdev.kbase.us/services
auth_service_url=https://appdev.kbase.us/services/auth/api/legacy/KBase/Sessions/Login

```

should become

```
kbase_endpoint=https://ci.kbase.us/services
auth_service_url=https://ci.kbase.us/services/auth/api/legacy/KBase/Sessions/Login

```

> If you are testing against different deployment environments, you will want to change both the token and the kbase endpoint to be accommodate that environment.

### Rest of the settings

At the bottom of the file, add these properties to `test.cfg`:

```
secure.mongo_db=ui_service
secure.mongo_host=mongo
secure.mongo_port=27017
secure.mongo_user=ui_service
secure.mongo_pwd=ui_service
secure.admin_users=USERNAME
```

where

`USERNAME` is either your username, or some username you wish to use for the admin functions test

> TODO: clarify this!!!

## Run the Tests

Now you are ready to run the tests.

```
kb-sdk test
```

## FIN

You are now ready to hack on UIService and use it directly from kbase-ui using the dynamic-services option.

E.g.

```
make dev-start dynamic-services="UIService"
```
