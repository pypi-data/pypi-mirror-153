ARG BASE_WEB_BB_APP_IMAGE_NAME

FROM ${BASE_WEB_BB_APP_IMAGE_NAME}
MAINTAINER Danilenko Alexander

RUN pip3 install -r /srv/web_bb_app/requirements/stage.txt

# Patch pip to use --depth=1 with Git (shallow clones).
RUN sed -i "s/cls.run_command(\['clone', '-q', url, dest\])/cls.run_command(['clone', '--depth=1', '-b', rev_options.rev, '-q', url, dest])/g" /usr/local/lib/python3.9/site-packages/pip/_internal/vcs/git.py
