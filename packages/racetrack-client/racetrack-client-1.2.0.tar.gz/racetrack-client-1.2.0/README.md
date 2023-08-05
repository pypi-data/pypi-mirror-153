# Racetrack client context
`racetrack-client` is a CLI client tool for deploying workloads to Racetrack (IKP-RT).

Racetrack system allows to deploy jobs in a one step.
It transforms your code to in-operation workloads, e.g. Kubernetes workloads.
You write some code according to a set of coventions, you include the manifest file which explains the code, 
and you submit it to Racetrack. A short while after, the service calling your code is in operation.

# Quickstart
1. [Install](#installation) `racetrack` client: `pip3 install racetrack-client`
1. [Configure access token](#private-job-repositories) to your git repository: `racetrack config credentials set REPO_URL USERNAME TOKEN`
1. [Deploy](#deploying) your job to Racetrack: `racetrack deploy . https://racetrack.example.com/ikp-rt/lifecycle`
1. You will see the URL of your deployed job in the output.

# Installation
Install racetrack-client using pip:
```bash
pip3 install racetrack-client
```

Python 3.8+ is required. So if you have any troubles, try with:
```
sudo apt install python3.8 python3.8-dev python3.8-venv
python3.8 -m pip install racetrack-client
```

This will install `racetrack` CLI tool. Verify installation by running `racetrack`.

# Usage
Run `racetrack --help` to see usage.

## Deploying
To deploy a job, just run in the place where `fatman.yaml` is located:
```bash
racetrack deploy . https://racetrack.example.com/ikp-rt/lifecycle
```

`racetrack deploy [WORKDIR] [RACETRACK_URL]` has 2 optional arguments:
- `WORKDIR` - a place where the `fatman.yaml` is, by default it's current directory
- `RACETRACK_URL` - URL address to Racetrack server, where a job should be deployed. 
  If not given, it will be deployed to a URL configured in a local client config, 
  by default it's set to a local cluster at `http://localhost:7002`.

## Showing logs

To see recent logs from your Fatman output, run `racetrack logs` command:
```bash
racetrack logs . https://racetrack.example.com/ikp-rt/lifecycle
```

`racetrack logs [WORKDIR] [RACETRACK_URL]` has 2 arguments:
- `WORKDIR` - a place where the `fatman.yaml` is, by default it's current directory
- `RACETRACK_URL` - URL address to Racetrack server, where the Fatman is deployed.

## Local client configuration
If you want to update client configuration (namely persist some preferences for later use), use the following command: 
```bash
racetrack config set [CONFIG_NAME] [VALUE]
```
Local client configuration is stored at `~/.racetrack/config.yaml`.

### Configuring default Racetrack URL
You can set default Racetrack URL address: 
```bash
racetrack config racetrack_url https://racetrack.example.com/ikp-rt/lifecycle
```
Then you can run just `racetrack deploy` command (without `RACETRACK_URL` argument), racetrack_url will be inferred from client configuration.

### Private Job repositories
Before building & deploying a Job stored in a private git repository, you should make sure that Racetrack has access to it.
Add git credentials to access your repository using command:
```bash
racetrack config credentials set REPO_URL USERNAME TOKEN
```

- `REPO_URL` can be a full URL of a git remote (eg. https://gitlab.com/git/namespace/ikp-rt)
or a general domain name (eg. https://gitlab.com) if you want to use same token for all repositories from there.
- `USERNAME` is your git account username
- `TOKEN` is a password to read from your repository.
  Use access tokens with `read_repository` scope instead of your real password!
  Here's [how to create personal access token in Gitlab](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#creating-a-personal-access-token)

### Racetrack URL aliases

You can set up aliases for Racetrack server URL addresses by issuing command:
```bash
racetrack config alias set ALIAS RACETRACK_URL
```

If you operate with many environments, setting short names may come in handy. For instance:
```bash
racetrack config alias set dev https://dev.racetrack.example.com/ikp-rt/lifecycle
racetrack config alias set test https://test.racetrack.example.com/ikp-rt/lifecycle
racetrack config alias set prod https://prod.racetrack.example.com/ikp-rt/lifecycle
racetrack config alias set kind http://localhost:7002
racetrack config alias set compose http://localhost:7102
```

and then you can use your short names instead of full `RACETRACK_URL` address when calling `racetrack deploy . dev`.

# Development setup
Clone IKP-RT repository and run it inside this directory:
```bash
make setup
```
