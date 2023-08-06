"""
Manages the version number for the project based on git tags.
If on a tag, report that as-is.
When moved on from the tag, auto-increment the desired level of semantic version
"""
import re
import os
import sys
import argparse
import setuptools
import subprocess
from pathlib import Path
import traceback


# Set environment variable "VERSION_INCREMENT" to set next version jump
VERSION_INCREMENT_ENV = "VERSION_INCREMENT"

PROJECT_ROOT_ENV = "PROJECT_ROOT"

VERSION_INCREMENT_PATCH = 'patch'
VERSION_INCREMENT_MINOR = 'minor'
VERSION_INCREMENT_MAJOR = 'major'

SUPPORT_PATCH = os.environ.get("VERSION_SUPPORT_PATCH", False)

repo_dir = os.environ.get(PROJECT_ROOT_ENV, '.')


VERBOSE = False


version = "UNKNOWN"
version_short = "0.0.0" if SUPPORT_PATCH else "0.0"
version_py = version_short
git_hash = ''
on_tag = False
dirty = True


try:
    from _version import version, version_short, git_hash, on_tag, dirty, SUPPORT_PATCH
except:
    pass


def vers_split(vers):
    try:
        return list(re.search(r"v?(\d+\.\d+(\.\d+)?)", vers).group(1).split('.'))
    except:
        print("Could not parse version from:", vers, file=sys.stderr)
        raise


def get_version_info_from_git():
    global SUPPORT_PATCH
    fail_ret = None, None, None, None
    # Note: git describe doesn't work if no tag is available
    current_commit = None
    try:
        current_commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"],
                                          cwd=repo_dir, stderr=subprocess.STDOUT, universal_newlines=True).strip()
        git_tag = subprocess.check_output(["git", "describe", "--long", "--tags", "--dirty", "--always"],
                                          cwd=repo_dir, stderr=subprocess.STDOUT, universal_newlines=True).strip()
    except subprocess.CalledProcessError as er:
        if VERBOSE:
            traceback.print_exc()
        if er.returncode == 128:
            # git exit code of 128 means no repository found
            return fail_ret
        git_tag = ""
    except OSError:
        if VERBOSE:
            traceback.print_exc()
        return fail_ret

    if git_tag.startswith(current_commit):
        # No tags yet, new repo
        git_hash = current_commit
        parts = re.match(r'(^[a-f0-9]*?)(-dirty)?$', git_tag.lower())
        git_dirty = parts.group(2)
        tag_name = ""
        if SUPPORT_PATCH:
            git_tag_parts = ['0', '0', '0']
        else:
            git_tag_parts = ['0', '0']
        on_tag = False

    else:
        parts = re.match(r'(^.*?)-(\d+)-g(.*?)(-dirty)?$', git_tag)
        tag_name = parts.group(1)
        num_commits = parts.group(2)
        git_hash = parts.group(3)
        git_dirty = parts.group(4)

        git_tag_parts = vers_split(git_tag)

        if len(git_tag_parts) == 3:
            SUPPORT_PATCH = True

        try:
            # Find all tags on the commit and get the largest version if there are multiple
            tag_sha = subprocess.check_output(["git", "rev-list", "-n", "1", tag_name],
                                              cwd=repo_dir, stderr=subprocess.STDOUT, universal_newlines=True).strip()

            sha_tags = subprocess.check_output(["git", "tag", "--contains", tag_sha],
                                               cwd=repo_dir, stderr=subprocess.STDOUT, universal_newlines=True).strip()

            sha_tags = [vers_split(t) for t in sha_tags.split('\n')]
            git_tag_parts = max(sha_tags)

        except subprocess.CalledProcessError as er:
            if VERBOSE:
                traceback.print_exc()

        except OSError:
            if VERBOSE:
                traceback.print_exc()
            return fail_ret

        try:
            on_tag = subprocess.check_output(["git", "describe", "--exact-match", "--tags", "HEAD"],
                                             cwd=repo_dir, stderr=subprocess.STDOUT, universal_newlines=True).strip()
        except subprocess.CalledProcessError:
            if VERBOSE:
                traceback.print_exc()
            on_tag = False
        except OSError:
            if VERBOSE:
                traceback.print_exc()
            return fail_ret

    if git_dirty:
        git_hash += "-dirty"

    return git_tag_parts, tag_name, git_hash, on_tag, git_dirty


def increment_index(increment):
    try:
        index = {
            VERSION_INCREMENT_PATCH: 2,
            VERSION_INCREMENT_MINOR: 1,
            VERSION_INCREMENT_MAJOR: 0,
        }[increment]
    except KeyError:
        raise SystemExit("change: %s must be one of '%s', '%s' or '%s'" %
                         (increment, VERSION_INCREMENT_MAJOR,
                          VERSION_INCREMENT_MINOR, VERSION_INCREMENT_PATCH))
    return index


def increment_from_messages(tag_name):
    # Increment version
    increment = []

    # Check git logs between last tag and now
    try:
        git_range = "%s..HEAD" % tag_name if tag_name else "HEAD"
        commit_messages = subprocess.check_output(["git", "log", git_range],
                                cwd=repo_dir, stderr=subprocess.STDOUT, universal_newlines=True).strip()
    except subprocess.CalledProcessError:
        commit_messages = ''

    for match in re.findall(r'CHANGE: *(%s|%s|%s)' % (
        VERSION_INCREMENT_MAJOR, VERSION_INCREMENT_MINOR, VERSION_INCREMENT_PATCH
    ), commit_messages):
        try:
            increment.append(increment_index(match))
        except SystemExit as ex:
            print(ex.args, file=sys.stderr)
    if increment:
        return min(increment)
    return None


def git_version():
    parts, tag_name, g_hash, on_tag, dirty = get_version_info_from_git()
    if not parts:
        raise ValueError("could not read git details")
    try:
        if not (on_tag and not dirty):

            index = increment_from_messages(tag_name)

            # Fallback to checking env for increment if commit messages don't specify
            if index is None:
                increment = os.environ.get(VERSION_INCREMENT_ENV, VERSION_INCREMENT_MINOR).lower()
                if len(parts) < 2:
                    if VERBOSE:
                        print("WARNING: Adding minor version to scheme that previously had none", file=sys.stderr)
                    parts.append('0')
                elif len(parts) < 3 and SUPPORT_PATCH:
                    if VERBOSE:
                        print("WARNING: Adding patch version to scheme that previously had none", file=sys.stderr)
                    parts.append('0')

                index = increment_index(increment)

            if index == increment_index(VERSION_INCREMENT_PATCH) and not SUPPORT_PATCH:
                raise SystemExit("Increment '%s' not currently supported" % VERSION_INCREMENT_PATCH)

            max_index = 2 if SUPPORT_PATCH else 1

            parts = parts[0:index] + [str(int(parts[index]) + 1)] + (['0'] * max(0, (max_index - index)))

    except (IndexError, ValueError, AttributeError) as ex:
        if "'NoneType' object has no attribute 'group'" in str(ex):  # regex fail
            print("Parsing version number failed:", tag_name, file=sys.stderr)
        else:
            print("Could not increment %s : %s" % (tag_name, ex), file=sys.stderr)

    vers_short = "v" + ".".join(parts)
    vers_long = vers_short + '-g' + g_hash
    return vers_short, vers_long, g_hash, on_tag, dirty


def py_version():
    global version
    def py_format(m):
        groups = m.groups()
        return f"{groups[0]}+{groups[2]}{'.dirty' if groups[3] else ''}"
    
    v = re.sub(r'v(\d+(\.\d)*)-(g.*?)(-dirty)?$', py_format, version)
    
    v_short = version_short.lstrip("v")

    if dirty:
        v += "+dirty"
        v_short += "+dirty"

    return v, v_short


def save():
    (Path(repo_dir) / '_version.py').write_text(
        '# Version managed by git-version\n'
        f'version = "{version}"\n'
        f'version_short = "{version_short}"\n'
        f'git_hash = "{git_hash}"\n'
        f'on_tag = {True if on_tag else False}\n'
        f'dirty = {True if dirty else False}\n'
        f'SUPPORT_PATCH = {True if SUPPORT_PATCH else False}\n'
    )


def rename_file(pattern, short):
    global version, version_short
    import glob
    for f in glob.glob(pattern):
        f = Path(f)
        newname = f.name.format(
            version=version,
            version_short=version_short,
            git_hash=git_hash,
        )
        if newname == f.name:
            name, ext = f.stem, f.suffix
            newname = f"{name}-{version_short if short else version}{ext}"
        print(f'Renaming "{f}" -> "{newname}"')
        f.rename(f.with_name(newname))


def fill_file(template_file, output_file):
    template_file = Path(template_file)
    output_file = Path(output_file)
    template = template_file.read_text()
    output = template.format(
            version=version,
            version_short=version_short,
            git_hash=git_hash,
        )
    output_file.write_text(output)
    print("Written:", output_file)


error = None
try:
    version_short, version, git_hash, on_tag, dirty = git_version()
    version_py, version_py_short = py_version()

except Exception as ex:
    error = str(ex)


def setup_keyword(dist: setuptools.Distribution, keyword, value):
    if not value:
        return

    dist.metadata.version = version_py

    if not isinstance(value, str):
        return

    if "desc" in value:
        # function can be run multiple times, ensure we only append once.
        if not dist.metadata.long_description.strip().endswith(version_py):
            dist.metadata.long_description += f"\n\nversion: {version_py}"

    if "gitlab" in value:
        # Long (PEP440 local) number schemes aren't allowed on PyPI
        # This scheme uses short version when building from default branch
        # or on tags.
        ci_commit_tag = os.environ.get("CI_COMMIT_TAG")
        if ci_commit_tag:
            dist.metadata.version = version_py_short
            return
        try:
            ci_commit_branch = os.environ.get("CI_COMMIT_BRANCH")
            ci_default_branch = os.environ["CI_DEFAULT_BRANCH"]
            if ci_commit_branch == ci_default_branch:
                dist.metadata.version = version_py_short
        except KeyError:
            # No env CI_DEFAULT_BRANCH, not running in Gitlab CI.
            pass
    
    elif "short" in value:
        dist.metadata.version = version_py_short


def main():
    global version, version_short, git_hash, on_tag, dirty, VERBOSE

    VERBOSE = True
    parser = argparse.ArgumentParser(description='Mange current/next version.')
    parser.add_argument('--save', action='store_true', help='Store in _version.py')
    parser.add_argument('--short', action='store_true', help='Print the short version string')
    parser.add_argument('--git', action='store_true', help='Print the release git hash')
    parser.add_argument('--rename', help='Add version numbers to filename(s)')
    parser.add_argument('--template', metavar=('template', 'output'), type=Path, nargs=2,
                        help='Add version to <template> and write result to <output>')
    parser.add_argument('--tag', action='store_true', help='Creates git tag to release the current commit')
    args = parser.parse_args()

    if error:
        try:
            version_short, version, git_hash, on_tag, dirty = git_version()
        except:
            import traceback
            traceback.print_exc()
    if args.save:
        save()

    if args.rename:
        rename_file(args.rename, args.short)
        return
    if args.template:
        fill_file(args.template[0], args.template[1])
        return

    if args.tag:
        if on_tag:
            raise SystemExit("Already on tag", on_tag)
        if dirty:
            raise SystemExit("Git dirty, cannot tag")
        print(version_short)
        subprocess.run(["git", "tag", version_short], cwd=repo_dir)

    if args.short:
        print(version_short)
    elif args.git:
        print(git_hash)
    else:
        print(version)


if __name__ == "__main__":
    main()
