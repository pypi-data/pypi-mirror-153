import traceback
from .GeneralUtilities import GeneralUtilities
from .ScriptCollectionCore import ScriptCollectionCore


class HardeningScript:

    __sc: ScriptCollectionCore = ScriptCollectionCore()
    __applicationstokeep: "list[str]" = None
    __additionalfolderstoremove: "list[str]" = None
    __applicationstodelete: "list[str]" = [
        "git", "curl", "wget", "sudo", "sendmail", "net-tools", "nano", "lsof", "tcpdump",
        "unattended-upgrades", "mlocate", "gpg", "htop", "netcat", "gcc-10", "gdb", "perl-modules-*",
        "binutils-common", "bash", "tar", "vi"
    ]

    def __init__(self, applicationstokeep, additionalfoldertoremove):
        self.__applicationstokeep = GeneralUtilities.to_list(applicationstokeep, ";")
        self.__additionalfolderstoremove = GeneralUtilities.to_list(additionalfoldertoremove, ";")

    @GeneralUtilities.check_arguments
    def run(self):
        try:
            GeneralUtilities.write_message_to_stdout("Hardening-configuration:")
            GeneralUtilities.write_message_to_stdout(f"  applicationstokeep: {self.__applicationstokeep}")
            GeneralUtilities.write_message_to_stdout(f"  additionalFolderToRemove: {self.__additionalfolderstoremove}")

            # TODO:
            # - kill applications which opens undesired ports
            # - generally disable root-login
            # - prevent creating/writing files using something like "echo x > y"
            # - prevent reading from files as much as possible
            # - prevent executing files as much as possible
            # - shrink rights of all user as much as possible
            # - deinstall/disable find, chown, chmod, apt etc. and all other applications which are not listed in $applicationstokeep
            # - disable unnecessary services/daemons if available (e. g. "systemctl disable avahi-daemon")
            # etc.
            # general idea: remove as much as possible from the file-system. all necessary binaries should already be available in the RAM usually.

            # Remove undesired folders
            for additionalfoldertoremove in self.__additionalfolderstoremove:
                GeneralUtilities.write_message_to_stdout(f"Remove folder {additionalfoldertoremove}...")
                GeneralUtilities.ensure_directory_does_not_exist(additionalfoldertoremove)

            # Remove undesired packages
            for applicationtodelete in self.__applicationstodelete:
                if not applicationtodelete in self.__applicationstokeep and self.__package_is_installed(applicationtodelete):
                    GeneralUtilities.write_message_to_stdout(f"Remove application {applicationtodelete}...")
                    self.__execute("apt-get", f"purge -y {applicationtodelete}")
        except Exception as exception:
            GeneralUtilities.write_exception_to_stderr_with_traceback(exception, traceback, "Exception occurred while hardening.")

    @GeneralUtilities.check_arguments
    def __package_is_installed(self, package: str) -> bool:
        return True  # TODO see https://askubuntu.com/questions/660305/how-to-tell-if-a-certain-package-exists-in-the-apt-repos

    @GeneralUtilities.check_arguments
    def __execute(self, program: str, argument: str, workding_directory: str = None):
        return self.__sc.run_program(program, argument, workding_directory)
