# What is this?

Tinybird Analytics is a blazing fast analytics engine for your serverless applications.
Think of it as a set of next-generation lego pieces for building data workflows and applications which rely on real-time analytics.

## Developing tinybird.co?

### Installing the development environment

1. Compile or install ClickHouse. Current production version is 21.9.5.16:

    To help you choosing the right version of ClickHouse to install, [take a look at this section in the FAQ](#which-clickhouse-version-should-i-install)

    a. The easiest way to have multiple ClickHouse versions locally is to use pre-built binaries. Check out [https://clickhouse.com/docs/en/getting-started/install/#from-tgz-archives](https://clickhouse.com/docs/en/getting-started/install/#from-tgz-archives) and [https://clickhouse.tech/docs/en/development/build/#you-dont-have-to-build-clickhouse](https://clickhouse.tech/docs/en/development/build/#you-dont-have-to-build-clickhouse). [This is the current production version for Linux](https://repo.clickhouse.com/tgz/stable/clickhouse-common-static-21.9.5.16.tgz), while the rest can be found [in the stable dir of the tgz archive](https://repo.clickhouse.com/tgz/stable). (see FAQ: using native ClickHouse builds with macOS). You can download the `clickhouse-common-static` tgz for any stable released ClickHouse version. That contains the standalone binaries within its `usr/bin` directory. This way, you can have different portable versions of ClickHouse that you can use to test. Then, you simply set `CLICKHOUSE_BIN_FOLDER_PATH` env var as explained in the following sections to choose which version to use. e.g. of directory structure:

    ```bash
    /home/Tinybird/ch-versions
    ├── 20.7.2.30
    │   ├── clickhouse
    │   ├── clickhouse-extract-from-config -> clickhouse
    │   └── clickhouse-odbc-bridge
    ├── 21.9.5.16
    │   ├── clickhouse
    │   ├── clickhouse-extract-from-config -> clickhouse
    │   ├── clickhouse-library-bridge
    │   └── clickhouse-odbc-bridge
    ```

    b. Compiling ClickHouse yourself. You'll need 70 GB of free disk space. It is recommended to use our production version (v21.9.5.16) following its compilation docs: [https://github.com/ClickHouse/ClickHouse/blob/v21.9.5.16-stable/docs/en/development/build.md](https://github.com/ClickHouse/ClickHouse/blob/v21.9.5.16-stable/docs/en/development/build.md). The final binary is generated at `[build_dir]/programs/clickhouse`. You can use this compiled version setting the `CLICKHOUSE_BIN_FOLDER_PATH` env var accordingly.

2. Install and configure Redis

    On MacOS:

    ```bash
    brew install redis
    ```

    On Ubuntu/Debian:

    ```bash
    sudo apt install redis-server
    ```

    Install the redis-cell extension.

    On Linux:

    ```bash
    sudo cp deploy/files/redis-cell/redis-cell-v0.2.5-x86_64-unknown-linux-gnu/libredis_cell.so /var/lib/redis
    echo 'loadmodule /var/lib/redis/libredis_cell.so' | sudo tee -a /etc/redis/redis.conf
    ```

    Then modify `/etc/redis/redis.conf` and change line `supervised no` to `supervised systemd`.
    Lastly, start the service with `sudo systemctl restart redis`. You can also enable it to be automatically
    started on boot: `sudo systemctl enable redis`

3. Install Zookeeper

    ```bash
    # On Ubuntu:
    sudo apt install zookeeperd
    ```

    ```bash
    # On Mac:
    brew install zookeeper
    ```

4. Checkout this repo

5. Install Python >= 3.8.8 (any version 3.8.X >= 3.8.8 should work as well)

    **On Ubuntu**

    ```bash
    sudo apt install python3-pip libcurl4-openssl-dev libsqlite3-dev liblzma-dev libssl-dev libbz2-dev
    ```

    Install pyenv to use the recommended python version (3.8.8), following [pyenv's installation guide](https://github.com/pyenv/pyenv-installer)

    Then install python 3.8.8 and set it as the default for our analytics directory:

    ```bash
    # analytics is this cloned repo path
    cd analytics/
    CONFIGURE_OPTS=--enable-shared pyenv install 3.8.12
    pyenv local 3.8.12
    ```

    **On Mac OS 11.X**

    Install [pyenv's system dependencies](https://github.com/pyenv/pyenv/wiki#troubleshooting--faq):

    If you haven't done so, install Xcode Command Line Tools (xcode-select --install) and Homebrew. Then:

    ```bash
    brew install openssl readline sqlite3 xz zlib
    ```

    Install pyenv, following [pyenv's installation guide](https://github.com/pyenv/pyenv-installer)

    Install Python >= 3.8.8:

    ```bash
    pyenv install 3.8.12
    ```

    Set it as a global version if you want to always use this one:

    ```bash
    pyenv global 3.8.12
    ```

    **On Mac M1**

    Note that the first native version is 3.9.1

    Install Python >= 3.9.1:

    ```bash
    pyenv install 3.9.9
    ```

    Set it as a global version if you want to always use this one:

    ```bash
    pyenv global 3.9.9
    ```

6. Create your mvenv and install all dependencies:

    **A. Straightforward way:**

    ```bash
    pyenv exec python3 -m venv .e
    .e/bin/python3 -m pip install --upgrade pip
    . .e/bin/activate
    PYCURL_SSL_LIBRARY=openssl pip install --editable .
    ```

    (--editable option means you can change code inside tinybird folder). Note that you need, at least, ClickHouse headers in order to install python dependencies

    virtualenv alternative in case something goes wrong with pyenv:

    ```bash
    # analytics is this cloned repo path
    sudo apt-get install python3-dev
    pip3 install virtualenv
    virtualenv -p python3.8 .e
    . .e/bin/activate
    ```

    **B. You might get an error like this on macOS 11.X:**

    ```bash
    ImportError: pycurl: libcurl link-time ssl backend (none/other) is different from compile-time ssl backend (openssl)
    ```

    If that's the case, try installing `pycurl` like this (use the required pycurl version):

    **Mac Intel**

    ```bash
    brew install openssl curl-openssl libffi librdkafka postgresql
    python3 -mvenv .e
    . .e/bin/activate

    # Needs the latest pip version to correctly install clickhouse-toolset
    pip install --upgrade pip

    # Install pycurl with the correct openssl files. After this, to check if pycurl is correctly installed and configured,
    # executing "python -c 'import pycurl'" must return nothing.
    export PYCURL_SSL_LIBRARY=openssl;export LDFLAGS='-L/usr/local/opt/openssl/lib -L/usr/local/opt/c-ares/lib -L/usr/local/opt/nghttp2/lib -L/usr/local/opt/libmetalink/lib -L/usr/local/opt/rtmpdump/lib -L/usr/local/opt/libssh2/lib -L/usr/local/opt/openldap/lib -L/usr/local/opt/brotli/lib';export CPPFLAGS=-I/usr/local/opt/openssl/include;pip install pycurl==7.43.0.6 --compile --no-cache-dir

    # Finally install the rest of dependencies.
    pip install --editable .
    ```

    **Mac M1**

    ```bash
    brew install openssl curl-openssl libffi librdkafka postgresql
    python3 -mvenv .e
    . .e/bin/activate

    # Needs the latest pip version to correctly install clickhouse-toolset
    pip install --upgrade pip

    # Install pycurl with the correct openssl files. After this, to check if pycurl is correctly installed and configured,
    # executing "python -c 'import pycurl'" must return nothing.
    export PYCURL_SSL_LIBRARY=openssl
    export LDFLAGS="-L/opt/homebrew/opt/curl/lib -I/opt/homebrew/opt/openssl/include"
    export CPPFLAGS="-I/opt/homebrew/opt/curl/include -L/opt/homebrew/opt/openssl/lib"
    pip install --no-cache-dir --compile --install-option="--with-openssl" --install-option="--openssl-dir=/opt/homebrew/opt/openssl@3" pycurl==7.43.0.6

    # Finally install the rest of dependencies.
    export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1
    export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=1
    pip install --editable .
    ```

7. Config pre-commit to install a pre-commit hook to prevent lint errors:

    ```bash
    pre-commit install
    ```

8. Extra system-wide configuration

    **On Linux**, increase the max number of opened files:

    ```bash
    ulimit -n 8096
    ```

    To make that change persistent, you will need to add to your `/etc/security/limits.conf` the following:

    ```bash
    # Increase # of file descriptors
    *               hard    nofile          8096
    *               soft    nofile          8096
    ```

    **On MacOS** you may have noticed that Clickhouse takes at least 5 seconds to do some operations. For instance,
    if you execute Clickhouse Local with a simple query, it may take more time than expected:

    ```bash
    ➜  clickhouse2111 time ./clickhouse local --query 'Select 1'
    1
    ./clickhouse local --query 'Select 1'  0.06s user 0.02s system 1% cpu 5.092 total
    ```

    This problem is related to how MacOS [manages internally the DNS queries and the hostname](https://stackoverflow.com/questions/44760633/mac-os-x-slow-connections-mdns-4-5-seconds-bonjour-slow)

    To fix this, you need to add your laptop hostname to the `/etc/hosts` file. For example doing:

    ```bash
    sudo su
    echo 127.0.0.1 localhost $(hostname) >> /etc/hosts
    ```

    This should be enough to fix the problem.

    **In both platforms:**

    If your ClickHouse binary is not in the system path, you will need to
    set *CLICKHOUSE_BIN_FOLDER_PATH* environment variable on your session, for
    example adding it to your shell init scripts (likely `~/.bashrc` or `~/.zshrc`).
    This will be an example for a self-compiled installation:

    ```bash
    # On self-compiled installation (Ubuntu):
    export CLICKHOUSE_BIN_FOLDER_PATH=/usr/local/bin/
    ```

9. Configure your ClickHouse (default)

    * Create the `clickhouse` user

    ```bash
    sudo groupadd -r clickhouse
    sudo useradd -r --shell /bin/false --home-dir /nonexistent -g clickhouse clickhouse
    ```

    * Copy config from CI tests

    ```bash
    # On Linux:
    sudo su
    echo '127.0.0.1 redis clickhouse-01 clickhouse-02 clickhouse-metrics' >> /etc/hosts
    cp -r tests/clickhouse-config-1/* /etc/clickhouse-server-1/
    cp -r tests/clickhouse-config-2/* /etc/clickhouse-server-2/
    mkdir -p /etc/clickhouse-server-1/config.d/
    mkdir -p /etc/clickhouse-server-2/config.d/
    cp tests/clickhouse-config-1/macros/127.0.0.1.xml /etc/clickhouse-server-1/config.d/macros.xml
    cp tests/clickhouse-config-2/macros/127.0.0.1.xml /etc/clickhouse-server-2/config.d/macros.xml
    ```

    * Set a persistent data path

    Modify `/etc/clickhouse-server-1/config.xml` and `/etc/clickhouse-server-2/config.xml` to change the data directory:

    ```xml
        <!-- Path to data directory, with trailing slash. -->
        <path>/var/lib/clickhouse/</path>
    ```

    Modify `/etc/clickhouse-server-1/config.xml` and replace `/clickhouse-server/` by `/clickhouse-server-1/` in the following lines:

    ```xml
    <log>/var/log/clickhouse-server-1/clickhouse-server.log</log>
    <errorlog>/var/log/clickhouse-server-1/clickhouse-server.err.log</errorlog>

    <include_from>/etc/clickhouse-server-1/tinybird.xml</include_from>
    ```

    And ensure the directories exist with proper permissions:

    ```bash
    sudo mkdir -p /var/lib/clickhouse /var/log/clickhouse-server-1 /var/log/clickhouse-server-2
    sudo chown clickhouse /var/lib/clickhouse /var/log/clickhouse-server-*
    ```

    **Important note:** on macOS you need to configure the TCP port to 9001 due to a bug in clickhouse-local that limits connections to the default port.

    1. Install Kafka [optional]

    Download Kafka:

    ```bash
    curl 'https://archive.apache.org/dist/kafka/2.8.0/kafka_2.13-2.8.0.tgz' | tar xz
    ```

    To avoid having to setup the KAFKA_PATH envvar, decompress it on the parent folder of analytics:

    ```bash
    my/dir/analytics
    my/dir/kafka_2.13-2.8.0
    ```

10. Configure your ClickHouse (advanced)

    This *advanced* configuration is useful when having multiple CH versions and you want to switch from one version to another easily, and have a tidy development environment (cause you're a *tidybird*)

    The steps are the same as in the previous point, but with the following differences:

    * Create the `clickhouse` user (same as above)

    ```bash
    sudo groupadd -r clickhouse
    sudo useradd -r --shell /bin/false --home-dir /nonexistent -g clickhouse clickhouse
    ```

    Let's say your working environment is going to look like this:

    ```bash
    /home/Tinybird/
    ├── ch-versions
    │   ├── 20.7.2.30
    │   └── 21.9.5.16
    │
    ├── common-config
    │   ├── clickhouse-server-1
    │   │   ├── config.d
    │   │   ├── config.xml
    │   │   ├── logs
    │   │   ├── macros
    │   │   ├── tinybird.xml
    │   │   └── users.xml
    │   ├── clickhouse-server-2
    │   │   ├── config.d
    │   │   ├── config.xml
    │   │   ├── logs
    │   │   ├── macros
    │   │   ├── tinybird.xml
    │   │   └── users.xml
    │   └── clickhouse-server-metrics
    │       ├── config.d
    │       ├── config.xml
    │       ├── logs
    │       ├── macros
    │       ├── metrics.xml
    │       └── users.xml
    │
    ├── common-data
    │   ├── clickhouse-server-1
    │   ├── clickhouse-server-2
    │   └── clickhouse-server-metrics
    ```

    In the `common-config` directory, you can copy the three clickhouse configurations you can find in the `tests` directory: `clickhouse-config-1`, `clickhouse-config-2` and `clickhouse-config-metrics`.

    > Note: The metrics directory is only necessary for developing 'distributed' metrics features, as they are on production.

    * The purpose of this is to have:
      * A `tinybird` cluster with 2 replicas (which means, you'd have to launch 2 clickhouse servers)
      * A `metrics` cluster (which needs another clickhouse server if needed)

    * Add clickhouse hosts in your `/etc/hosts` file:

    ```bash
    sudo su
    echo '127.0.0.1 clickhouse-01 clickhouse-02 clickhouse-metrics' >> /etc/hosts
    ```

    * Copy the config servers:

    ```bash
    mkdir /home/Tinybird/common-config

    cp -r tests/clickhouse-config-1/* /home/Tinybird/common-config/clickhouse-server-1/
    cp -r tests/clickhouse-config-2/* /home/Tinybird/common-config/clickhouse-server-2/
    cp -r tests/clickhouse-config-metrics/* /home/Tinybird/common-config/clickhouse-server-metrics/

    mkdir -p /home/Tinybird/common-config/clickhouse-server-1/config.d/
    mkdir -p /home/Tinybird/common-config/clickhouse-server-2/config.d/
    mkdir -p /home/Tinybird/common-config/clickhouse-server-metrics/config.d/

    cp tests/clickhouse-config-1/macros/127.0.0.1.xml /home/Tinybird/common-config/clickhouse-server-1/config.d/macros.xml

    cp tests/clickhouse-config-2/macros/127.0.0.1.xml /home/Tinybird/common-config/clickhouse-server-1/config.d/macros.xml

    cp tests/clickhouse-config-metrics/macros/127.0.0.1.xml /home/Tinybird/common-config/clickhouse-server-1/config.d/macros.xml
    ```

    * Create the common data directory

    ```bash
    mkdir /home/Tinybird/common-data
    ```

    * Change the config files in your `common-config` directory to set up the config paths properly **for each server** in its `config.xml` file:
      * Logs: `<log>/home/Tinybird/common-config/clickhouse-server-1/logs/clickhouse-server.log</log>`
      * Error logs: `<errorlog>/home/Tinybird/common-config/server-metrics/logs/clickhouse-server.err.log</errorlog>`
      * Data: `<path>/home/Tinybird/common-data/clickhouse-server-1/data/</path>`
      * Data tmp: `<tmp_path>/home/Tinybird/common-data/clickhouse-server-1/data/tmp/</tmp_path>`
      * User files: `<user_files_path>/home/Tinybird/common-data/clickhouse-server-1/data/user_files/</user_files_path>`
      * Include: `<include_from>/home/Tinybird/common-data/clickhouse-server-1/tinybird.xml</include_from>`
        * Include in metrics: `<include_from>/home/Tinybird/common-data/clickhouse-server-1/metrics.xml</include_from>`
      * Format schemas: `<format_schema_path>/home/Tinybird/common-data/clickhouse-server-1/data/format_schemas/</format_schema_path>`

    * Uncomment `metrics` config cluster in `/home/Tinybird/common-config/clickhouse-server-*/tinybird.xml` files.

### Start ClickHouse and zookeeper

Leave opened the zookeeper service:

```bash
# On Linux:
sudo /usr/share/zookeeper/bin/zkServer.sh start-foreground
```

* Default:

Start a ClickHouse server:

```bash
sudo -u clickhouse CH_PORT_01=8123 clickhouse-server --config-file=/etc/clickhouse-server/config.xml
```

* Advanced:

  > Note: We're using the full path to be more explicit on where is each file. It's more verbose, but for a guide it's easier to understand.

  In the advanced mode, you choose the CH version to launch each time, on each server.

  * clickhouse-01

      ```bash
      sudo -u clickhouse CH_PORT_01=8123 ./home/Tinybird/ch-versions/21.9.5.16/usr/bin/clickhouse server --config-file=/home/Tinybird/common-config/clickhouse-server-1/config.xml
      ```

  * clickhouse-02

      ```bash
      sudo -u clickhouse CH_PORT_02=8124 ./home/Tinybird/ch-versions/21.9.5.16/usr/bin/clickhouse server --config-file=/home/Tinybird/common-config/clickhouse-server-2/config.xml
      ```

  * clickhouse-metrics

      ```bash
      sudo -u clickhouse CH_PORT_03=8125 ./home/Tinybird/ch-versions/21.9.5.16/usr/bin/clickhouse server --config-file=/home/Tinybird/common-config/clickhouse-server-metrics/config.xml
      ```

      You can now enter any of the three CH servers using `clickhouse client` (by default, it'll go to port 9000, which is clickhouse-01, but you can select a different one by doing `-h clickhouse-02`, for instance):

      ```bash
      $ ./home/Tinybird/ch-versions/21.9.5.16/usr/bin/clickhouse client
      ClickHouse client version 21.9.5.16 (official build).
      Connecting to localhost:9000 as user default.
      Connected to ClickHouse server version 21.9.5 revision 54449.
      ```

You can check if your clusters are correctly configured from the clickhouse console:

```sql
:) select cluster, shard_num, replica_num, host_name, host_address, port, is_local from system.clusters

┌─cluster──┬─shard_num─┬─replica_num─┬─host_name──────────┬─host_address─┬─port─┬─is_local─┐
│ metrics  │         1 │           1 │ clickhouse-metrics │ 127.0.0.1    │ 9002 │        0 │
│ tinybird │         1 │           1 │ clickhouse-01      │ 127.0.0.1    │ 9000 │        0 │
│ tinybird │         1 │           2 │ clickhouse-02      │ 127.0.0.1    │ 9001 │        0 │
└──────────┴───────────┴─────────────┴────────────────────┴──────────────┴──────┴──────────┘
```

Finally, you need to create the following data source in the metrics server:

```bash
clickhouse client -mn -h clickhouse-metrics
```

```sql
CREATE TABLE default.usage_metrics_processed_log on cluster metrics
(
       date Date,
       database String,
       host String,
       read_bytes UInt64,
       written_bytes UInt64
)
ENGINE SummingMergeTree
PARTITION BY toYYYYMM(date)
ORDER BY (host, database, date);
```

### Testing locally

1. Install testing dependencies

    ```bash
    pip install -e ".[test]"
    ```

2. Run the tests with [pytest](https://docs.pytest.org/en/stable/usage.html):

   * To run all tests

   ```bash
   pytest tests
   ```

   * There're several options, for example, testing a single file:

   ```bash
   pytest tests/views/test_api_datasources.py -vv
   ```

   * Running a single test:

   ```bash
   pytest tests/views/test_api_datasources.py -k test_name
   ```

### Starting the development environment

> Note: remember about setting the CLICKHOUSE_BIN_FOLDER_PATH correctly with the version you want to use in the app, as it's explained above

```bash
tinybird_server --port 8001
```

* Using the *advanced* configuration from above:

```bash
CLICKHOUSE_BIN_FOLDER_PATH=/home/Tinybird/ch-versions/21.9.5.16/usr/bin tinybird_server --port 8001
```

**Important note:** on macOS add `OBJC_DISABLE_INITIALIZE_FORK_SAFETY` as follows

```bash
OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES tinybird_server --port 8001
```

### Useful commands

If running CH with docker, you can do the following to connect to ClickHouse client

```bash
docker exec -it tt ClickHouse client
```

### Configuring the metrics

If you've configured your clickhouse environment following the *advanced* steps, you should be able to activate the metrics by changing the `default_secrets.py` file adding: `metrics_cluster="metrics"`

## Developing in the UI

We encourage you to use **node** version 16 to have the same version that we use in production builds. Then, in the root of the project:

```bash
npm install
npm run dev:build
```

If you want to make changes and check how they look:

```bash
npm run dev:watch
```

Don't forget to test your changes:

```bash
npm run test
```

Or test + watch 🤗:

```bash
npm run test:watch
```

You have more information about development [here](development.md).

## FAQ

### Which ClickHouse version should I install?

That depends on your role. As a rule of thumb:

* If you are not a developer or don't want to do backend-related work. Download the recommended prebuilt release.

* If you are doing backend work, you should have available several different releases available for testing. The oldest one we support at the moment is 20.7.2.30.
  The default in production is 21.9.5.16. See the official [prebuilt binaries](https://clickhouse.com/docs/en/getting-started/install/#from-tgz-archives).
  You should also have your own build copy of ClickHouse for testing and debugging purposes as explained [here](#installing-the-development-environment)

Finally, ClickHouse/master should be considered to be stable and fully compatible with Analytics. All tests should pass and everything work as expected.
If you detect any issue, please open a ticket and tag it as `clickhouse-*"

### What do I do to validate my development environment is working correctly?

Browse to [http://localhost:8001/dashboard](http://localhost:8001/dashboard). You'll be prompted to login with your gmail account. Go back to /dashboard once you do and try importing

### I can't connect to ClickHouse with tinybird configuration

```bash
clickhouse client -h clickhouse-01
```

### Where is the marketing website code?

It is in [webflow](https://webflow.com/)

### Where is the blog hosted?

It is generated with Jekyll, and it is located in other [repository](https://gitlab.com/tinybird/blog).

### How can I see the documentation?

There is an automatic deploy job created so every time you merge something in master, if everything goes OK, the latest version of the documentation will be available at [https://docs.tinybird.co](https://docs.tinybird.co)

## Using native ClickHouse builds with macOS

Downloading the latest version of ClickHouse already compiled:

```bash
curl -O 'https://builds.clickhouse.tech/master/macos/clickhouse' && chmod a+x ./clickhouse
sudo -u clickhouse CH_PORT_01=8123 clickhouse-server --config-file=/etc/clickhouse-server/config.xml
```

## Building a new CI docker container image

```bash
# Build a new image `test-tmp
docker build -t test-tmp:latest -f gitlab/tests-integration.Dockerfile .

# Login, you'll need to create a new gitlab API token
docker login registry.gitlab.com

# Tag & push your image
docker tag test-tmp registry.gitlab.com/tinybird/analytics/test-tmp
docker push registry.gitlab.com/tinybird/analytics/test-tmp
```

Note: Docker images contain the analytics python dependencies. If you change the dependencies in any of the `setup.py` files it'll work, but ideally you should include it in the Docker images as well.

## Debugging problems in gitlab CI

You can use `gitlab-runner` to execute any `.gitlab-ci.yml` job locally. Follow these steps to debug any of those jobs:

* Modify the `.gitlab-ci.yml` file, including `tail -f /dev/null` in the script section of the job
* Run the job you need with gitlab-runner, for instance: `gitlab-runner exec docker tests_integration_ch_207_py38`
* Wait until the container stops in `tail -f /dev/null`
* `docker ps` to list the name of the Docker container
* Open a shell session inside the container `docker exec -it <docker_name_from_previous_step> /bin/bash`
* Now you can run anything you need to debug, including breakpoints with pdb, etc.
* Once you finish stop the container `docker stop <docker_name>`

Note: If you do any modification to a project file, you need to commit it in order to be available in the Docker container. Once you finish you can squash all the commits.

## Adding distributed metrics

Read the [metrics](METRICS.md) guide.
