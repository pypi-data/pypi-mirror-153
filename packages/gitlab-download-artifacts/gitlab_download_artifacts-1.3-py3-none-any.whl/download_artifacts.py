#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Will download the gitlab artifacts matching a git or submodule, or provided repo http url (optionally with @<commit>)

import os
import ssl
import time
import json
import shutil
import base64
import argparse
import webbrowser
from pathlib import Path
from subprocess import run
from zipfile import ZipFile
from urllib.parse import urlsplit
from urllib.request import urlopen, Request

ctx = ssl.create_default_context()
ctx.load_default_certs()


def download(submodule: str, job: str, project_token=None, timeout: int = 20):
    priv_token = project_token or os.environ.get('PROJECT_TOKEN', os.environ.get('PRIVATE_TOKEN'))

    if str(submodule).startswith('https://'):
        target = Path(".") / "._artifact.zip"
        urlparts = urlsplit(submodule)
        if '@' in urlparts.path:
            commit = urlparts.path.split('@')[-1]
            url = submodule.replace(commit, '').strip('@')
        else:
            url = submodule
            commit = None
        urlprint = url.replace(urlparts.password, '<pass>') if urlparts.password else url
    else:
        target = Path(submodule) / "._artifact.zip"
        url = urlprint = run(['git', 'remote', 'get-url', 'origin'], cwd=submodule, capture_output=True).stdout.decode().strip()
        commit = run(['git', 'rev-parse', 'HEAD'], cwd=submodule, capture_output=True).stdout.decode().strip()

    print(f"Searching for gitlab artifacts from: {urlprint}@{commit} job: {job}")

    if url.startswith('git@'):
        url = url.replace(':', '/').replace('git@', 'https://')
    if url.endswith('.git'):
        url = url[:-4]
    if url.endswith('/'):
        url = url[:-1]

    urlparts = urlsplit(url)

    timeout_time = time.time() + (timeout * 60)
    
    if priv_token or (urlparts.username and urlparts.password):
        project = urlparts.path.strip('/').replace('/', '%2F')

        api_url = f"{urlparts.scheme}://{urlparts.hostname}/api/v4/projects/{project}"

        if priv_token:
            header = {'PRIVATE-TOKEN': priv_token}
        else:
            b64auth = base64.b64encode(("%s:%s" % (urlparts.username, urlparts.password)).encode()).decode()
            header = {"Authorization": f"Basic {b64auth}"}

        # Checking commit
        if commit is None:
            # find default branch
            resp = json.load(urlopen(Request(
                f"{api_url}/repository/branches",
                headers=header
            ), context=ctx))
            for branch in resp:
                if branch['default']:
                    commit = branch['name']
                    break

            if commit is None:
                raise SystemExit(f"Could not find default branch, please provide desired branch or commit sha")

        # Get the full sha of commit
        resp = json.load(urlopen(Request(
            f"{api_url}/repository/commits/{commit}",
            headers=header
        ), context=ctx))
        commit = resp['id']

        # Find the latest pipeline for that commit
        resp = urlopen(Request(
            f"{api_url}/pipelines?sha={commit}",
            headers=header
        ), context=ctx)

        pipelines = json.load(resp)

        if not pipelines:
            raise SystemExit(f"No CI pipelines found/run for job: {job}")

        pipelines.sort(key=lambda p: p['id'])
        
        named_jobs = None
        for pipeline in reversed(pipelines):
            pipeline_id = pipeline['id']

            desired_job = {}
            desired_job_status = None

            jobs = json.load(urlopen(Request(
                f"{api_url}/pipelines/{pipeline_id}/jobs",
                headers=header
            ), context=ctx))
            named_jobs = [j for j in jobs if j["name"] == job]
            if not named_jobs:
                print(f'Job "{job}" not found in pipeline {pipeline_id}, available: {[j["name"] for j in jobs]}')
                continue

            desired_job = named_jobs[0]

            while time.time() < timeout_time:
                desired_job_status = desired_job.get('status', None)
                if desired_job_status in ("created", "pending"):
                    print("Job hasn't started yet, waiting...")
                    time.sleep(60)

                if desired_job_status in ("success", "failed", "canceled"):
                    break

                # Job running, wait for it to finish
                print("Job %s, waiting..." % desired_job_status)
                time.sleep(20)

            if desired_job_status != 'success':
                raise SystemExit(f'Job "{job}"" artifact not available, status: {desired_job_status}')

            job_id = desired_job['id']
            print(f'Downloading artifacts from job id: {job_id}, pipeline: {pipeline_id}')

            req = urlopen(Request(
                f"{api_url}/jobs/{job_id}/artifacts",
                headers=header
            ), context=ctx)

            chunksize = 64 * 1024
            with target.open('wb') as fp:
                shutil.copyfileobj(req, fp, chunksize)

            with target.open('rb') as fp:
                if fp.read(15) == b"<!DOCTYPE html>":
                    broken_target = target.with_suffix(".broken")
                    target.rename(broken_target)
                    raise SystemExit(f"ERROR: binary not downloaded correctly, check {broken_target}")
            break

        if not named_jobs:
            raise SystemExit(f'Job "{job}" not found.')

    else:
        if os.environ.get('CI_JOB_TOKEN'):
            raise SystemExit(f"ERROR: Gitlab CI usage requires Project / private token: https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html")

        # No login token found, likely on developer PC. Download using system browser
        url = f"{url}/-/jobs/artifacts/{commit}/download?job={job}"

        if os.name == 'nt':
            from winreg import OpenKey, HKEY_CURRENT_USER, QueryValueEx
            with OpenKey(HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
                download_dir = Path(QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0])
            download_dir_print = download_dir.resolve()
        elif os.environ.get('WSL_INTEROP'):
            download_dir_win = run([
                'bash', '-l', '-c',
                '/mnt/c/WINDOWS/py.exe -c '
                '"from winreg import OpenKey, HKEY_CURRENT_USER, QueryValueEx; '
                'key = OpenKey(HKEY_CURRENT_USER, r\'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders\'); '
                'print(QueryValueEx(key, \'{374DE290-123F-4565-9164-39C4925E467B}\')[0])" '
                ], capture_output=True
            ).stdout.decode().strip()
            download_dir = Path(run(['wslpath', download_dir_win], capture_output=True).stdout.decode().strip())
            download_dir_print = download_dir_win
        else:
            download_dir = Path.home() / 'Downloads'
            download_dir_print = download_dir.resolve()

        print("**********************************************************************************")
        print("If your browser does not open automatically, please navigate to the following url:")
        print(url)
        print('*** Ensure you download the "artifacts.zip" file to:', download_dir_print)
        print("**********************************************************************************")
        time.sleep(3)

        artifact = download_dir / "artifacts.zip"
        if artifact.exists():
            os.unlink(str(artifact))

        webbrowser.open(url)

        while not artifact.exists():
            print('.', end='')
            time.sleep(1)

        shutil.copy(artifact, target)
        print(artifact, "->", target)

    if not target.exists():
        raise SystemExit("File not downloaded")

    target_dir = target.parent
    print(f"Extracting artifacts into", target_dir)
    with ZipFile(str(target.resolve()), 'r') as zipObj:
        zipObj.extractall(path=str(target_dir.resolve()))
    target.unlink()
    print("Finished")


def main():
    parser = argparse.ArgumentParser(description='Download gitlab artifacts')
    parser.add_argument('target', help="Path to git repo to grab or repo url (optionally with @<commit>)")
    parser.add_argument('job', help='Gitlab CI job name to grab from')
    parser.add_argument('-p', '--project-token', help='Project / private token to auth with, env: ${PROJECT_TOKEN} by default')
    parser.add_argument('-t', '--timeout', type=int, default=20, help='Timeout (in minutes) to wait for dependent jobs to be ready')

    args = parser.parse_args()

    download(args.target, args.job, args.project_token, args.timeout)


if __name__ == "__main__":
    main()
