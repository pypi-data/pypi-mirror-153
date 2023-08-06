APPLICATION_VERSION = "1.0.0-alpha.11"
# [Semantic versioning](semver.org) is used, and we may also add `dev` at the end of the version
# Example: `1.2.3-alpha.4-dev.5`

APPLICATION_PRETTY_NAME = "Mindfulness at the Computer"
APPLICATION_NAME = "mindfulness-at-the-computer"
SHORT_DESCR_STR = "Helps you stay mindful of your breathing while using your computer."

# The following is used in the makefile for automatically naming the archive file:
if __name__ == "__main__":
    print(APPLICATION_VERSION)
