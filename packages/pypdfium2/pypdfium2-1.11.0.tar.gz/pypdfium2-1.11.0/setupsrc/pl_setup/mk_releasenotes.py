#! /usr/bin/env python3
# SPDX-FileCopyrightText: 2022 geisserml <geisserml@gmail.com>
# SPDX-License-Identifier: Apache-2.0 OR BSD-3-Clause

import sys
import shutil
from os.path import dirname, abspath, join

sys.path.insert(0, dirname(dirname(abspath(__file__))))
from pl_setup.packaging_base import SourceTree, run_cmd


Git = shutil.which('git')
RepositoryURL = 'https://github.com/pypdfium2-team/pypdfium2'


def run_default(command):
    return run_cmd(command, cwd=SourceTree, capture=True)

def get_url(tag):
    return RepositoryURL + '/tree/%s' % tag

def generate_tags_list():
    tags_str = run_default([Git, 'for-each-ref', '--sort=creatordate', '--format', '%(refname)', 'refs/tags'])
    tags_list = tags_str.split('\n')
    tags_list.reverse()
    return tags_list


def get_tag(TagsList, n_descends, skip_beta=False):
    
    i = 0
    for line in TagsList:
        tag = line.split('/')[-1].strip()
        if skip_beta and i > 0 and 'b' in tag:
            continue
        if i >= n_descends:
            break
        i += 1
    
    return tag


def main():
    
    TagsList = generate_tags_list()
    current_tag, prev_tag = get_tag(TagsList, 0), get_tag(TagsList, 1, True)
    print(current_tag, prev_tag)
    
    relnotes = "Release %s\n\n" % current_tag
    relnotes += "### Changes\n\nCommits between [`%s`](%s) and [`%s`](%s):\n\n" % (prev_tag, get_url(prev_tag), current_tag, get_url(current_tag))
    relnotes += run_default([Git, 'log', '%s..%s' % (prev_tag, current_tag), "--pretty=format:* %H %s"])
    relnotes += '\n'
    
    with open(join(SourceTree, 'RELEASE.md'), 'w') as fh:
        fh.write(relnotes)


if __name__ == '__main__':
    main()
