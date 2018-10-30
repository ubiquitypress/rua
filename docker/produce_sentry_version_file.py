#! /bin/python
# Produce a `sentry_version.ini` file from Bumpversion config and GIT SHA.

from configparser import ConfigParser
import os

import raven


BUILDBOT_PROJECT_FOLDER = '/buildbot/rua/build'

config = ConfigParser()
config.read('{base}/.bumpversion.cfg'.format(base=BUILDBOT_PROJECT_FOLDER))
current_version = config.get('bumpversion', 'current_version')


sentry_version = (
    '{main}-{sha}'.format(
        main=current_version,
        sha=raven.fetch_git_sha(
            os.path.join(
                '/',
                *os.path.dirname(
                    os.path.realpath(__file__)
                ).split('/')[:-1]
            )
        )
    )
)

version_file = open(
    '{base}/src/sentry_version.ini'.format(base=BUILDBOT_PROJECT_FOLDER),
    'w'
)
config.add_section('sentry')
config.set('sentry', 'version', sentry_version)
config.write(version_file)
version_file.close()
