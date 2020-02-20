"""
Semantic version tag generator
"""

import semver


def increment_maker(current_semver, bump_type):
    """
    Takes in strings for the current version and the desired version bump
    Returns an updated string that complies with semantic versioning with given bump
    """
    d = {
        "major": semver.bump_major,
        "minor": semver.bump_minor,
        "patch": semver.bump_patch,
    }
    new_semver = d[bump_type](current_semver)

    return new_semver


def tag_gen(current_tag, bump_type):
    """
    Takes current tag and desired bump, returns new tag
    """
    current_semver = current_tag[1:]  # Trim off the 'v'
    new_semver = increment_maker(current_semver, bump_type)
    new_tag = f"v{new_semver}"

    return new_tag


if __name__ == "__main__":
    t = tag_gen("v9.3.2", "major")
    print(t)
