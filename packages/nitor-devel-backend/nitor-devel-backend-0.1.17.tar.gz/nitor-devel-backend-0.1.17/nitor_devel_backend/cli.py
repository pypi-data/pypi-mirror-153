#!/usr/bin/env python3

import json
import os
import sys
import base64
from os import unlink, environ, path, R_OK, access
from os.path import exists, expanduser, isfile, join
from hashlib import sha256
from secrets import choice
from threading import Thread
from argparse import ArgumentParser
from shutil import which
from tempfile import mkstemp
from subprocess import Popen, PIPE
from threadlocal_aws.resources import ec2
from n_vault import Vault
from n_utils.profile_util import get_profile
from threadlocal_aws.clients import ecr, sts, iam
from n_utils.yuuuu3332111i1l1i import i1ii1iIII as machine_uuid
from n_utils.utils import id_generator
from ec2_utils.instance_info import stack_params_and_outputs_and_stack

def patch_service(service, port):
    if service["type"] == "proxy" and (
        ".internal" in service["host"] or "targetGroup" in service
    ):
        service["host"] = "localhost"
        service["port"] = port
        if "targetGroup" in service:
            del service["targetGroup"]
    for key, value in service.items():
        if isinstance(value, str):
            service[key] = value.replace("${host}", os.getlogin())

def mangle_conf(filename, args):
    forwarding_port = 9999
    conf = json.loads(Vault().lookup(f"config-sites-{args.environment}.json"))
    conf["publicURI"] = "https://localhost:8443"
    conf["tls"] = {
        "serverKey": "certs/localhost.key.clear",
        "serverCert": "certs/localhost.crt",
    }
    conf["session"] = {"serverName": "", "secretFile": ".secret", "sessionAge": 1209600}
    impersonate_service = None
    for service in conf["services"].copy():
        # Virtualhost confs can not work
        if service["type"] == "virtualHost":
            conf["services"].remove(service)
            if service["host"] == args.impersonate:
                impersonate_service = service
                service["host"] = "localhost"
                for subservice in service["services"]:
                    patch_service(subservice, forwarding_port)
                for last_service in reversed(service["services"]):
                    if last_service["type"] == "s3":
                        service["services"].remove(last_service)
                        break
        else:
            patch_service(service, forwarding_port)

    for last_service in reversed(conf["services"]):
        if last_service["type"] == "s3":
            conf["services"].remove(last_service)
            break

    local_service = [{}, {}]
    local_service[0]["type"] = "static"
    local_service[0]["route"] = "/apitesting/*"
    local_service[0]["dir"] = "/app/apitesting"
    local_service[0]["readOnly"] = True
    local_service[0]["cacheTimeout"] = 1800

    if args.port:
        local_service[1]["type"] = "proxy"
        local_service[1]["host"] = "host.docker.internal"
        local_service[1]["route"] = "/*"
        local_service[1]["port"] = int(args.port)
        local_service[1]["path"] = "/"
        local_service[1]["receiveTimeout"] = 300
    elif args.directory:
        local_service[1]["type"] = "static"
        local_service[1]["route"] = "/*"
        local_service[1]["dir"] = "/app/static"
        local_service[1]["readOnly"] = False
        local_service[1]["cacheTimeout"] = 1
    elif args.service:
        local_service = json.loads(args.service)
    elif args.file:
        local_service = json.load(args.file)

    if impersonate_service:
        impersonate_service["services"] += local_service.copy()
        local_service = [impersonate_service]

    conf["services"] += local_service
    
    with open(filename, "w") as conffile:
        json.dump(conf, conffile)

    print(f"Patched configuration into {filename}")

def run_backend(args, instance):
 
    try:
        _, fname = mkstemp()
        mangle_conf(fname, args)
        if docker := which("docker"):
            beginning = [
                docker,
                "run",
                "-p",
                "8443:8443",
                "-e",
                "AWS_ACCESS_KEY_ID",
                "-e",
                "AWS_SECRET_ACCESS_KEY",
                "-e",
                "AWS_SESSION_TOKEN",
                "-e",
                "ENV",
                "-e",
                "AWS_DEFAULT_REGION",
                "-e",
                "AWS_REGION",
                "-e",
                "INSTANCE_ID",
                "-e",
                "SECRET",
            ]
            if sys.platform == "linux":
                beginning.append("--add-host=host.docker.internal:host-gateway")
            mounts = ["--mount", f"type=bind,src={fname},dst=/app/config.json,ro"]
            if args.directory:
                mounts += [
                    "--mount",
                    f"type=bind,src={path.abspath(args.directory)},dst=/app/static,ro",
                ]
            end = [
                "832585949989.dkr.ecr.eu-west-1.amazonaws.com/devel-backend/dev-proxy:0046"
            ]
            cmd = beginning + mounts + end
            # Login to ecr
            repo = ecr(region="eu-west-1").describe_repositories(
                repositoryNames=["devel-backend/dev-proxy"]
            )["repositories"][0]
            token_resp = ecr(region="eu-west-1").get_authorization_token(
                registryIds=[repo["registryId"]]
            )
            if "authorizationData" in token_resp:
                auth_data = token_resp["authorizationData"][0]
                full_token = (
                    base64.b64decode(auth_data["authorizationToken"])
                    .decode("utf-8")
                    .split(":")
                )
                user = full_token[0]
                token = full_token[1]
                login_proc = Popen(
                    [
                        docker,
                        "login",
                        "-u",
                        user,
                        "-p",
                        token,
                        auth_data["proxyEndpoint"],
                    ]
                )
                login_proc.communicate()
            print_cmd = cmd.copy()
            print(" ".join(print_cmd))
        else:
            print(f"Need to have docker installed to run nitor-backend")
            sys.exit(1)
        run_env = environ.copy()
        run_env["AWS_DEFAULT_REGION"] = "eu-west-1"
        run_env["AWS_REGION"] = "eu-west-1"
        run_env["ENV"] = args.environment
        resp, _ = stack_params_and_outputs_and_stack(
            stack_name="sites-sites-" + args.environment, stack_region="eu-west-1"
        )
        role = iam(region="eu-west-1").get_role(RoleName=resp["resBackendRole"])
        role_arn = role["Role"]["Arn"]
        session = sts(region="eu-west-1").assume_role(RoleArn=role_arn, RoleSessionName="nitorbackend-" + id_generator())
        run_env["AWS_ACCESS_KEY_ID"] = session["Credentials"]["AccessKeyId"]
        run_env["AWS_SECRET_ACCESS_KEY"] = session["Credentials"]["SecretAccessKey"]
        run_env["AWS_SESSION_TOKEN"] = session["Credentials"]["SessionToken"]
        run_env["INSTANCE_ID"] = instance
        my_uuid = machine_uuid()
        run_env["SECRET"] = sha256(my_uuid.encode()).hexdigest()[:63]
        proc = Popen(cmd, env=run_env)
        try:
            proc.communicate()
        except:
            pass
    finally:
        unlink(fname)


def cli_run_backend():
    parser = ArgumentParser(
        description="Run a nitor backend locally to enable serving nitor data backends and your development server resources from the same port."
        + " Proxy is available on https://localhost:8443 and can not be changed because it is configured as a redirect url for the authentication provider."
    )
    parser.add_argument(
        "environment",
        help="Run agains dev or prod data resources",
        choices=["dev", "prod"],
    )
    source_args = parser.add_mutually_exclusive_group(required=True)
    source_args.add_argument(
        "--port", "-p", help="The port your local dev server is listening to"
    )
    source_args.add_argument(
        "--directory",
        "-d",
        help="The directory holding your created site static artifacts",
    )
    source_args.add_argument(
        "--service",
        "-s",
        help="Give dev service backend configuration as json on the command line in case you want to for example mix a local dynamic server "
        + "with local static resources. Needs to be an array of service configuration elements. "
        + "See https://github.com/NitorCreations/nitor-backend for available services.",
    )
    source_args.add_argument(
        "--file",
        "-f",
        help="Give dev service backend configuration as json in a file. See above.",
    )
    parser.add_argument(
        "--impersonate",
        "-i",
        help="Impersonate a virtualhost service in the existing configuration by forwarding any proxy subservices with the target in "
        + "the internal ALB to the ssh tunnel and forwarding s3 traffic to the local development backend.",
    )
    parser.add_argument(
        "--dumpconfig",
        "-c",
        help="Dump mangled configuration to given file and exit"
    )
    args = parser.parse_args()
    if "AWS_PROFILE" not in environ:
        parser.error(
            "AWS_PROFILE environment variable needs to be defined to give access to the container image and port forwardings. Preferably via 'eval \"$(ndt enable-profile nitor-infra)\"' or 'nep nitor-infra'"
        )
    if args.dumpconfig:
        mangle_conf(args.dumpconfig, args)
    else:
        instance = choice(
            list(
                ec2(region="eu-west-1").instances.filter(
                    Filters=[
                        {"Name": "tag:Name", "Values": [f"ecs-infra-{args.environment}"]}
                    ]
                )
            )
        )
        run_backend(args, instance.id)
