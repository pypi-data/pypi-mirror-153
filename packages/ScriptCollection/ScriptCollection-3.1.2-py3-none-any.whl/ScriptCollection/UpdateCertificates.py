import os
from pathlib import Path
import traceback
from shutil import copyfile
from .ScriptCollectionCore import ScriptCollectionCore
from .GeneralUtilities import GeneralUtilities


class CertificateUpdater:

    __domains: list(str)
    __email: str

    __current_folder = os.path.dirname(os.path.abspath(__file__))
    __repository_folder = GeneralUtilities.resolve_relative_path(f"..{os.path.sep}..{os.path.sep}..{os.path.sep}", __current_folder)
    __letsencrypt_folder = GeneralUtilities.resolve_relative_path(f"..{os.path.sep}..{os.path.sep}Volumes{os.path.sep}letsencrypt", __current_folder)
    __letsencrypt_live_folder = os.path.join(__letsencrypt_folder, "live")
    __letsencrypt_archive_folder = os.path.join(__letsencrypt_folder, "archive")
    __log_folder = GeneralUtilities.resolve_relative_path(f"Logs{os.path.sep}Overhead", __repository_folder)
    __sc = ScriptCollectionCore()
    __line = "___________________________________________________________________"

    def __init__(self, domains: list(str), email: str):
        self.__domains = domains
        self.__email = email

    @GeneralUtilities.check_arguments
    def __get_latest_index_by_domain(self, domain: str) -> int:
        result = self.__get_latest_index_by_filelist(GeneralUtilities.get_all_files_of_folder(os.path.join(self.__letsencrypt_archive_folder, domain)))
        GeneralUtilities.write_message_to_stdout(f"Debug: Latest found existing number for domain {domain}: {result}")
        return result

    @GeneralUtilities.check_arguments
    def __get_latest_index_by_filelist(self, filenames: list) -> int:
        print("files:")
        print(filenames)
        filenames = [Path(os.path.basename(file)).stem for file in filenames]
        print(filenames)
        filenames = [file for file in filenames if file.startswith("privkey")]
        print(filenames)
        numbers = [int(file[len("privkey"):]) for file in filenames]
        # numbers=[]
        #print([os.path.basename(file) for file in filenames])
        result = max(numbers)
        return result

    @GeneralUtilities.check_arguments
    def __replace_symlink_by_file(self, domain: str, filename: str, index: int) -> None:
        # ".../live/example.com/cert.pem" is a symlink but should replaced by a copy of ".../archive/example.com/cert.42pem"
        archive_file = os.path.join(self.__letsencrypt_archive_folder, domain, filename+str(index)+".pem")
        live_folder = os.path.join(self.__letsencrypt_live_folder, domain)
        live_filename = filename+".pem"
        live_file = os.path.join(live_folder, live_filename)
        self.__sc.run_program("rm", live_filename, live_folder)
        copyfile(archive_file, live_file)

    @GeneralUtilities.check_arguments
    def __replace_file_by_symlink(self, domain: str, filename: str, index: int) -> None:
        # new ".../live/example.com/cert.pem" is a file but should replaced by a symlink which points to ".../archive/example.com/cert42.pem"
        live_folder = os.path.join(self.__letsencrypt_live_folder, domain)
        live_filename = filename+".pem"
        self.__sc.run_program("rm", live_filename, live_folder)
        self.__sc.run_program("ln", f"-s ../../archive/{domain}/{filename+str(index)}.pem {live_filename}", live_folder)

    @GeneralUtilities.check_arguments
    def __replace_symlinks_by_files(self, domain):
        index = self.__get_latest_index_by_domain(domain)
        self.__replace_symlink_by_file(domain, "cert", index)
        self.__replace_symlink_by_file(domain, "chain", index)
        self.__replace_symlink_by_file(domain, "fullchain", index)
        self.__replace_symlink_by_file(domain, "privkey", index)

    @GeneralUtilities.check_arguments
    def __replace_files_by_symlinks(self, domain):
        index = self.__get_latest_index_by_domain(domain)
        self.__replace_file_by_symlink(domain, "cert", index)
        self.__replace_file_by_symlink(domain, "chain", index)
        self.__replace_file_by_symlink(domain, "fullchain", index)
        self.__replace_file_by_symlink(domain, "privkey", index)

    @GeneralUtilities.check_arguments
    def update_certificate_managed_by_docker_and_letsencrypt(self) -> None:
        GeneralUtilities.write_message_to_stdout("current_folder:")
        GeneralUtilities.write_message_to_stdout(self.__current_folder)
        GeneralUtilities.write_message_to_stdout("letsencrypt_folder:")
        GeneralUtilities.write_message_to_stdout(self.__letsencrypt_folder)
        GeneralUtilities.write_message_to_stdout("letsencrypt_live_folder:")
        GeneralUtilities.write_message_to_stdout(self.__letsencrypt_live_folder)
        GeneralUtilities.write_message_to_stdout("letsencrypt_archive_folder:")
        GeneralUtilities.write_message_to_stdout(self.__letsencrypt_archive_folder)
        GeneralUtilities.write_message_to_stdout("log_folder:")
        GeneralUtilities.write_message_to_stdout(self.__log_folder)

        GeneralUtilities.write_message_to_stdout(self.__line+self.__line)
        GeneralUtilities.write_message_to_stdout("Updating certificates")
        self.__sc.git_commit(self.__current_folder, "Saved current changes")
        for domain in self.__domains:
            try:
                GeneralUtilities.write_message_to_stdout(self.__line)
                GeneralUtilities.write_message_to_stdout(f"Process domain {domain}")
                certificate_for_domain_already_exists = os.path.isfile(f"{self.__letsencrypt_folder}/renewal/{domain}.conf")
                if certificate_for_domain_already_exists:
                    GeneralUtilities.write_message_to_stdout(f"Update certificate for domain {domain}")
                    self.__replace_files_by_symlinks(domain)
                else:
                    GeneralUtilities.write_message_to_stdout(f"Create certificate for domain {domain}")
                certbot_container_name = "r2_updatecertificates_certbot"
                dockerargument = f"run --name {certbot_container_name} --volume {self.__letsencrypt_folder}:/etc/letsencrypt"
                dockerargument = dockerargument+f" --volume {self.__log_folder}:/var/log/letsencrypt -p 80:80 certbot/certbot:latest"
                certbotargument = f"--standalone --email {self.__email} --agree-tos --force-renewal --rsa-key-size 4096 --non-interactive --no-eff-email --domain {domain}"
                if(certificate_for_domain_already_exists):
                    self.__sc.run_program("docker", f"{dockerargument} certonly --no-random-sleep-on-renew {certbotargument}",
                                                          self.__current_folder, throw_exception_if_exitcode_is_not_zero=True)
                    self.__replace_symlinks_by_files(domain)
                else:
                    self.__sc.run_program("docker", f"{dockerargument} certonly --cert-name {domain} {certbotargument}",
                                                          self.__current_folder, throw_exception_if_exitcode_is_not_zero=True)
            except Exception as exception:
                GeneralUtilities.write_exception_to_stderr_with_traceback(exception, traceback, "Error while updating certificate")
            finally:
                try:
                    self.__sc.run_program("docker", f"container rm {certbot_container_name}", self.__current_folder, throw_exception_if_exitcode_is_not_zero=True)
                except Exception as exception:
                    GeneralUtilities.write_exception_to_stderr_with_traceback(exception, traceback, "Error while removing container")

        GeneralUtilities.write_message_to_stdout("Commit changes...")
        self.__sc.git_commit(self.__repository_folder, "Executed certificate-update-process")
        GeneralUtilities.write_message_to_stdout("Finished certificate-update-process")
