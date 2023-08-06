# Timeseer.AI

Timeseer is a Flask web application that can run data quality analyses on time series data.

![Timeseer components](diagrams/components.svg)

## Running

First, install Python and `npm`.

Then create a virtualenv for Python and install dependencies:

```bash
$ python -m venv venv
$ source venv/bin/activate
$ make deps
```

Then generate the NPM libraries:

```bash
$ make npm
```

Then start Timeseer:

```bash
$ make run
```

Timeseer is now listening on http://localhost:5000.

Timeseer Bus needs to be started separately:

```bash
$ make run-bus
```

Timeseer Bus is listening on http://localhost:8081.

## Configuration

See the [Admin docs](docs/admin/admin.asciidoc).

## Client

See [Timeseer client](timeseer_client/README.md).

### Release

To release a new timeseer client package to PyPI, tag the appropriate commit with `client-<version_number>`.

example:
```bash
git tag -a client-0.0.1
```

## Windows

Then ensure the version number in `setup_windows.py` is correct.

Package Timeseer as a Windows `.msi` installer by running:

```
> .\build_timeseer.ps1
```

This builds the javascript,
updates the documentation and generates an MSI Installer in `dist/`.

For quick testing during development,
a Windows Sandbox configuration is available in `windows/sandbox-timeseer.wsb`.

First configure Timeseer by providing a `Timeseer.toml` configuration file.
A `Timeseer-example.toml` file is provided to be copied.

Note that by default, Timeseer is configured on Windows to launch only one worker.
This is a safe default for systems with limited memory.
If not enough memory is available, the Windows Event Viewer will show that the service crashed
with a DEP (Data Execution Prevention) exception.
This probably happens because a `malloc()` returns `NULL` and this is not checked,
causing a `0x0` pointer dereference.

## M1 Macs (using Rosetta)

Configure the terminal app to `Open using Rosetta`. To do this, select it
inside the applications folder on Finder, press ⌘+i, and check this option.
Optionally, first create a copy of the terminal app being used.
This way it's possible to have the original running natively and set the
copy to run using Rosetta.

Open the terminal configured for Rosetta and use it to install homebrew.
Follow the default instructions on their [homepage](https://brew.sh).
This is required even if homebrew has already been installed for the M1.
The ARM (M1) installation of homebrew should be in `/opt/homebrew/bin/brew`,
and installing it again inside the Rosetta terminal should result in a separate
version under `/usr/local/bin/brew`.

Use the homebrew installed inside our Rosetta environment to install
python. This python installation should be located at
`/usr/local/Cellar/python@3.9/3.9.12/bin/python3` (version numbers may differ).
Use this version of python to create a virtual environment and then activate it.
After this is done, the usual steps to install deps and run the project will
be working.

Remember to use the Rosetta version of homebrew to install extra build dependencies
as needed. Solution based on
[this article](https://medium.com/thinknum/how-to-install-python-under-rosetta-2-f98c0865e012).

## Development

Install all dependencies:

```bash
(venv) $ make deps dev-deps unix-deps
```

You might need to install additional dependencies for [xmlsec](https://pypi.org/project/xmlsec/).

Format Python code using [black](https://github.com/psf/black):

```bash
(venv) $ make format
```

Lint (and autoformat JS):

```bash
(venv) $ make lint
```

To lint only Python code:

```bash
(venv) $ make lint-python
```

To lint only JS code:

```bash
$ make lint-js
```

Test:

```bash
(venv) $ make test
```

Run the docker container locally:

```bash
$ make run-docker
```

This will start Timeseer at http://localhost:8080.

The examples and example configuration will be volume mapped in the container.

Run a Timeseer bus instance locally:

```bash
$ make run-docker-bus
```

This will start Timeseer Bus at http://localhost:8081.

The examples and example configuration will be volume mapped in the container.

While developing, the `timeseer` module will not be found in tests or modules in VS Code.
To solve this, install the package:

```
(venv) $ pip install -e .
```

Update the VS Code settings to add the current path to the `pylint` path:

```json
    "python.linting.pylintArgs": ["--init-hook", "'import sys; sys.path.append(\".\")'"],
```

To enable 'hot' reload for the react files run:

```bash
(venv) $ make npm-dev
```

Finally,
to remove any generated output (javascript and documentation),
use:

```bash
$ make clean
```

### Timeseer Client

To run and test a timeseer client locally

Create a new build of the timeseer client

``` bash
(venv) $ python3 timeseer_client/setup_client.py install
```

Create the distributions

``` bash
(venv) $ python3 timeseer_client/setup_client.py sdist bdist_wheel
```

Create a new empty venv to load in your distributions and test

```bash
$ python -m venv venv-new
$ source venv-new/bin/activate
```

Copy the unzipped `timeseer-0.0.0.tar.gz` files into the `venv-new/lib` to start testing.

### E2E Testing

Timeseer uses [cypress](https://www.cypress.io/) to run E2E tests.

E2E tests rely on the ['TSAI Antwerp' data source](https://demo-data.dev.timeseer.ai).

The E2E tests expect Timeseer to be available on port 8080.

Start Timeseer with:

```
$ python -m timeseer.cli
```

on Mac start with:

```
$ python -m windows.server_windows
```

To run the E2E tests, use:

```
$ npm run cypress:run
```

During development, use:

```
$ npm run cypress:open
```

### Windows

On Windows, the usual Unix tooling is not available.
Install Python and NPM (Node.js).

Install the npm packages:

```
PS > npm ci
PS > npm run build
```

Create the virtual environment:

```
PS > python -m venv venv
```

To be able to enter the virtual environment, allow running unsigned scripts.
This can be done for the current session only:

```
PS > Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process
```

Alternatively, launch Powershell with the `-ExecutionPolicy Unrestricted` flag.
This can be configured in the Windows Terminal profile.

Enter the virtual environment:

```
PS > .\venv\Scripts\activate
(venv) PS >
```

Set the environment variables required by Flask to start:

```
(venv) PS > $Env:FLASK_APP = "timeseer.web"
(venv) PS > $Env:FLASK_ENV = "development"
```

Then start Timeseer:

```
(venv) PS > python -m flask run
```

### Configuration

The default configuration contains an include for `data/*.toml`.
Store the configuration for development sources in `data/`.
This prevents them to be overwritten by updates and does not require them to be stashed away when rebasing.

To start Timeseer (on http://localhost:8080) with only one customer configuration loaded, use:

```bash
(venv) $ python -m timeseer.cli --config-file data/<customer>.toml
```

To start both the web server (on http://localhost:8080) and the flight interface (on localhost:8080),
create `data/flight.toml`:

```
[flight]
enable = true
authentication = false
```

Now start Timeseer with:

```bash
$ python -m timeseer.cli
```

This will not automatically reload the web server when files change.
Use `make` and `make run-bus` separately to achieve that.

### Database Migrations

Timeseer uses [Yoyo](https://ollycope.com/software/yoyo/latest/) for database migrations.
There is one subdirectory of `timeseer/repository/migrations` per database.

Individual migrations follow the `<number>__<name>.(sql|py)` naming conventions.
Dependencies between migrations are not automatically inferred from the naming,
but need to be explicitly declared in the migrations itself.

For example, in `002__index.sql`:

```sql
-- depends: 001__create
```

Observe that there is no extension in the name of the migration.

### Testing mails

Python includes an SMTP server that prints mails to standard output.

Enable it with:

```bash
$ python -m smtpd -c DebuggingServer -n localhost:1025
```

### Update NPM packages

Timeseer uses `npm` and webpack to manage NPM packages.
Webpack generates static include files in `timeseer/web/static/dist/` from 'libraries' in `src/`.

Update NPM packages in `package.json`.
Then run:

```bash
$ npm run build
```

### Update diagrams

Install [PlantUML](https://plantuml.com/), then run:

```bash
$ make docs
```

### Internal documentation

Internal documentation is written in [AsciiDoc](https://asciidoctor.org/docs/asciidoc-syntax-quick-reference/) in the [docs/](docs/) directory.

Build and run the container locally:

```bash
$ make run-dev-docs
```

The documentation will be available at http://localhost:8082.

### Product documentation

Data source and admin documentation can be generated using:

```bash
$ make source-docs
$ make admin-docs
```

To generate a standalone PDF of the Admin Guide, use:

```bash
$ make standalone-admin-docs
```

### Dependency updates

Two types of thiry-party dependencies need to be updated.

Update javascript libraries using `npm`.
First update all major versions in `package.json`.

```bash
$ rm -rf node_modules
$ rm package-lock.json
$ npm install
```

This installs the latest version of all packages and locks their version in `package-lock.json`.

Python dependencies can be updated using the `requirements-top.txt` file that contains all top-level dependencies.

First remove the virtualenv and then manually install all dependencies in `requirements-top.txt`.

```bash
$ rm -rf venv/
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install ...
(venv) $ pip freeze > requirements.txt
```

First do this for the common requirements.

Then create diffs for the Unix (`requirements-unix.txt`) and Windows (`requirements-windows.txt`) requirements only.

To update `requirements-dev.txt`,
manually install the required tools in a clean virtualenv:

```bash
(venv) $ pip install black flake8 pylint mypy pytest
(venv) $ pip freeze > requirements-dev.txt
```

### License compliance

To generate a license compliance report, Fossa is used.

Download the fossa plugin

```bash
$ curl -H 'Cache-Control: no-cache' https://raw.githubusercontent.com/fossas/fossa-cli/master/install.sh | bash
```

and run the analysis with your [Fossa api key](https://app.fossa.com/account/settings/integrations/api_tokens)

```bash
$ FOSSA_API_KEY=<YOUR_FOSSA_API_KEY> make fossa
```

To generate a report make sure your Fossa api key is of all types (opposed to push-only)

```bash
$ FOSSA_API_KEY=<YOUR_FOSSA_API_KEY> make fossa-report
```

This will generate a basic report in `compliance/NOTICE.txt`

To include the complete license report a couple of manual steps needs to be completed:

1. Go to (https://app.fossa.com/projects)[https://app.fossa.com/projects] and select the Timeseer.AI project
2. Go to the 'Reports' tab, select html format and download the report.
3. Rename the downloaded file to `license-report.html` and remove the `head`-tag
4. Make the date in `header`-tag unambiguous by using 'Month Year' e.g: `March 2021`
5. Place the `license-report.html` file in the `timeseer/web/templates/compliance` folder

### Create an Azure VM for performance tests

The [scripts/deploy-performance-test.yml](scripts/deploy-performance-test.yml) playbook is able to create a VM where a Timeseer wheel can be deployed.
The VM has access to large data sets.

First build a wheel for Timeseer:

```bash
(venv) $ make clean-python wheel
```

Ensure that Ansible can authenticate to Azure.

The most straightforward way to do this is to create a file `~/.azure/credentials`:

```ini
[default]
subscription_id=270d8f43-e23b-4366-8954-ea7131e4e128
client_id=ffa71394-3b51-4fc0-9c05-ef2dd9eb6eb5
secret="<>"
tenant=b5e6dd09-4097-4c39-ac09-8c3ba45950f6
```

The `secret` value is the value of your Client Secret for the `ansible-local` App Registration in Azure Active Directory.

Install Ansible and the correct libraries in a new virtualenv to avoid conflicts in the Azure libraries used by Timeseer and Ansible:

```bash
$ python -m venv venv-ansible
(venv-ansible) $ pip install 'ansible==2.10.0'
(venv-ansible) $ ansible-galaxy collection install --force azure.azcollection
(venv-ansible) $ pip install -r ~/.ansible/collections/ansible_collections/azure/azcollection/requirements-azure.txt

```

Then,
run the playbook:

```bash
(venv-ansible) $ ansible-playbook scripts/deploy-performance-test.yml --extra-vars "deploy_name=001"
```

To run this command on mac, an extra environment variable need to be added

```bash
(venv-ansible) $ OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES ansible-playbook scripts/deploy-performance-test.yml --extra-vars "deploy_name=001"
```

The `deploy_name` variable should identify your deployment.

Other optional `--extra-vars`:

- `cpu_cores`: the number of cores on the VM instance
- `spot`: `yes` to create a spot VM instance

For example:
```bash
(venv-ansible) $ ansible-playbook scripts/deploy-performance-test.yml --extra-vars "deploy_name=001 cpu_cores=8"
```

The playbook will print the SSH command to connect to the VM.
SSH public keys are read from your Github profile.

```ansible
TASK [debug] **********************************************************************************************************************************************
ok: [localhost] => {
    "msg": "The VM is available using 'ssh sysadmin@20.123.201.16'"
}

```

To remove the resource group on Azure:

```bash
(venv-ansible) $ ansible-playbook scripts/remove-performance-test.yml --extra-vars "deploy_name=001"
```

### Manual deploy to acceptance environment

The [acceptance test environment](https://acceptance.timeseer.ai) runs on an Azure VM.

Start the `vm-acceptance` VM in the Azure portal,
in the `rg-acceptance` resource group.

Local deployments can be triggered using Ansible.
Configure a virtualenv for Ansible as documented in the previous chapter and generate a wheel:

```bash
(venv) $ make clean-python wheel
```

Then run the playbook:

```bash
(venv-ansible) $ ansible-playbook scripts/deploy-acceptance.yml -i scripts/hosts
```

To run this command on mac, an extra environment variable need to be added

```bash
(venv-ansible) $ OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES ansible-playbook scripts/deploy-acceptance.yml -i scripts/hosts
```

The [Timeseer configuration](scripts/roles/timeseer/files/Timeseer-acceptance.toml) for the acceptance environment is managed in this repository.
Updates to it happen automatically on deploy.

### Automatic deploy to acceptance environment

Write a commit id to [`scripts/acceptance`](scripts/acceptance).

```bash
$ echo $(git rev-parse HEAD) > scripts/acceptance
```

This triggers a Github Action that starts the acceptance test environment and deploys the given commit.

## Release to demo

To release a new version to the demo server, tag the commit with `v<version>`

```bash
$ git tag -a v1.0.0
```

This will tag the latest docker image with a `stable` tag and deployed to the demo server.
