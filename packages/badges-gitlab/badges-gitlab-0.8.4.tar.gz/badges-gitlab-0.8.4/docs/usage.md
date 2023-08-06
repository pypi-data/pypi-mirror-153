# Usage 

## Common Usage

Install this package from pip and run it in your project folder.

```code
$ pip install badges-gitlab
$ badges-gitlab
```
This package was intended to be used in CI jobs, but if you want to test locally, you must point a 
folder with the json files in the format used by [shields.io endpoint](https://shields.io/endpoint),
otherwise it won't work because most of the badges uses the Gitlab API Token and CI Environment Variables.

## Continuous Integration Job

Below it is an example of a job running at the end of the pipeline in the default branch (main) 
and using cache for job optimization. Make sure to adequate your pipeline.

To ensure all possible badges are generated, include the [personal access token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) 
as an environment variable direct into the .gitlab-ci.yml or 
in the [CI/CD Variables configuration](https://docs.gitlab.com/ee/ci/variables/).

```yaml
badges:
  image: python:3.9
  stage: badges
  variables:
    PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
    PRIVATE_TOKEN: $ACCESS_TOKEN
  cache:
    key: badges
    paths:
      - .cache/pip
      - venv/
  before_script:
     - python -V        
     - pip install virtualenv
     - virtualenv venv
     - source venv/bin/activate
  script:
     - pip install badges-gitlab
     - badges-gitlab -V
     - badges-gitlab
  artifacts:
    when: always
    paths:
      - public/badges/*.svg
    expire_in: 3 months
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: always
      allow_failure: true
 ```

As the badges are generated only during this job, and if you want to make sure there are available for some 
time. So, adjust the expiration of the artifacts accordingly.

### Schedule Pipelines

Some badges have dynamic data and are generated only during this job, and the data can be outdated.
If you don't want to use third party APIs all the time to generate the badges (sometimes these APIs fail), you could use the 
[pipeline schedule](https://docs.gitlab.com/ee/ci/pipelines/schedules.html) 
function in conjunction with the rules option to run once a day as example.

```yaml
  rules:
    - if: '$CI_PIPELINE_SOURCE == "schedule"'
```

### Non compatible Python jobs

It is possible to use artifacts from previous jobs with information to generate new badges.

The json files must be "shields.io" compliant and located in the folder specified in the badges job 
(default: public/badges). Below is the accepted format.

```json
{
  "schemaVersion": 1,
  "label": "hello",
  "message": "sweet world",
  "color": "orange"
}
```

### Dockerfile Example

Alternatively, you can optimize even further the job building a docker image for this job and uploading
to [Gitlab Container Registry](https://docs.gitlab.com/ee/user/packages/container_registry).

```
FROM python:3.9-alpine

MAINTAINER foo@bar.com

RUN pip install badges-gitlab
```

## Using the Badges

This package seeks to use the post jobs availability of the artifacts 
[through links](https://docs.gitlab.com/ee/ci/pipelines/job_artifacts.html#access-the-latest-job-artifacts-by-url), 
which are described in Gitlab Documentation.

#### Gitlab Project Badges

You can insert using the project badges [Project Badges](https://docs.gitlab.com/ee/user/project/badges.html#badges).

Examples of a link for the project license in project badges section:

```
https://gitlab.com/%{project_path}/-/jobs/artifacts/%{default_branch}/raw/public/badges/license_name.svg?job=badges
```

### Readme

Other option is to use in the Readme file, through links. In Gitlab you can leverage the [relative links
feature](https://docs.gitlab.com/ee/user/markdown.html#links).

Example of a link in a markdown Readme.

```
![License](../-/jobs/artifacts/main/raw/public/badges/license_name.svg?job=badges)
```
# Configuration

It is now possible to configure this tool using pyproject.toml. 
Currently the parameters path, junit_xml, static_badges and link_badges are supported.
Example of pyproject.toml section:
```toml
[tool.badges_gitlab]
    path = "public/badges"
    junit_xml = "tests/report.xml"
    # List of Lists Format [["label", "message", "color"]]
    static_badges = [
        ["conventional commits", "1.0.0", "yellow"]
    ]
    # List of Links
    link_badges = [
        'https://img.shields.io/pypi/wheel/badges-gitlab'
    ]
```
Priority is:
- Command line parameters
- Toml file configuration

# Frequently Asked Questions

***Is this project for me?***

Although it is possible to generate badges with other API's such as [shields.io](http://shields.io), 
usually this process is not available in private repositories.

So if you are hosting a public project, this package is not specifically meant 
for you as you can workaround with other easier implementations. 

One good project to be consulted is from [@asdoi](https://gitlab.com/asdoi), available on
https://gitlab.com/asdoi/gitlab-badges and https://gitlab.com/asdoi/git_badges.

But, if you are hosting a private project and don't want to expose your project (Gitlab pages) 
or don't want to risk exposing your credentials (API Requests), maybe this project is for you.

Another reason would be to avoid overloading servers (e.g. shields.io) with unnecessary 
requests for (re)creating badges.

***How does it work?***

Some design choices were made to create this package.
1. The badges' generation were converted into two stages:
    - The first stage uses the Gitlab API (if the private-token turns out to be valid) to generate the json for some badges.
    - The second stage gets all the JSON files from the target folder and creates badges using anybadge.
2. These two stages have a purpose, if any other CI Pipeline job generates json files with their own data, you can also use these files to create badges.
3. The default directory is /public/badges:
    - This folder may be used later for Gitlab pages, although this can be modified through parameters.


