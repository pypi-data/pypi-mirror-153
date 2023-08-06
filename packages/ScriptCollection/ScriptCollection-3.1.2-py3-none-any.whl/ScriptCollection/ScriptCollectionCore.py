from datetime import timedelta, datetime
import binascii
from configparser import ConfigParser
import filecmp
import hashlib
from io import BytesIO
import itertools
import math
import os
from pathlib import Path
from random import randrange
from subprocess import Popen
import re
import shutil
import traceback
import uuid
import ntplib
from lxml import etree
import pycdlib
import send2trash
from PyPDF2 import PdfFileMerger

from .GeneralUtilities import GeneralUtilities
from .ProgramRunnerPopen import ProgramRunnerPopen
from .ProgramRunnerBase import ProgramRunnerBase
from .ProgramRunnerEpew import ProgramRunnerEpew, CustomEpewArgument


version = "3.1.2"
__version__ = version


class ScriptCollectionCore:

    # The purpose of this property is to use it when testing your code which uses scriptcollection for external program-calls.
    # Do not change this value for productive environments.
    mock_program_calls: bool = False
    # The purpose of this property is to use it when testing your code which uses scriptcollection for external program-calls.
    execute_program_really_if_no_mock_call_is_defined: bool = False
    __mocked_program_calls: list = list()
    program_runner: ProgramRunnerBase = None

    def __init__(self):
        self.program_runner = ProgramRunnerPopen()

    @staticmethod
    @GeneralUtilities.check_arguments
    def get_scriptcollection_version() -> str:
        return __version__

    @GeneralUtilities.check_arguments
    def create_release(self, configurationfile: str) -> int:  # obsolete
        # TODO remove this function and all its child-functions which are unused then
        error_occurred = False
        try:
            current_release_information: dict[str, str] = {}
            configparser = ConfigParser()
            with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
                configparser.read_file(text_io_wrapper)

            repository = self.get_item_from_configuration(configparser, "general", "repository", current_release_information)
            releaserepository = self.get_item_from_configuration(configparser, "other", "releaserepository", current_release_information)

            if (self.__repository_has_changes(repository) or self.__repository_has_changes(releaserepository)):
                return 1

            srcbranch = self.get_item_from_configuration(configparser, 'prepare', 'sourcebranchname', current_release_information)
            trgbranch = self.get_item_from_configuration(configparser, 'prepare', 'targetbranchname', current_release_information)
            commitid = self.git_get_current_commit_id(repository, trgbranch)

            if(commitid == self.git_get_current_commit_id(repository, srcbranch)):
                GeneralUtilities.write_message_to_stderr(
                    f"Can not create release because the main-branch and the development-branch are on the same commit (commit-id: {commitid})")
                return 1

            self.git_checkout(repository, srcbranch)
            self.run_program("git", "clean -dfx", repository, throw_exception_if_exitcode_is_not_zero=True)
            self.__calculate_version(configparser, current_release_information)
            repository_version = self.get_version_for_buildscripts(configparser, current_release_information)

            GeneralUtilities.write_message_to_stdout(f"Create release v{repository_version} for repository {repository}")
            self.git_merge(repository, srcbranch, trgbranch, False, False)

            try:
                if self.get_boolean_value_from_configuration(configparser, 'general', 'createdotnetrelease', current_release_information) and not error_occurred:
                    GeneralUtilities.write_message_to_stdout("Start to create .NET-release")
                    error_occurred = not self.__execute_and_return_boolean("create_dotnet_release",
                                                                           lambda: self.__create_dotnet_release_premerge(
                                                                               configurationfile, current_release_information))

                if self.get_boolean_value_from_configuration(configparser, 'general', 'createpythonrelease', current_release_information) and not error_occurred:
                    GeneralUtilities.write_message_to_stdout("Start to create Python-release")
                    error_occurred = not self.__execute_and_return_boolean("python_create_wheel_release",
                                                                           lambda: self.python_create_wheel_release_premerge(
                                                                               configurationfile, current_release_information))

                if self.get_boolean_value_from_configuration(configparser, 'general', 'createdebrelease', current_release_information) and not error_occurred:
                    GeneralUtilities.write_message_to_stdout("Start to create Deb-release")
                    error_occurred = not self.__execute_and_return_boolean("deb_create_installer_release",
                                                                           lambda: self.deb_create_installer_release_premerge(
                                                                               configurationfile, current_release_information))

                if self.get_boolean_value_from_configuration(configparser, 'general', 'createdockerrelease', current_release_information) and not error_occurred:
                    GeneralUtilities.write_message_to_stdout("Start to create docker-release")
                    error_occurred = not self.__execute_and_return_boolean("docker_create_installer_release",
                                                                           lambda: self.docker_create_image_release_premerge(
                                                                               configurationfile, current_release_information))

                if self.get_boolean_value_from_configuration(configparser, 'general', 'createflutterandroidrelease', current_release_information) and not error_occurred:
                    GeneralUtilities.write_message_to_stdout("Start to create FlutterAndroid-release")
                    error_occurred = not self.__execute_and_return_boolean("flutterandroid_create_installer_release",
                                                                           lambda: self.flutterandroid_create_installer_release_premerge(
                                                                               configurationfile, current_release_information))

                if self.get_boolean_value_from_configuration(configparser, 'general', 'createflutteriosrelease', current_release_information) and not error_occurred:
                    GeneralUtilities.write_message_to_stdout("Start to create FlutterIOS-release")
                    error_occurred = not self.__execute_and_return_boolean("flutterios_create_installer_release",
                                                                           lambda: self.flutterios_create_installer_release_premerge(
                                                                               configurationfile, current_release_information))

                if self.get_boolean_value_from_configuration(configparser, 'general', 'createscriptrelease', current_release_information) and not error_occurred:
                    GeneralUtilities.write_message_to_stdout("Start to create Script-release")
                    error_occurred = not self.__execute_and_return_boolean("generic_create_installer_release",
                                                                           lambda: self.generic_create_script_release_premerge(
                                                                               configurationfile, current_release_information))

                if not error_occurred:
                    commit_id = self.git_commit(
                        repository, f"Merge branch '{self.get_item_from_configuration(configparser, 'prepare', 'sourcebranchname',current_release_information)}' "
                        f"into '{self.get_item_from_configuration(configparser, 'prepare', 'targetbranchname',current_release_information)}'")
                    current_release_information["builtin.mergecommitid"] = commit_id

                    # TODO allow multiple custom pre- (and post)-build-regex-replacements for files specified by glob-pattern
                    # (like "!\[Generic\ badge\]\(https://img\.shields\.io/badge/coverage\-\d(\d)?%25\-green\)"
                    # -> "![Generic badge](https://img.shields.io/badge/coverage-__testcoverage__%25-green)" in all "**/*.md"-files)

                    if self.get_boolean_value_from_configuration(configparser, 'general', 'createdotnetrelease', current_release_information) and not error_occurred:
                        GeneralUtilities.write_message_to_stdout("Start to create .NET-release")
                        error_occurred = not self.__execute_and_return_boolean("create_dotnet_release",
                                                                               lambda: self.__create_dotnet_release_postmerge(
                                                                                   configurationfile, current_release_information))

                    if self.get_boolean_value_from_configuration(configparser, 'general', 'createpythonrelease', current_release_information) and not error_occurred:
                        GeneralUtilities.write_message_to_stdout("Start to create Python-release")
                        error_occurred = not self.__execute_and_return_boolean("python_create_wheel_release",
                                                                               lambda: self.python_create_wheel_release_postmerge(
                                                                                   configurationfile, current_release_information))

                    if self.get_boolean_value_from_configuration(configparser, 'general', 'createdebrelease', current_release_information) and not error_occurred:
                        GeneralUtilities.write_message_to_stdout("Start to create Deb-release")
                        error_occurred = not self.__execute_and_return_boolean("deb_create_installer_release",
                                                                               lambda: self.deb_create_installer_release_postmerge(
                                                                                   configurationfile, current_release_information))

                    if self.get_boolean_value_from_configuration(configparser, 'general', 'createdockerrelease', current_release_information) and not error_occurred:
                        GeneralUtilities.write_message_to_stdout("Start to create docker-release")
                        error_occurred = not self.__execute_and_return_boolean("docker_create_installer_release",
                                                                               lambda: self.docker_create_image_release_postmerge(configurationfile,
                                                                                                                                  current_release_information))

                    if self.get_boolean_value_from_configuration(configparser, 'general', 'createflutterandroidrelease', current_release_information) and not error_occurred:
                        GeneralUtilities.write_message_to_stdout("Start to create FlutterAndroid-release")
                        error_occurred = not self.__execute_and_return_boolean("flutterandroid_create_installer_release",
                                                                               lambda: self.flutterandroid_create_installer_release_postmerge(configurationfile,
                                                                                                                                              current_release_information))

                    if self.get_boolean_value_from_configuration(configparser, 'general', 'createflutteriosrelease', current_release_information) and not error_occurred:
                        GeneralUtilities.write_message_to_stdout("Start to create FlutterIOS-release")
                        error_occurred = not self.__execute_and_return_boolean("flutterios_create_installer_release",
                                                                               lambda: self.flutterios_create_installer_release_postmerge(configurationfile,
                                                                                                                                          current_release_information))

                    if self.get_boolean_value_from_configuration(configparser, 'general', 'createscriptrelease', current_release_information) and not error_occurred:
                        GeneralUtilities.write_message_to_stdout("Start to create Script-release")
                        error_occurred = not self.__execute_and_return_boolean("generic_create_installer_release",
                                                                               lambda: self.generic_create_script_release_postmerge(
                                                                                   configurationfile, current_release_information))

            except Exception as exception:
                error_occurred = True
                GeneralUtilities.write_exception_to_stderr_with_traceback(exception, traceback, f"Error occurred while creating release defined by '{configurationfile}'.")

            finally:
                GeneralUtilities.write_message_to_stdout("Finished to create release")

            if error_occurred:
                GeneralUtilities.write_message_to_stderr("Creating release was not successful")
                self.git_merge_abort(repository)
                self.__undo_changes(repository)
                self.__undo_changes(releaserepository)
                self.git_checkout(repository, self.get_item_from_configuration(configparser, 'prepare', 'sourcebranchname', current_release_information))
                return 1
            else:
                self.git_merge(repository, self.get_item_from_configuration(configparser, 'prepare', 'targetbranchname', current_release_information),
                               self.get_item_from_configuration(configparser, 'prepare', 'sourcebranchname', current_release_information), True)
                tag = self.get_item_from_configuration(configparser, 'prepare', 'gittagprefix', current_release_information) + repository_version
                tag_message = f"Created {tag}"
                self.git_create_tag(repository, commit_id,
                                    tag, self.get_boolean_value_from_configuration(configparser, 'other', 'signtags', current_release_information), tag_message)
                self.__push_branch_of_release(configparser, current_release_information, repository,
                                              self.get_boolean_value_from_configuration(configparser, 'other', 'exportrepositorysourcebranch', current_release_information),
                                              self.get_item_from_configuration(configparser, 'prepare', 'sourcebranchname', current_release_information))
                self.__push_branch_of_release(configparser, current_release_information, repository,
                                              self.get_boolean_value_from_configuration(configparser, 'other', 'exportrepositorytargetbranch', current_release_information),
                                              self.get_item_from_configuration(configparser, 'prepare', 'targetbranchname', current_release_information))
                GeneralUtilities.write_message_to_stdout("Creating release was successful")
                return 0

        except Exception as e:
            GeneralUtilities.write_exception_to_stderr_with_traceback(e, traceback, f"Fatal error occurred while creating release defined by '{configurationfile}'.")
            return 1

    @GeneralUtilities.check_arguments
    def __push_branch_of_release(self, configparser: ConfigParser, current_release_information: dict[str, str], repository: str, export: bool, branch: str):
        if export:
            self.git_push(repository, self.get_item_from_configuration(configparser, 'other',
                                                                       'exportrepositoryremotename', current_release_information), branch, branch, False, True)

    @GeneralUtilities.check_arguments
    def python_file_has_errors(self, file: str, working_directory: str, treat_warnings_as_errors: bool = True) -> tuple[bool, list[str]]:
        errors = list()
        filename = os.path.relpath(file, working_directory)
        if treat_warnings_as_errors:
            errorsonly_argument = ""
        else:
            errorsonly_argument = " --errors-only"
        (exit_code, stdout, stderr, _) = self.run_program("pylint", filename+errorsonly_argument, working_directory, throw_exception_if_exitcode_is_not_zero=False)
        if(exit_code != 0):
            errors.append(f"Linting-issues of {file}:")
            errors.append(f"Pylint-exitcode: {exit_code}")
            for line in GeneralUtilities.string_to_lines(stdout):
                errors.append(line)
            for line in GeneralUtilities.string_to_lines(stderr):
                errors.append(line)
            return (True, errors)

        return (False, errors)

    class MergeToStableBranchInformationForProjectInCommonProjectFormat:
        project_has_source_code: bool = True
        repository: str
        sourcebranch: str = "main"
        targetbranch: str = "stable"
        run_build_py: bool = True
        build_py_arguments: str = ""
        sign_git_tags: bool = True

        push_source_branch: bool = False
        push_source_branch_remote_name: str = None  # This value will be ignored if push_source_branch = False

        merge_target_as_fast_forward_into_source_after_merge: bool = True
        push_target_branch: bool = False  # This value will be ignored if merge_target_as_fast_forward_into_source_after_merge = False
        push_target_branch_remote_name: str = None  # This value will be ignored if or merge_target_as_fast_forward_into_source_after_merge push_target_branch = False

        verbosity: int = 1

        def __init__(self, repository: str):
            self.repository = repository

    class CreateReleaseInformationForProjectInCommonProjectFormat:
        projectname: str
        repository: str
        build_artifacts_target_folder: str
        build_py_arguments: str = ""
        verbosity: int = 1
        push_artifact_to_registry_scripts: dict[str, str] = dict[str, str]()  # key: codeunit, value: scriptfile for pushing codeunit's artifact to one or more registries
        reference_repository: str = None
        public_repository_url: str = None
        target_branch_name: str = None

        def __init__(self, repository: str, build_artifacts_target_folder: str, projectname: str, public_repository_url: str, target_branch_name: str):
            self.repository = repository
            self.public_repository_url = public_repository_url
            self.target_branch_name = target_branch_name
            self.build_artifacts_target_folder = build_artifacts_target_folder
            if projectname is None:
                projectname = os.path.basename(self.repository)
            else:
                self.projectname = projectname
            self.reference_repository = GeneralUtilities.resolve_relative_path(f"../{projectname}Reference", repository)

    @GeneralUtilities.check_arguments
    def get_code_units_of_repository_in_common_project_format(self, repository_folder: str) -> list[str]:
        result = []
        for direct_subfolder in GeneralUtilities.get_direct_folders_of_folder(repository_folder):
            subfolder_name = os.path.basename(direct_subfolder)
            if os.path.isfile(os.path.join(direct_subfolder, subfolder_name+".codeunit")):
                # TODO validate .codeunit file against appropriate xsd-file
                result.append(subfolder_name)
        return result

    @GeneralUtilities.check_arguments
    def __get_testcoverage_threshold_from_codeunit_file(self, codeunit_file):
        root: etree._ElementTree = etree.parse(codeunit_file)
        return float(str(root.xpath('//codeunit:minimalcodecoverageinpercent/text()', namespaces={'codeunit': 'https://github.com/anionDev/ProjectTemplates'})[0]))

    @GeneralUtilities.check_arguments
    def check_testcoverage(self, testcoverage_file_in_cobertura_format: str, threshold_in_percent: float):
        root: etree._ElementTree = etree.parse(testcoverage_file_in_cobertura_format)
        coverage_in_percent = round(float(str(root.xpath('//coverage/@line-rate')[0]))*100, 2)
        minimalrequiredtestcoverageinpercent = threshold_in_percent
        if(coverage_in_percent < minimalrequiredtestcoverageinpercent):
            raise ValueError(f"The testcoverage must be {minimalrequiredtestcoverageinpercent}% or more but is {coverage_in_percent}%.")

    @GeneralUtilities.check_arguments
    def create_release_starter_for_repository_in_standardized_format(self, create_release_file: str, logfile=None, verbosity: int = 1):
        folder_of_this_file = os.path.dirname(create_release_file)
        self.run_program("python.py", "CreateRelease.py", folder_of_this_file, verbosity, log_file=logfile)

    @GeneralUtilities.check_arguments
    def standardized_tasks_merge_to_stable_branch_for_project_in_common_project_format(self, information: MergeToStableBranchInformationForProjectInCommonProjectFormat) -> str:

        src_branch_commit_id = self.git_get_current_commit_id(information.repository,  information.sourcebranch)
        if(src_branch_commit_id == self.git_get_current_commit_id(information.repository,  information.targetbranch)):
            GeneralUtilities.write_message_to_stderr(
                f"Can not merge because the source-branch and the target-branch are on the same commit (commit-id: {src_branch_commit_id})")

        self.git_checkout(information.repository, information.sourcebranch)
        self.run_program("git", "clean -dfx", information.repository, throw_exception_if_exitcode_is_not_zero=True)
        project_version = self.get_semver_version_from_gitversion(information.repository)
        self.git_merge(information.repository, information.sourcebranch, information.targetbranch, False, False)
        success = False
        try:
            for codeunitname in self.get_code_units_of_repository_in_common_project_format(information.repository):
                GeneralUtilities.write_message_to_stdout(f"Process codeunit {codeunitname}")

                common_tasks_file: str = "CommonTasks.py"
                common_tasks_folder: str = os.path.join(information.repository, codeunitname, "Other")
                if os.path.isfile(os.path.join(common_tasks_folder, common_tasks_file)):
                    GeneralUtilities.write_message_to_stdout("Do common tasks")
                    self.run_program("python", f"{common_tasks_file} --projectversion={project_version}", common_tasks_folder, verbosity=information.verbosity)

                if information.project_has_source_code:
                    GeneralUtilities.write_message_to_stdout("Run testcases")
                    qualityfolder = os.path.join(information.repository, codeunitname, "Other", "QualityCheck")
                    self.run_program("python", "RunTestcases.py", qualityfolder, verbosity=information.verbosity)
                    self.check_testcoverage(os.path.join(information.repository, codeunitname, "Other", "QualityCheck", "TestCoverage", "TestCoverage.xml"),
                                            self.__get_testcoverage_threshold_from_codeunit_file(os.path.join(information.repository, codeunitname, f"{codeunitname}.codeunit")))

                    GeneralUtilities.write_message_to_stdout("Check linting")
                    self.run_program("python", "Linting.py", os.path.join(information.repository, codeunitname, "Other", "QualityCheck"), verbosity=information.verbosity)

                    GeneralUtilities.write_message_to_stdout("Generate reference")
                    self.run_program("python", "GenerateReference.py", os.path.join(information.repository, codeunitname, "Other", "Reference"), verbosity=information.verbosity)

                    if information.run_build_py:
                        # only as test to ensure building works before the merge will be committed
                        GeneralUtilities.write_message_to_stdout("Building")
                        codeunit_folder = os.path.join(information.repository, codeunitname)
                        codeunit_version = self.get_version_of_codeunit(os.path.join(codeunit_folder, f"{codeunitname}.codeunit"))
                        commitid = self.git_get_current_commit_id(information.repository)
                        self.__run_build_py(commitid, codeunit_version, information.build_py_arguments, information.repository, codeunitname, information.verbosity)

            commit_id = self.git_commit(information.repository,  f"Created release v{project_version}")
            success = True
        except Exception as exception:
            GeneralUtilities.write_exception_to_stderr(exception, "Error while doing merge-tasks. Merge will be aborted.")
            self.git_merge_abort(information.repository)
            self.git_checkout(information.repository, information.sourcebranch)

        if not success:
            raise Exception("Release was not successful.")

        self.git_create_tag(information.repository, commit_id, f"v{project_version}", information.sign_git_tags)

        if information.push_target_branch:
            GeneralUtilities.write_message_to_stdout("Push target-branch")
            self.git_push(information.repository, information.push_target_branch_remote_name,
                          information.targetbranch, information.targetbranch, pushalltags=True, verbosity=False)

        if information.merge_target_as_fast_forward_into_source_after_merge:
            self.git_merge(information.repository, information.targetbranch, information.sourcebranch, True, True)
            if information.push_source_branch:
                GeneralUtilities.write_message_to_stdout("Push source-branch")
                self.git_push(information.repository, information.push_source_branch_remote_name, information.sourcebranch,
                              information.sourcebranch, pushalltags=False, verbosity=information.verbosity)
        return project_version

    def __run_build_py(self, commitid, codeunit_version, build_py_arguments, repository, codeunitname, verbosity):
        self.run_program("python", f"Build.py --commitid={commitid} --codeunitversion={codeunit_version} {build_py_arguments}", os.path.join(repository, codeunitname, "Other", "Build"),
                         verbosity=verbosity)

    @GeneralUtilities.check_arguments
    def standardized_tasks_release_buildartifact_for_project_in_common_project_format(self, information: CreateReleaseInformationForProjectInCommonProjectFormat) -> None:
        # This function is intended to be called directly after standardized_tasks_merge_to_stable_branch_for_project_in_common_project_format

        project_version = self.get_semver_version_from_gitversion(information.repository)
        target_folder_base = os.path.join(information.build_artifacts_target_folder, information.projectname, project_version)
        if os.path.isdir(target_folder_base):
            raise ValueError(f"The folder '{target_folder_base}' already exists.")
        GeneralUtilities.ensure_directory_exists(target_folder_base)
        commitid = self.git_get_current_commit_id(information.repository)
        codeunits = self.get_code_units_of_repository_in_common_project_format(information.repository)

        for codeunitname in codeunits:
            codeunit_folder = os.path.join(information.repository, codeunitname)
            codeunit_version = self.get_version_of_codeunit(os.path.join(codeunit_folder, f"{codeunitname}.codeunit"))
            self.__run_build_py(commitid, codeunit_version, information.build_py_arguments, information.repository, codeunitname, information.verbosity)

        reference_repository_target_for_project = os.path.join(information.reference_repository, "ReferenceContent")

        for codeunitname in codeunits:
            codeunit_folder = os.path.join(information.repository, codeunitname)
            codeunit_version = self.get_version_of_codeunit(os.path.join(codeunit_folder, f"{codeunitname}.codeunit"))

            target_folder_for_codeunit = os.path.join(target_folder_base, codeunitname)
            GeneralUtilities.ensure_directory_exists(target_folder_for_codeunit)
            shutil.copyfile(os.path.join(information.repository, codeunitname, f"{codeunitname}.codeunit"), os.path.join(target_folder_for_codeunit, f"{codeunitname}.codeunit"))

            target_folder_for_codeunit_buildartifact = os.path.join(target_folder_for_codeunit, "BuildArtifact")
            shutil.copytree(os.path.join(codeunit_folder, "Other", "Build", "BuildArtifact"), target_folder_for_codeunit_buildartifact)

            target_folder_for_codeunit_testcoveragereport = os.path.join(target_folder_for_codeunit, "TestCoverageReport")
            shutil.copytree(os.path.join(codeunit_folder, "Other", "QualityCheck", "TestCoverage", "TestCoverageReport"), target_folder_for_codeunit_testcoveragereport)

            target_folder_for_codeunit_generatedreference = os.path.join(target_folder_for_codeunit, "GeneratedReference")
            shutil.copytree(os.path.join(codeunit_folder, "Other", "Reference", "GeneratedReference"), target_folder_for_codeunit_generatedreference)

            if codeunitname in information.push_artifact_to_registry_scripts:
                push_artifact_to_registry_script = information.push_artifact_to_registry_scripts[codeunitname]
                folder = os.path.dirname(push_artifact_to_registry_script)
                file = os.path.basename(push_artifact_to_registry_script)
                self.run_program("python", file, folder, verbosity=information.verbosity, throw_exception_if_exitcode_is_not_zero=True)

            # Copy reference of codeunit to reference-repository
            self.__export_codeunit_reference_content_to_reference_repository(f"v{project_version}", False, reference_repository_target_for_project, information.repository,
                                                                             codeunitname, information.projectname, codeunit_version, information.public_repository_url,
                                                                             information.target_branch_name)
            self.__export_codeunit_reference_content_to_reference_repository("Latest", True, reference_repository_target_for_project, information.repository,
                                                                             codeunitname, information.projectname,  codeunit_version, information.public_repository_url,
                                                                             information.target_branch_name)

        all_available_version_identifier_folders_of_reference = list(folder for folder in GeneralUtilities.get_direct_folders_of_folder(reference_repository_target_for_project))
        all_available_version_identifier_folders_of_reference.reverse()  # move newer versions above
        all_available_version_identifier_folders_of_reference.insert(0, all_available_version_identifier_folders_of_reference.pop())  # move latest version to the top
        reference_versions_html_lines = []
        for all_available_version_identifier_folder_of_reference in all_available_version_identifier_folders_of_reference:
            version_identifier_of_project = os.path.basename(all_available_version_identifier_folder_of_reference)
            if version_identifier_of_project == "Latest":
                latest_version_hint = f" (v {project_version})"
            else:
                latest_version_hint = ""
            reference_versions_html_lines.append(f"<h2>{version_identifier_of_project}{latest_version_hint}</h2>")
            reference_versions_html_lines.append("Contained codeunits:<br>")
            reference_versions_html_lines.append("<ul>")
            for codeunit_reference_folder in list(folder for folder in GeneralUtilities.get_direct_folders_of_folder(all_available_version_identifier_folder_of_reference)):
                codeunit_folder = os.path.join(information.repository, codeunitname)
                codeunit_version = self.get_version_of_codeunit(os.path.join(codeunit_folder, f"{codeunitname}.codeunit"))
                reference_versions_html_lines.append(f'<li><a href="./{version_identifier_of_project}/{os.path.basename(codeunit_reference_folder)}/index.html">'
                                                     f'{os.path.basename(codeunit_reference_folder)} v{version_identifier_of_project}</a></li>')
            reference_versions_html_lines.append("</ul>")

        reference_versions_links_file_content = "    \n".join(reference_versions_html_lines)
        title = f"{information.projectname}-reference"
        reference_index_file = os.path.join(reference_repository_target_for_project, "index.html")
        reference_index_file_content = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>

<body>
    <h1>{title}</h1>
    {reference_versions_links_file_content}
</body>

</html>
"""
        GeneralUtilities.write_text_to_file(reference_index_file, reference_index_file_content)

    def replace_version_in_python_file(self, file: str, new_version_value: str):
        GeneralUtilities.write_text_to_file(file, re.sub("version = \"\\d+\\.\\d+\\.\\d+\"", f"version = \"{new_version_value}\"",
                                                         GeneralUtilities.read_text_from_file(file)))

    def __export_codeunit_reference_content_to_reference_repository(self, project_version_identifier: str, replace_existing_content: bool, target_folder_for_reference_repository: str,
                                                                    repository: str, codeunitname, projectname: str, codeunit_version: str, public_repository_url: str, branch: str) -> None:

        target_folder = os.path.join(target_folder_for_reference_repository, project_version_identifier, codeunitname)
        if os.path.isdir(target_folder) and not replace_existing_content:
            raise ValueError(f"Folder '{target_folder}' already exists.")

        GeneralUtilities.ensure_directory_does_not_exist(target_folder)
        GeneralUtilities.ensure_directory_exists(target_folder)
        title = f"{codeunitname}-reference (codeunit v{codeunit_version}, conained in project {projectname} ({project_version_identifier}))"

        if public_repository_url is None:
            repo_url_html = ""
        else:
            repo_url_html = f'<a href="{public_repository_url}/tree/{branch}/{codeunitname}">Source-code</a><br>'

        index_file_for_reference = os.path.join(target_folder, "index.html")
        index_file_content = f"""<!DOCTYPE html>
<html lang="en">

  <head>
    <meta charset="UTF-8">
    <title>{title}</title>
  </head>

  <body>
    <h1>{title}</h1>
    Available reference-content for {codeunitname}:<br>
    {repo_url_html}
    <a href="./GeneratedReference/index.html">Refrerence</a><br>
    <a href="./TestCoverageReport/index.html">TestCoverageReport</a><br>
  </body>

</html>
"""
        GeneralUtilities.ensure_file_exists(index_file_for_reference)
        GeneralUtilities.write_text_to_file(index_file_for_reference, index_file_content)

        other_folder_in_repository = os.path.join(repository, codeunitname, "Other")

        source_generatedreference = os.path.join(other_folder_in_repository, "Reference", "GeneratedReference")
        target_generatedreference = os.path.join(target_folder, "GeneratedReference")
        shutil.copytree(source_generatedreference, target_generatedreference)

        source_testcoveragereport = os.path.join(other_folder_in_repository, "QualityCheck", "TestCoverage", "TestCoverageReport")
        target_testcoveragereport = os.path.join(target_folder, "TestCoverageReport")
        shutil.copytree(source_testcoveragereport, target_testcoveragereport)

    def getversion_from_arguments_or_gitversion(self, common_tasks_file: str, commandline_arguments: list[str]) -> None:
        current_version: str = None
        for commandline_argument in commandline_arguments:
            if commandline_argument.startswith("--projectversion="):
                current_version = commandline_argument.split("=")[1]
        if current_version is None:
            current_version = self.get_semver_version_from_gitversion(GeneralUtilities.resolve_relative_path("../..", os.path.dirname(common_tasks_file)))
        return current_version

    def update_version_of_codeunit_to_project_version(self, common_tasks_file: str, current_version: str) -> None:
        codeunit_name: str = os.path.basename(GeneralUtilities.resolve_relative_path("..", os.path.dirname(common_tasks_file)))
        codeunit_file: str = os.path.join(GeneralUtilities.resolve_relative_path("..", os.path.dirname(common_tasks_file)), f"{codeunit_name}.codeunit")
        self.write_version_to_codeunit_file(codeunit_file, current_version)

    def get_version_of_codeunit(self, codeunit_file: str) -> None:
        root: etree._ElementTree = etree.parse(codeunit_file)
        result = str(root.xpath('//codeunit:version/text()', namespaces={'codeunit': 'https://github.com/anionDev/ProjectTemplates'})[0])
        return result

    def write_version_to_codeunit_file(self, codeunit_file: str, current_version: str) -> None:
        versionregex = "\\d+\\.\\d+\\.\\d+"
        versiononlyregex = f"^{versionregex}$"
        pattern = re.compile(versiononlyregex)
        if pattern.match(current_version):
            GeneralUtilities.write_text_to_file(codeunit_file, re.sub(f"<codeunit:version>{versionregex}<\\/codeunit:version>",
                                                                      f"<codeunit:version>{current_version}</codeunit:version>", GeneralUtilities.read_text_from_file(codeunit_file)))
        else:
            raise ValueError(f"Version '{current_version}' does not match version-regex '{versiononlyregex}'")

    def standardized_tasks_linting_for_dotnet_project_in_common_project_structure(self, linting_script_file: str, args: list[str]):
        pass  # TODO

    def standardized_tasks_generate_reference_by_docfx(self, generate_reference_script_file: str) -> None:
        folder_of_current_file = os.path.dirname(generate_reference_script_file)
        generated_reference_folder = os.path.join(folder_of_current_file, "GeneratedReference")
        GeneralUtilities.ensure_directory_does_not_exist(generated_reference_folder)
        GeneralUtilities.ensure_directory_exists(generated_reference_folder)
        obj_folder = os.path.join(folder_of_current_file, "obj")
        GeneralUtilities.ensure_directory_does_not_exist(obj_folder)
        GeneralUtilities.ensure_directory_exists(obj_folder)
        self.run_program("docfx", "docfx.json", folder_of_current_file)
        GeneralUtilities.ensure_directory_does_not_exist(obj_folder)

    def standardized_tasks_linting_for_python_project_in_common_project_structure(self, linting_script_file):
        repository_folder: str = str(Path(os.path.dirname(linting_script_file)).parent.parent.parent.absolute())
        codeunitname: str = Path(os.path.dirname(linting_script_file)).parent.parent.name
        errors_found = False
        GeneralUtilities.write_message_to_stdout(f"Check for linting-issues in codeunit {codeunitname}")
        src_folder = os.path.join(repository_folder, codeunitname, codeunitname)
        tests_folder = src_folder+"Tests"
        for file in GeneralUtilities.get_all_files_of_folder(src_folder)+GeneralUtilities.get_all_files_of_folder(tests_folder):
            relative_file_path_in_repository = os.path.relpath(file, repository_folder)
            if file.endswith(".py") and os.path.getsize(file) > 0 and not self.file_is_git_ignored(relative_file_path_in_repository, repository_folder):
                GeneralUtilities.write_message_to_stdout(f"Check for linting-issues in {os.path.relpath(file,os.path.join(repository_folder,codeunitname))}")
                linting_result = self.python_file_has_errors(file, repository_folder)
                if (linting_result[0]):
                    errors_found = True
                    for error in linting_result[1]:
                        GeneralUtilities.write_message_to_stderr(error)
        if errors_found:
            raise Exception("Linting-issues occurred")
        else:
            GeneralUtilities.write_message_to_stdout("No linting-issues found.")

    def standardized_tasks_run_testcases_for_python_project(self, repository_folder: str, codeunitname: str):
        codeunit_folder = os.path.join(repository_folder, codeunitname)
        self.run_program("coverage", "run -m pytest", codeunit_folder)
        self.run_program("coverage", "xml", codeunit_folder)
        coveragefile = os.path.join(repository_folder, codeunitname, "Other/QualityCheck/TestCoverage/TestCoverage.xml")
        GeneralUtilities.ensure_file_does_not_exist(coveragefile)
        os.rename(os.path.join(repository_folder, codeunitname, "coverage.xml"), coveragefile)

    def standardized_tasks_generate_coverage_report(self, repository_folder: str, codeunitname: str, verbosity: int = 1, generate_badges: bool = True, args: list[str] = []):
        """This script expects that the file '<repositorybasefolder>/<codeunitname>/Other/QualityCheck/TestCoverage/TestCoverage.xml'
        which contains a test-coverage-report in the cobertura-format exists.
        This script expectes that the testcoverage-reportfolder is '<repositorybasefolder>/<codeunitname>/Other/QualityCheck/TestCoverage/TestCoverageReport'.
        This script expectes that a test-coverage-badges should be added to '<repositorybasefolder>/<codeunitname>/Other/QualityCheck/TestCoverage/Badges'."""
        if verbosity == 0:
            verbose_argument_for_reportgenerator = "Off"
        if verbosity == 1:
            verbose_argument_for_reportgenerator = "Error"
        if verbosity == 2:
            verbose_argument_for_reportgenerator = "Info"
        if verbosity == 3:
            verbose_argument_for_reportgenerator = "Verbose"

        # Generating report
        GeneralUtilities.ensure_directory_does_not_exist(os.path.join(repository_folder, codeunitname, "Other/QualityCheck/TestCoverage/TestCoverageReport"))
        GeneralUtilities.ensure_directory_exists(os.path.join(repository_folder, codeunitname, "Other/QualityCheck/TestCoverage/TestCoverageReport"))
        self.run_program("reportgenerator", "-reports:Other/QualityCheck/TestCoverage/TestCoverage.xml -targetdir:Other/QualityCheck/TestCoverage/TestCoverageReport " +
                         f"-verbosity:{verbose_argument_for_reportgenerator}", os.path.join(repository_folder, codeunitname))

        if generate_badges:
            # Generating badges
            GeneralUtilities.ensure_directory_does_not_exist(os.path.join(repository_folder, codeunitname, "Other/QualityCheck/TestCoverage/Badges"))
            GeneralUtilities.ensure_directory_exists(os.path.join(repository_folder, codeunitname, "Other/QualityCheck/TestCoverage/Badges"))
            self.run_program("reportgenerator", "-reports:Other/QualityCheck/TestCoverage/TestCoverage.xml -targetdir:Other/QualityCheck/TestCoverage/Badges -reporttypes:Badges " +
                             f"-verbosity:{verbose_argument_for_reportgenerator}",  os.path.join(repository_folder, codeunitname))

    def standardized_tasks_generate_refefrence_for_dotnet_project_in_common_project_structure(self, generate_reference_file: str, commandline_arguments: list[str] = []):
        reference_folder = os.path.dirname(generate_reference_file)
        reference_result_folder = os.path.join(reference_folder, "GeneratedReference")
        GeneralUtilities.ensure_directory_does_not_exist(reference_result_folder)
        self.run_program("docfx", "docfx.json", reference_folder)

    @GeneralUtilities.check_arguments
    def standardized_tasks_run_testcases_for_dotnet_project_in_common_project_structure(self, runtestcases_file: str, buildconfiguration: str = "Release", commandline_arguments: list[str] = []):
        repository_folder: str = str(Path(os.path.dirname(runtestcases_file)).parent.parent.parent.absolute())
        codeunit_name: str = os.path.basename(str(Path(os.path.dirname(runtestcases_file)).parent.parent.absolute()))
        for commandline_argument in commandline_arguments:
            if commandline_argument.startswith("-buildconfiguration:"):
                buildconfiguration = commandline_argument[len("-buildconfiguration:"):]
        testprojectname = codeunit_name+"Tests"
        coveragefilesource = os.path.join(repository_folder, codeunit_name, testprojectname, "TestCoverage.xml")
        coveragefiletarget = os.path.join(repository_folder, codeunit_name, "Other/QualityCheck/TestCoverage/TestCoverage.xml")
        GeneralUtilities.ensure_file_does_not_exist(coveragefilesource)
        self.run_program("dotnet", f"test {testprojectname}/{testprojectname}.csproj -c {buildconfiguration}"
                         f" --verbosity normal /p:CollectCoverage=true /p:CoverletOutput=TestCoverage.xml"
                         f" /p:CoverletOutputFormat=cobertura", os.path.join(repository_folder, codeunit_name))
        GeneralUtilities.ensure_file_does_not_exist(coveragefiletarget)
        os.rename(coveragefilesource, coveragefiletarget)
        self.standardized_tasks_generate_coverage_report(repository_folder, codeunit_name, 1)

    def replace_version_in_nuspec_file(self, nuspec_file: str, current_version: str):
        versionregex = "\\d+\\.\\d+\\.\\d+"
        versiononlyregex = f"^{versionregex}$"
        pattern = re.compile(versiononlyregex)
        if pattern.match(current_version):
            GeneralUtilities.write_text_to_file(nuspec_file, re.sub(f"<version>{versionregex}<\\/version>",
                                                                    f"<version>{current_version}</version>", GeneralUtilities.read_text_from_file(nuspec_file)))
        else:
            raise ValueError(f"Version '{current_version}' does not match version-regex '{versiononlyregex}'")

    def replace_version_in_csproj_file(self, csproj_file: str, current_version: str):
        versionregex = "\\d+\\.\\d+\\.\\d+"
        versiononlyregex = f"^{versionregex}$"
        pattern = re.compile(versiononlyregex)
        if pattern.match(current_version):
            GeneralUtilities.write_text_to_file(csproj_file, re.sub(f"<Version>{versionregex}<\\/Version>",
                                                                    f"<Version>{current_version}</Version>", GeneralUtilities.read_text_from_file(csproj_file)))
        else:
            raise ValueError(f"Version '{current_version}' does not match version-regex '{versiononlyregex}'")

    @GeneralUtilities.check_arguments
    def push_nuget_build_artifact_of_repository_in_common_file_structure(self, nupkg_file: str, registry_address: str, api_key: str, verbosity: int = 1):
        nupkg_file_name = os.path.basename(nupkg_file)
        nupkg_file_folder = os.path.dirname(nupkg_file)
        self.run_program("dotnet", f"nuget push {nupkg_file_name} --force-english-output --source {registry_address} --api-key {api_key}",
                         nupkg_file_folder, verbosity)

    def standardized_tasks_run_testcases_for_python_project_in_common_project_structure(self, run_testcases_file: str, generate_badges: bool = True):
        repository_folder: str = str(Path(os.path.dirname(run_testcases_file)).parent.parent.parent.absolute())
        codeunitname: str = Path(os.path.dirname(run_testcases_file)).parent.parent.name
        self.standardized_tasks_run_testcases_for_python_project(repository_folder, codeunitname)
        self.standardized_tasks_generate_coverage_report(repository_folder, codeunitname, generate_badges)

    def standardized_tasks_build_for_python_project_in_common_project_structure(self, build_file: str):
        setuppy_file_folder = str(Path(os.path.dirname(build_file)).parent.parent.absolute())
        setuppy_file_filename = "Setup.py"
        repository_folder: str = str(Path(os.path.dirname(build_file)).parent.parent.parent.absolute())
        codeunitname: str = Path(os.path.dirname(build_file)).parent.parent.name
        target_directory = os.path.join(repository_folder, codeunitname, "Other", "Build", "BuildArtifact")
        GeneralUtilities.ensure_directory_does_not_exist(target_directory)
        self.run_program("git", f"clean -dfx --exclude={codeunitname}/Other {codeunitname}", repository_folder)
        GeneralUtilities.ensure_directory_exists(target_directory)
        self.run_program("python", f"{setuppy_file_filename} bdist_wheel --dist-dir {target_directory}", setuppy_file_folder)

    @GeneralUtilities.check_arguments
    def dotnet_executable_build(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        verbosity = self.__get_verbosity_for_exuecutor(configparser)
        sign_things = self.__get_sign_things(configparser, current_release_information)
        config = self.get_item_from_configuration(configparser, 'dotnet', 'buildconfiguration', current_release_information)
        for runtime in self.get_items_from_configuration(configparser, 'dotnet', 'runtimes', current_release_information):
            self.dotnet_build_old(current_release_information, self.__get_csprojfile_folder(configparser, current_release_information),
                                  self.__get_csprojfile_filename(configparser, current_release_information),
                                  self.__get_buildoutputdirectory(configparser, runtime, current_release_information), config,
                                  runtime, self.get_item_from_configuration(configparser, 'dotnet', 'dotnetframework', current_release_information), True,
                                  verbosity, sign_things[0], sign_things[1])
        publishdirectory = self.get_item_from_configuration(configparser, 'dotnet', 'publishdirectory', current_release_information)
        GeneralUtilities.ensure_directory_does_not_exist(publishdirectory)
        shutil.copytree(self.get_item_from_configuration(configparser, 'dotnet', 'buildoutputdirectory', current_release_information), publishdirectory)

    @GeneralUtilities.check_arguments
    def dotnet_build(self, repository_folder: str, projectname: str, configuration: str):
        self.run_program("dotnet", f"clean -c {configuration}", repository_folder)
        self.run_program("dotnet", f"build {projectname}/{projectname}.csproj -c {configuration}", repository_folder)

    @GeneralUtilities.check_arguments
    def __get_sign_things(self, configparser: ConfigParser, current_release_information: dict[str, str]) -> tuple:
        files_to_sign_raw_value = self.get_items_from_configuration(configparser, 'dotnet', 'filestosign', current_release_information)
        if(GeneralUtilities.string_is_none_or_whitespace(files_to_sign_raw_value)):
            return [None, None]
        else:
            return [GeneralUtilities.to_list(files_to_sign_raw_value, ";"), self.get_item_from_configuration(configparser, 'dotnet', 'snkfile', current_release_information)]

    @GeneralUtilities.check_arguments
    def dotnet_create_executable_release_premerge(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        repository_version = self.get_version_for_buildscripts(configparser, current_release_information)
        if self.get_boolean_value_from_configuration(configparser, 'dotnet', 'updateversionsincsprojfile', current_release_information):
            GeneralUtilities.update_version_in_csproj_file(self.get_item_from_configuration(configparser, 'dotnet', 'csprojfile', current_release_information), repository_version)
        self.__run_testcases(configurationfile, current_release_information)

    @GeneralUtilities.check_arguments
    def dotnet_create_executable_release_postmerge(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        self.dotnet_executable_build(configurationfile, current_release_information)
        self.dotnet_generate_reference(configurationfile, current_release_information)

    @GeneralUtilities.check_arguments
    def dotnet_create_nuget_release_premerge(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        repository_version = self.get_version_for_buildscripts(configparser, current_release_information)
        if self.get_boolean_value_from_configuration(configparser, 'dotnet', 'updateversionsincsprojfile', current_release_information):
            GeneralUtilities.update_version_in_csproj_file(self.get_item_from_configuration(configparser, 'dotnet', 'csprojfile', current_release_information), repository_version)
        self.__run_testcases(configurationfile, current_release_information)

    @GeneralUtilities.check_arguments
    def __run_testcases(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        if self.get_boolean_value_from_configuration(configparser, 'other', 'hastestproject', current_release_information):
            scriptfile = self.get_item_from_configuration(configparser, 'other', "runtestcasesscript", current_release_information)
            self.run_program("python", os.path.dirname(scriptfile), os.path.basename(scriptfile))
            coverage_file = os.path.join(self.get_item_from_configuration(configparser, "general", "repository",
                                         current_release_information), "Other", "TestCoverage", "TestCoverage.xml")
            root: etree._ElementTree = etree.parse(coverage_file)
            coverage_in_percent = round(float(str(root.xpath('//coverage/@line-rate')[0]))*100, 2)
            current_release_information['general.testcoverage'] = coverage_in_percent
            minimalrequiredtestcoverageinpercent = self.get_number_value_from_configuration(configparser, "other", "minimalrequiredtestcoverageinpercent")
            if(coverage_in_percent < minimalrequiredtestcoverageinpercent):
                raise ValueError(f"The testcoverage must be {minimalrequiredtestcoverageinpercent}% or more but is {coverage_in_percent}%.")

    @GeneralUtilities.check_arguments
    def run_testcases_for_csharp_project(self, repository_folder: str, testprojectname: str, configuration: str):
        self.dotnet_build(repository_folder, testprojectname, configuration)
        coveragefilesource = os.path.join(repository_folder, f"{testprojectname}/TestCoverage.xml")
        coveragefiletarget = os.path.join(repository_folder, "Other/TestCoverage/TestCoverage.xml")
        GeneralUtilities.ensure_file_does_not_exist(coveragefilesource)
        self.run_program("dotnet", f"test {testprojectname}/{testprojectname}.csproj -c {configuration}"
                         f" --verbosity normal /p:CollectCoverage=true /p:CoverletOutput=TestCoverage.xml"
                         f" /p:CoverletOutputFormat=cobertura", repository_folder)
        GeneralUtilities.ensure_file_does_not_exist(coveragefiletarget)
        os.rename(coveragefilesource, coveragefiletarget)

    @GeneralUtilities.check_arguments
    def dotnet_create_nuget_release_postmerge(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        self.dotnet_nuget_build(configurationfile, current_release_information)
        self.dotnet_generate_reference(configurationfile, current_release_information)
        self.dotnet_release_nuget(configurationfile, current_release_information)

    __nuget_template = r"""<?xml version="1.0" encoding="utf-8"?>
    <package xmlns="http://schemas.microsoft.com/packaging/2011/10/nuspec.xsd">
      <metadata minClientVersion="2.12">
        <id>__.general.productname.__</id>
        <version>__.builtin.version.__</version>
        <title>__.general.productname.__</title>
        <authors>__.general.author.__</authors>
        <owners>__.general.author.__</owners>
        <requireLicenseAcceptance>true</requireLicenseAcceptance>
        <copyright>Copyright © __.builtin.year.__ by __.general.author.__</copyright>
        <description>__.general.description.__</description>
        <summary>__.general.description.__</summary>
        <license type="file">lib/__.dotnet.dotnetframework.__/__.general.productname.__.License.txt</license>
        <dependencies>
          <group targetFramework="__.dotnet.dotnetframework.__" />
        </dependencies>
        __.internal.projecturlentry.__
        __.internal.repositoryentry.__
        __.internal.iconentry.__
      </metadata>
      <files>
        <file src="Binary/__.general.productname.__.dll" target="lib/__.dotnet.dotnetframework.__" />
        <file src="Binary/__.general.productname.__.License.txt" target="lib/__.dotnet.dotnetframework.__" />
        __.internal.iconfileentry.__
      </files>
    </package>"""

    @GeneralUtilities.check_arguments
    def dotnet_nuget_build(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        sign_things = self.__get_sign_things(configparser, current_release_information)
        config = self.get_item_from_configuration(configparser, 'dotnet', 'buildconfiguration', current_release_information)
        for runtime in self.get_items_from_configuration(configparser, 'dotnet', 'runtimes', current_release_information):
            self.dotnet_build_old(current_release_information, self.__get_csprojfile_folder(configparser, current_release_information),
                                  self.__get_csprojfile_filename(configparser, current_release_information),
                                  self.__get_buildoutputdirectory(configparser, runtime, current_release_information), config,
                                  runtime, self.get_item_from_configuration(configparser, 'dotnet', 'dotnetframework', current_release_information), True,
                                  self.__get_verbosity_for_exuecutor(configparser),
                                  sign_things[0], sign_things[1])
        publishdirectory = self.get_item_from_configuration(configparser, 'dotnet', 'publishdirectory', current_release_information)
        publishdirectory_binary = publishdirectory+os.path.sep+"Binary"
        GeneralUtilities.ensure_directory_does_not_exist(publishdirectory)
        shutil.copytree(self.get_item_from_configuration(configparser, 'dotnet', 'buildoutputdirectory', current_release_information), publishdirectory_binary)

        nuspec_content = self.__replace_underscores_for_buildconfiguration(self.__nuget_template, configparser, current_release_information)

        if(self.configuration_item_is_available(configparser, "other", "projecturl")):
            nuspec_content = nuspec_content.replace("__.internal.projecturlentry.__",
                                                    f"<projectUrl>{self.get_item_from_configuration(configparser, 'other', 'projecturl',current_release_information)}</projectUrl>")
        else:
            nuspec_content = nuspec_content.replace("__.internal.projecturlentry.__", "")

        if "builtin.commitid" in current_release_information and self.configuration_item_is_available(configparser, "other", "repositoryurl"):
            repositoryurl = self.get_item_from_configuration(configparser, 'other', 'repositoryurl', current_release_information)
            branch = self.get_item_from_configuration(configparser, 'prepare', 'targetbranchname', current_release_information)
            commitid = current_release_information["builtin.commitid"]
            nuspec_content = nuspec_content.replace("__.internal.repositoryentry.__", f'<repository type="git" url="{repositoryurl}" branch="{branch}" commit="{commitid}" />')
        else:
            nuspec_content = nuspec_content.replace("__.internal.repositoryentry.__", "")

        if self.configuration_item_is_available(configparser, "dotnet", "iconfile"):
            shutil.copy2(self.get_item_from_configuration(configparser, "dotnet", "iconfile", current_release_information), os.path.join(publishdirectory, "icon.png"))
            nuspec_content = nuspec_content.replace("__.internal.iconentry.__", '<icon>images\\icon.png</icon>')
            nuspec_content = nuspec_content.replace("__.internal.iconfileentry.__", '<file src=".\\icon.png" target="images\\" />')
        else:
            nuspec_content = nuspec_content.replace("__.internal.iconentry.__", "")
            nuspec_content = nuspec_content.replace("__.internal.iconfileentry.__", "")

        nuspecfilename = self.get_item_from_configuration(configparser, 'general', 'productname', current_release_information)+".nuspec"
        nuspecfile = os.path.join(publishdirectory, nuspecfilename)
        with open(nuspecfile, encoding="utf-8", mode="w") as file_object:
            file_object.write(nuspec_content)
        self.run_program("nuget", f"pack {nuspecfilename}", publishdirectory, self.__get_verbosity_for_exuecutor(configparser))

    @GeneralUtilities.check_arguments
    def dotnet_release_nuget(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        repository_version = self.get_version_for_buildscripts(configparser, current_release_information)
        publishdirectory = self.get_item_from_configuration(configparser, 'dotnet', 'publishdirectory', current_release_information)
        latest_nupkg_file = self.get_item_from_configuration(configparser, 'general', 'productname', current_release_information)+"."+repository_version+".nupkg"
        for localnugettarget in self.get_items_from_configuration(configparser, 'dotnet', 'localnugettargets', current_release_information):
            self.run_program("dotnet", f"nuget push {latest_nupkg_file} --force-english-output --source {localnugettarget}",
                             publishdirectory,  self.__get_verbosity_for_exuecutor(configparser))
        if (self.get_boolean_value_from_configuration(configparser, 'dotnet', 'publishnugetfile', current_release_information)):
            with open(self.get_item_from_configuration(configparser, 'dotnet', 'nugetapikeyfile', current_release_information), 'r', encoding='utf-8') as apikeyfile:
                api_key = apikeyfile.read()
            nugetsource = self.get_item_from_configuration(configparser, 'dotnet', 'nugetsource', current_release_information)
            self.run_program("dotnet", f"nuget push {latest_nupkg_file} --force-english-output --source {nugetsource} --api-key {api_key}",
                             publishdirectory, self.__get_verbosity_for_exuecutor(configparser))

    @GeneralUtilities.check_arguments
    def dotnet_generate_reference(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        if self.get_boolean_value_from_configuration(configparser, 'dotnet', 'generatereference', current_release_information):
            self.git_checkout(
                self.get_item_from_configuration(configparser, 'other', 'referencerepository', current_release_information),
                self.get_item_from_configuration(configparser, 'other', 'exportreferencelocalbranchname', current_release_information))
            verbosity = self.__get_verbosity_for_exuecutor(configparser)
            if verbosity == 0:
                verbose_argument_for_docfx = "Error"
            if verbosity == 1:
                verbose_argument_for_docfx = "Warning"
            if verbosity == 2:
                verbose_argument_for_docfx = "Info"
            if verbosity == 3:
                verbose_argument_for_docfx = "verbose"
            docfx_file = self.get_item_from_configuration(configparser, 'dotnet', 'docfxfile', current_release_information)
            docfx_folder = os.path.dirname(docfx_file)
            GeneralUtilities.ensure_directory_does_not_exist(os.path.join(docfx_folder, "obj"))
            self.run_program("docfx", f'"{os.path.basename(docfx_file)}" --loglevel {verbose_argument_for_docfx}',
                             docfx_folder, verbosity)
            self.git_commit(self.get_item_from_configuration(configparser, 'other', 'referencerepository', current_release_information), "Updated reference")
            if self.get_boolean_value_from_configuration(configparser, 'other', 'exportreference', current_release_information):
                self.git_push(self.get_item_from_configuration(configparser, 'other', 'referencerepository', current_release_information),
                              self.get_item_from_configuration(configparser, 'other', 'exportreferenceremotename', current_release_information),
                              self.get_item_from_configuration(configparser, 'other', 'exportreferencelocalbranchname', current_release_information),
                              self.get_item_from_configuration(configparser, 'other', 'exportreferenceremotebranchname', current_release_information), False, False)

    @GeneralUtilities.check_arguments
    def dotnet_build_old(self, current_release_information: dict, folderOfCsprojFile: str, csprojFilename: str, outputDirectory: str, buildConfiguration: str, runtimeId: str, dotnet_framework: str,
                         clearOutputDirectoryBeforeBuild: bool = True, verbosity: int = 1, filesToSign: list = None, keyToSignForOutputfile: str = None) -> None:
        if os.path.isdir(outputDirectory) and clearOutputDirectoryBeforeBuild:
            GeneralUtilities.ensure_directory_does_not_exist(outputDirectory)
        GeneralUtilities.ensure_directory_exists(outputDirectory)
        GeneralUtilities.write_message_to_stdout("verbosity")
        GeneralUtilities.write_message_to_stdout(GeneralUtilities.str_none_safe(verbosity))
        if verbosity == 0:
            verbose_argument_for_dotnet = "quiet"
        elif verbosity == 1:
            verbose_argument_for_dotnet = "minimal"
        elif verbosity == 2:
            verbose_argument_for_dotnet = "normal"
        elif verbosity == 3:
            verbose_argument_for_dotnet = "detailed"
        else:
            raise Exception("Invalid value for verbosity: "+GeneralUtilities.str_none_safe(verbosity))
        argument = csprojFilename
        argument = argument + ' --no-incremental'
        argument = argument + f' --configuration {buildConfiguration}'
        argument = argument + f' --framework {dotnet_framework}'
        argument = argument + f' --runtime {runtimeId}'
        argument = argument + f' --verbosity {verbose_argument_for_dotnet}'
        argument = argument + f' --output "{outputDirectory}"'
        self.run_program("dotnet", f'build {argument}', folderOfCsprojFile, verbosity, addLogOverhead=False, title="Build")
        if(filesToSign is not None):
            for fileToSign in filesToSign:
                self.dotnet_sign(outputDirectory+os.path.sep+fileToSign, keyToSignForOutputfile, verbosity, current_release_information)

    @GeneralUtilities.check_arguments
    def dotnet_sign(self, dllOrExefile: str, snkfile: str, verbosity: int, current_release_information: dict[str, str]) -> None:
        dllOrExeFile = GeneralUtilities.resolve_relative_path_from_current_working_directory(dllOrExefile)
        snkfile = GeneralUtilities.resolve_relative_path_from_current_working_directory(snkfile)
        directory = os.path.dirname(dllOrExeFile)
        filename = os.path.basename(dllOrExeFile)
        if filename.lower().endswith(".dll"):
            filename = filename[:-4]
            extension = "dll"
        elif filename.lower().endswith(".exe"):
            filename = filename[:-4]
            extension = "exe"
        else:
            raise Exception("Only .dll-files and .exe-files can be signed")
        self.run_program("ildasm",
                         f'/all /typelist /text /out="{filename}.il" "{filename}.{extension}"',
                         directory,  verbosity, False, "Sign: ildasm")
        self.run_program("ilasm",
                         f'/{extension} /res:"{filename}.res" /optimize /key="{snkfile}" "{filename}.il"',
                         directory,  verbosity, False, "Sign: ilasm")
        os.remove(directory+os.path.sep+filename+".il")
        os.remove(directory+os.path.sep+filename+".res")

    @GeneralUtilities.check_arguments
    def deb_create_installer_release_premerge(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        pass

    @GeneralUtilities.check_arguments
    def deb_create_installer_release_postmerge(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        return False  # TODO implement

    @GeneralUtilities.check_arguments
    def docker_create_image_release_premerge(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        contextfolder: str = self.get_item_from_configuration(configparser, "docker", "contextfolder", current_release_information)
        imagename: str = self.get_item_from_configuration(configparser, "general", "productname", current_release_information).lower()
        registryaddress: str = self.get_item_from_configuration(configparser, "docker", "registryaddress", current_release_information)
        dockerfile_filename: str = self.get_item_from_configuration(configparser, "docker", "dockerfile", current_release_information)
        repository_version: str = self.get_version_for_buildscripts(configparser, current_release_information)
        environmentconfiguration_for_latest_tag: str = self.get_item_from_configuration(
            configparser, "docker", "environmentconfigurationforlatesttag", current_release_information).lower()
        pushimagetoregistry: bool = self.get_boolean_value_from_configuration(configparser, "docker", "pushimagetoregistry", current_release_information)
        latest_tag: str = f"{imagename}:latest"

        # collect tags
        tags_for_push = []
        tags_by_environment = dict()
        for environmentconfiguration in self.get_items_from_configuration(configparser, "docker", "environmentconfigurations", current_release_information):
            environmentconfiguration_lower: str = environmentconfiguration.lower()
            tags_for_current_environment = []
            version_tag = repository_version  # "1.0.0"
            version_environment_tag = f"{version_tag}-{environmentconfiguration_lower}"  # "1.0.0-environment"
            tags_for_current_environment.append(version_environment_tag)
            if environmentconfiguration_lower == environmentconfiguration_for_latest_tag:
                latest_tag = "latest"  # "latest"
                tags_for_current_environment.append(version_tag)
                tags_for_current_environment.append(latest_tag)
            entire_tags_for_current_environment = []
            for tag in tags_for_current_environment:
                entire_tags_for_current_environment.append(f"{imagename}:{tag}")
                if pushimagetoregistry:
                    tag_for_push = f"{registryaddress}:{tag}"
                    entire_tags_for_current_environment.append(tag_for_push)
                    tags_for_push.append(tag_for_push)
            tags_by_environment[environmentconfiguration] = entire_tags_for_current_environment

        current_release_information["builtin.docker.tags_by_environment"] = tags_by_environment
        current_release_information["builtin.docker.tags_for_push"] = tags_for_push

        # build image
        for environmentconfiguration, tags in tags_by_environment.items():
            argument = f"image build --no-cache --pull --force-rm --progress plain --build-arg EnvironmentStage={environmentconfiguration}"
            for tag in tags:
                argument = f"{argument} --tag {tag}"
            argument = f"{argument} --file {dockerfile_filename} ."
            self.run_program("docker", argument,
                             contextfolder,  print_errors_as_information=True,
                             verbosity=self.__get_verbosity_for_exuecutor(configparser))

    @GeneralUtilities.check_arguments
    def docker_create_image_release_postmerge(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        overwriteexistingfilesinartefactdirectory: bool = self.get_boolean_value_from_configuration(
            configparser, "docker", "overwriteexistingfilesinartefactdirectory", current_release_information)
        verbosity: int = self.__get_verbosity_for_exuecutor(configparser)

        # export to file
        if (self.get_boolean_value_from_configuration(configparser, "docker", "storeimageinartefactdirectory", current_release_information)):
            artefactdirectory = self.get_item_from_configuration(configparser, "docker", "artefactdirectory", current_release_information)
            GeneralUtilities.ensure_directory_exists(artefactdirectory)
            for environment in current_release_information["builtin.docker.tags_by_environment"]:
                for tag in current_release_information["builtin.docker.tags_by_environment"][environment]:
                    if not (tag in current_release_information["builtin.docker.tags_for_push"]):
                        self.__export_tag_to_file(tag, artefactdirectory, overwriteexistingfilesinartefactdirectory, verbosity)

        # push to registry
        for tag in current_release_information["builtin.docker.tags_for_push"]:
            self.run_program("docker", f"push {tag}",
                             print_errors_as_information=True,
                             verbosity=self.__get_verbosity_for_exuecutor(configparser))

        # remove local stored images:
        if self.get_boolean_value_from_configuration(configparser, "docker", "removenewcreatedlocalimagesafterexport", current_release_information):
            for environment in current_release_information["builtin.docker.tags_by_environment"]:
                for tag in current_release_information["builtin.docker.tags_by_environment"][environment]:
                    self.run_program("docker", f"image rm {tag}",
                                     print_errors_as_information=True,
                                     verbosity=verbosity)

    @GeneralUtilities.check_arguments
    def __export_tag_to_file(self, tag: str, artefactdirectory: str, overwriteexistingfilesinartefactdirectory: bool, verbosity: int) -> None:
        if tag.endswith(":latest"):
            separator = "_"
        else:
            separator = "_v"
        targetfile_name = tag.replace(":", separator) + ".tar"
        targetfile = os.path.join(artefactdirectory, targetfile_name)
        if os.path.isfile(targetfile):
            if overwriteexistingfilesinartefactdirectory:
                GeneralUtilities.ensure_file_does_not_exist(targetfile)
            else:
                raise Exception(f"File '{targetfile}' does already exist")

        self.run_program("docker", f"save -o {targetfile} {tag}",
                         print_errors_as_information=True,
                         verbosity=verbosity)

    @GeneralUtilities.check_arguments
    def flutterandroid_create_installer_release_premerge(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        pass

    @GeneralUtilities.check_arguments
    def flutterandroid_create_installer_release_postmerge(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        return False  # TODO implement

    @GeneralUtilities.check_arguments
    def flutterios_create_installer_release_premerge(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        pass

    @GeneralUtilities.check_arguments
    def flutterios_create_installer_release_postmerge(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        return False  # TODO implement

    @GeneralUtilities.check_arguments
    def generic_create_script_release_premerge(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        if GeneralUtilities.string_has_content(self.get_item_from_configuration(configparser, 'script', 'premerge_program', current_release_information)):
            self.run_program(self.get_item_from_configuration(configparser, 'script', 'premerge_program', current_release_information),
                             self.get_item_from_configuration(configparser, 'script', 'premerge_argument', current_release_information),
                             self.get_item_from_configuration(configparser, 'script', 'premerge_workingdirectory', current_release_information))

    @GeneralUtilities.check_arguments
    def generic_create_script_release_postmerge(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        if GeneralUtilities.string_has_content(self.get_item_from_configuration(configparser, 'script', 'postmerge_program', current_release_information)):
            self.run_program(self.get_item_from_configuration(configparser, 'script', 'postmerge_program', current_release_information),
                             self.get_item_from_configuration(configparser, 'script', 'postmerge_argument', current_release_information),
                             self.get_item_from_configuration(configparser, 'script', 'postmerge_workingdirectory', current_release_information))

    @GeneralUtilities.check_arguments
    def python_create_wheel_release_premerge(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        repository_version = self.get_version_for_buildscripts(configparser, current_release_information)

        # Update version
        if(self.get_boolean_value_from_configuration(configparser, 'python', 'updateversion', current_release_information)):
            for file in self.get_items_from_configuration(configparser, 'python', 'filesforupdatingversion', current_release_information):
                GeneralUtilities.replace_regex_each_line_of_file(file, '^version = ".+"\n$', f'version = "{repository_version}"\n')

        # lint-checks
        # TODO run linting-script

        # Run testcases
        self.__run_testcases(configurationfile, current_release_information)

    @GeneralUtilities.check_arguments
    def python_create_wheel_release_postmerge(self, configurationfile: str, current_release_information: dict[str, str]):
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        self.python_build(configurationfile, current_release_information)
        self.python_release_wheel(configurationfile, current_release_information)

    @GeneralUtilities.check_arguments
    def __execute_and_return_boolean(self, name: str, method) -> bool:
        try:
            method()
            return True
        except Exception as exception:
            GeneralUtilities.write_exception_to_stderr_with_traceback(exception, traceback, f"'{name}' resulted in an error")
            return False

    @GeneralUtilities.check_arguments
    def python_build(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        setuppyfile = self.get_item_from_configuration(configparser, "python", "pythonsetuppyfile", current_release_information)
        setuppyfilename = os.path.basename(setuppyfile)
        setuppyfilefolder = os.path.dirname(setuppyfile)
        publishdirectoryforwhlfile = self.get_item_from_configuration(configparser, "python", "publishdirectoryforwhlfile", current_release_information)
        GeneralUtilities.ensure_directory_exists(publishdirectoryforwhlfile)
        self.run_program("python",
                         setuppyfilename+' bdist_wheel --dist-dir "'+publishdirectoryforwhlfile+'"',
                         setuppyfilefolder,  self.__get_verbosity_for_exuecutor(configparser))

    @GeneralUtilities.check_arguments
    def python_release_wheel(self, configurationfile: str, current_release_information: dict[str, str]) -> None:
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        if self.get_boolean_value_from_configuration(configparser, 'python', 'publishwhlfile', current_release_information):
            with open(self.get_item_from_configuration(configparser, 'python', 'pypiapikeyfile', current_release_information), 'r', encoding='utf-8') as apikeyfile:
                api_key = apikeyfile.read()
            gpgidentity = self.get_item_from_configuration(configparser, 'other', 'gpgidentity', current_release_information)
            repository_version = self.get_version_for_buildscripts(configparser, current_release_information)
            productname = self.get_item_from_configuration(configparser, 'general', 'productname', current_release_information)
            verbosity = self.__get_verbosity_for_exuecutor(configparser)
            if verbosity > 2:
                verbose_argument = "--verbose"
            else:
                verbose_argument = ""
            twine_argument = f"upload --sign --identity {gpgidentity} --non-interactive {productname}-{repository_version}-py3-none-any.whl" \
                f" --disable-progress-bar --username __token__ --password {api_key} {verbose_argument}"
            self.run_program("twine", twine_argument,
                             self.get_item_from_configuration(
                                 configparser, "python", "publishdirectoryforwhlfile", current_release_information),
                             verbosity)

    @GeneralUtilities.check_arguments
    def find_file_by_extension(self, folder: str, extension: str):
        result = [file for file in GeneralUtilities.get_direct_files_of_folder(folder) if file.endswith(f".{extension}")]
        result_length = len(result)
        if result_length == 0:
            raise FileNotFoundError(f"No file available in folder '{folder}' with extension '{extension}'.")
        if result_length == 1:
            return result[0]
        else:
            raise ValueError(f"Multiple values available in folder '{folder}' with extension '{extension}'.")

    @GeneralUtilities.check_arguments
    def get_build_folder_in_repository_in_common_repository_format(self, repository_folder: str, codeunit_name: str) -> str:
        return os.path.join(repository_folder, codeunit_name, "Other", "Build", "BuildArtifact")

    @GeneralUtilities.check_arguments
    def get_wheel_file_in_repository_in_common_repository_format(self, repository_folder: str, codeunit_name: str) -> str:
        return self.find_file_by_extension(self.get_build_folder_in_repository_in_common_repository_format(repository_folder, codeunit_name), "whl")

    @GeneralUtilities.check_arguments
    def standardized_tasks_push_wheel_file_to_registry(self, wheel_file: str, api_key: str, repository="pypi", gpg_identity: str = None, verbosity: int = 1) -> None:
        folder = os.path.dirname(wheel_file)
        filename = os.path.basename(wheel_file)

        if gpg_identity is None:
            gpg_identity_argument = ""
        else:
            gpg_identity_argument = f" --sign --identity {gpg_identity}"

        if verbosity > 2:
            verbose_argument = " --verbose"
        else:
            verbose_argument = ""

        twine_argument = f"upload{gpg_identity_argument} --repository {repository} --non-interactive {filename} --disable-progress-bar"
        twine_argument = f"{twine_argument} --username __token__ --password {api_key}{verbose_argument}"
        self.run_program("twine", twine_argument, folder, verbosity, throw_exception_if_exitcode_is_not_zero=True)

    @GeneralUtilities.check_arguments
    def push_wheel_build_artifact_of_repository_in_common_file_structure(self, push_build_artifacts_file, product_name, codeunitname, apikey, gpg_identity: str = None) -> None:
        folder_of_this_file = os.path.dirname(push_build_artifacts_file)
        repository_folder = GeneralUtilities.resolve_relative_path(f"..{os.path.sep}../Submodules{os.path.sep}{product_name}", folder_of_this_file)
        wheel_file = self.get_wheel_file_in_repository_in_common_repository_format(repository_folder, codeunitname)
        self.standardized_tasks_push_wheel_file_to_registry(wheel_file, apikey, gpg_identity=gpg_identity)

    @GeneralUtilities.check_arguments
    def dotnet_sign_file(self, file: str, keyfile: str):
        directory = os.path.dirname(file)
        filename = os.path.basename(file)
        if filename.lower().endswith(".dll"):
            filename = filename[:-4]
            extension = "dll"
        elif filename.lower().endswith(".exe"):
            filename = filename[:-4]
            extension = "exe"
        else:
            raise Exception("Only .dll-files and .exe-files can be signed")
        self.run_program("ildasm", f'/all /typelist /text /out={filename}.il {filename}.{extension}', directory)
        self.run_program("ilasm", f'/{extension} /res:{filename}.res /optimize /key={keyfile} {filename}.il', directory)
        os.remove(directory+os.path.sep+filename+".il")
        os.remove(directory+os.path.sep+filename+".res")

    @GeneralUtilities.check_arguments
    def standardized_tasks_build_for_dotnet_build(self, csproj_file: str, buildconfiguration: str, outputfolder: str, files_to_sign: dict):
        # TODO update version in csproj-file
        csproj_file_folder = os.path.dirname(csproj_file)
        csproj_file_name = os.path.basename(csproj_file)
        self.run_program("dotnet", "clean", csproj_file_folder)
        GeneralUtilities.ensure_directory_does_not_exist(outputfolder)
        GeneralUtilities.ensure_directory_exists(outputfolder)
        self.run_program("dotnet", f"build {csproj_file_name} -c {buildconfiguration} -o {outputfolder}", csproj_file_folder)
        for file, keyfile in files_to_sign.items():
            self.dotnet_sign_file(os.path.join(outputfolder, file), keyfile)

    @GeneralUtilities.check_arguments
    def standardized_tasks_build_for_dotnet_project_in_common_project_structure(self, repository_folder: str, codeunitname: str,
                                                                                buildconfiguration: str, build_test_project_too: bool, output_folder: str, commandline_arguments: list[str]):
        codeunit_folder = os.path.join(repository_folder, codeunitname)
        csproj_file = os.path.join(codeunit_folder, codeunitname, codeunitname+".csproj")
        csproj_test_file = os.path.join(codeunit_folder, codeunitname+"Tests", codeunitname+"Tests.csproj")
        commandline_arguments = commandline_arguments[1:]
        files_to_sign: dict() = dict()
        for commandline_argument in commandline_arguments:
            if commandline_argument.startswith("-sign:"):
                commandline_argument_splitted: list[str] = commandline_argument.split(":")
                files_to_sign[commandline_argument_splitted[1]] = commandline_argument[len("-sign:"+commandline_argument_splitted[1])+1:]
        self.run_program("dotnet", "restore", codeunit_folder)
        self.standardized_tasks_build_for_dotnet_build(csproj_file, buildconfiguration, os.path.join(output_folder, codeunitname), files_to_sign)
        if build_test_project_too:
            self.standardized_tasks_build_for_dotnet_build(csproj_test_file, buildconfiguration, os.path.join(output_folder, codeunitname+"Tests"), files_to_sign)

    @GeneralUtilities.check_arguments
    def standardized_tasks_build_for_dotnet_library_project_in_common_project_structure(self, buildscript_file: str, buildconfiguration: str = "Release", commandline_arguments: list[str] = []):
        repository_folder: str = str(Path(os.path.dirname(buildscript_file)).parent.parent.parent.absolute())
        codeunitname: str = os.path.basename(str(Path(os.path.dirname(buildscript_file)).parent.parent.absolute()))
        for commandline_argument in commandline_arguments:
            if commandline_argument.startswith("-buildconfiguration:"):
                buildconfiguration = commandline_argument[len("-buildconfiguration:"):]
        outputfolder = os.path.join(os.path.dirname(buildscript_file), "BuildArtifact")
        GeneralUtilities.ensure_directory_does_not_exist(outputfolder)
        GeneralUtilities.ensure_directory_exists(outputfolder)
        self.standardized_tasks_build_for_dotnet_project_in_common_project_structure(
            repository_folder, codeunitname, buildconfiguration, True, outputfolder, commandline_arguments)
        self.standardized_tasks_build_for_dotnet_create_package(repository_folder, codeunitname, outputfolder)

    @GeneralUtilities.check_arguments
    def standardized_tasks_build_for_dotnet_create_package(self, repository: str, codeunitname: str, outputfolder: str):
        build_folder = os.path.join(repository, codeunitname, "Other", "Build")
        root: etree._ElementTree = etree.parse(os.path.join(build_folder, f"{codeunitname}.nuspec"))
        current_version = root.xpath("//*[name() = 'package']/*[name() = 'metadata']/*[name() = 'version']/text()")[0]
        nupkg_filename = f"{codeunitname}.{current_version}.nupkg"
        nupkg_file = f"{build_folder}/{nupkg_filename}"
        GeneralUtilities.ensure_file_does_not_exist(nupkg_file)
        self.run_program("nuget", f"pack {codeunitname}.nuspec", build_folder)
        GeneralUtilities.ensure_directory_does_not_exist(outputfolder)
        GeneralUtilities.ensure_directory_exists(outputfolder)
        os.rename(nupkg_file, f"{build_folder}/BuildArtifact/{nupkg_filename}")

    @GeneralUtilities.check_arguments
    def commit_is_signed_by_key(self, repository_folder: str, revision_identifier: str, key: str) -> bool:
        result = self.run_program("git", f"verify-commit {revision_identifier}", repository_folder, throw_exception_if_exitcode_is_not_zero=False)
        if(result[0] != 0):
            return False
        if(not GeneralUtilities.contains_line(result[1].splitlines(), f"gpg\\:\\ using\\ [A-Za-z0-9]+\\ key\\ [A-Za-z0-9]+{key}")):
            # TODO check whether this works on machines where gpg is installed in another langauge than english
            return False
        if(not GeneralUtilities.contains_line(result[1].splitlines(), "gpg\\:\\ Good\\ signature\\ from")):
            # TODO check whether this works on machines where gpg is installed in another langauge than english
            return False
        return True

    @GeneralUtilities.check_arguments
    def get_parent_commit_ids_of_commit(self, repository_folder: str, commit_id: str) -> str:
        return self.run_program("git", f'log --pretty=%P -n 1 "{commit_id}"',
                                       repository_folder, throw_exception_if_exitcode_is_not_zero=True)[1].replace("\r", "").replace("\n", "").split(" ")

    @GeneralUtilities.check_arguments
    def get_commit_ids_between_dates(self, repository_folder: str, since: datetime, until: datetime, ignore_commits_which_are_not_in_history_of_head: bool = True) -> None:
        since_as_string = self.__datetime_to_string_for_git(since)
        until_as_string = self.__datetime_to_string_for_git(until)
        result = filter(lambda line: not GeneralUtilities.string_is_none_or_whitespace(line),
                        self.run_program("git", f'log --since "{since_as_string}" --until "{until_as_string}" --pretty=format:"%H" --no-patch',
                                         repository_folder, throw_exception_if_exitcode_is_not_zero=True)[1].split("\n").replace("\r", ""))
        if ignore_commits_which_are_not_in_history_of_head:
            result = [commit_id for commit_id in result if self.git_commit_is_ancestor(repository_folder, commit_id)]
        return result

    @GeneralUtilities.check_arguments
    def __datetime_to_string_for_git(self, datetime_object: datetime) -> str:
        return datetime_object.strftime('%Y-%m-%d %H:%M:%S')

    @GeneralUtilities.check_arguments
    def git_commit_is_ancestor(self, repository_folder: str,  ancestor: str, descendant: str = "HEAD") -> bool:
        return self.run_program_argsasarray("git", ["merge-base", "--is-ancestor", ancestor, descendant], repository_folder, throw_exception_if_exitcode_is_not_zero=False)[0] == 0

    @GeneralUtilities.check_arguments
    def __git_changes_helper(self, repository_folder: str, arguments_as_array: list[str]) -> bool:
        lines = GeneralUtilities.string_to_lines(self.run_program_argsasarray("git", arguments_as_array, repository_folder,
                                                 throw_exception_if_exitcode_is_not_zero=True, verbosity=0)[1], False)
        for line in lines:
            if GeneralUtilities.string_has_content(line):
                return True
        return False

    @GeneralUtilities.check_arguments
    def git_repository_has_new_untracked_files(self, repositoryFolder: str):
        return self.__git_changes_helper(repositoryFolder, ["ls-files", "--exclude-standard", "--others"])

    @GeneralUtilities.check_arguments
    def git_repository_has_unstaged_changes_of_tracked_files(self, repositoryFolder: str):
        return self.__git_changes_helper(repositoryFolder, ["diff"])

    @GeneralUtilities.check_arguments
    def git_repository_has_staged_changes(self, repositoryFolder: str):
        return self.__git_changes_helper(repositoryFolder, ["diff", "--cached"])

    @GeneralUtilities.check_arguments
    def git_repository_has_uncommitted_changes(self, repositoryFolder: str) -> bool:
        if (self.git_repository_has_unstaged_changes(repositoryFolder)):
            return True
        if (self.git_repository_has_staged_changes(repositoryFolder)):
            return True
        return False

    @GeneralUtilities.check_arguments
    def git_repository_has_unstaged_changes(self, repository_folder: str) -> bool:
        if(self.git_repository_has_unstaged_changes_of_tracked_files(repository_folder)):
            return True
        if(self.git_repository_has_new_untracked_files(repository_folder)):
            return True
        return False

    @GeneralUtilities.check_arguments
    def git_get_current_commit_id(self, repository_folder: str, commit: str = "HEAD") -> str:
        result: tuple[int, str, str, int] = self.run_program_argsasarray("git", ["rev-parse", "--verify", commit],
                                                                         repository_folder, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)
        return result[1].replace('\n', '')

    @GeneralUtilities.check_arguments
    def git_fetch(self, folder: str, remotename: str = "--all") -> None:
        self.run_program_argsasarray("git", ["fetch", remotename, "--tags", "--prune"], folder, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_fetch_in_bare_repository(self, folder: str, remotename, localbranch: str, remotebranch: str) -> None:
        self.run_program_argsasarray("git", ["fetch", remotename, f"{remotebranch}:{localbranch}"], folder, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_remove_branch(self, folder: str, branchname: str) -> None:
        self.run_program("git", f"branch -D {branchname}", folder, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_push(self, folder: str, remotename: str, localbranchname: str, remotebranchname: str, forcepush: bool = False, pushalltags: bool = True, verbosity: int = 0) -> None:
        argument = ["push", remotename, f"{localbranchname}:{remotebranchname}"]
        if (forcepush):
            argument.append("--force")
        if (pushalltags):
            argument.append("--tags")
        result: tuple[int, str, str, int] = self.run_program_argsasarray("git", argument, folder, throw_exception_if_exitcode_is_not_zero=True, verbosity=verbosity)
        return result[1].replace('\r', '').replace('\n', '')

    @GeneralUtilities.check_arguments
    def git_clone(self, clone_target_folder: str, remote_repository_path: str, include_submodules: bool = True, mirror: bool = False) -> None:
        if(os.path.isdir(clone_target_folder)):
            pass  # TODO throw error
        else:
            args = ["clone", remote_repository_path, clone_target_folder]
            if include_submodules:
                args.append("--recurse-submodules")
                args.append("--remote-submodules")
            if mirror:
                args.append("--mirror")
            self.run_program_argsasarray("git", args, os.getcwd(), throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_get_all_remote_names(self, directory) -> list[str]:
        result = GeneralUtilities.string_to_lines(self.run_program_argsasarray("git", ["remote"], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)[1], False)
        return result

    @GeneralUtilities.check_arguments
    def repository_has_remote_with_specific_name(self, directory: str, remote_name: str) -> bool:
        return remote_name in self.git_get_all_remote_names(directory)

    @GeneralUtilities.check_arguments
    def git_add_or_set_remote_address(self, directory: str, remote_name: str, remote_address: str) -> None:
        if (self.repository_has_remote_with_specific_name(directory, remote_name)):
            self.run_program_argsasarray("git", ['remote', 'set-url', 'remote_name', remote_address], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)
        else:
            self.run_program_argsasarray("git", ['remote', 'add', remote_name, remote_address], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_stage_all_changes(self, directory: str) -> None:
        self.run_program_argsasarray("git", ["add", "-A"], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_unstage_all_changes(self, directory: str) -> None:
        self.run_program_argsasarray("git", ["reset"], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_stage_file(self, directory: str, file: str) -> None:
        self.run_program_argsasarray("git", ['stage', file], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_unstage_file(self, directory: str, file: str) -> None:
        self.run_program_argsasarray("git", ['reset', file], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_discard_unstaged_changes_of_file(self, directory: str, file: str) -> None:
        """Caution: This method works really only for 'changed' files yet. So this method does not work properly for new or renamed files."""
        self.run_program_argsasarray("git", ['checkout', file], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_discard_all_unstaged_changes(self, directory: str) -> None:
        """Caution: This function executes 'git clean -df'. This can delete files which maybe should not be deleted. Be aware of that."""
        self.run_program_argsasarray("git", ['clean', '-df'], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)
        self.run_program_argsasarray("git", ['checkout', '.'], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_commit(self, directory: str, message: str, author_name: str = None, author_email: str = None, stage_all_changes: bool = True,
                   no_changes_behavior: int = 0) -> str:
        # no_changes_behavior=0 => No commit
        # no_changes_behavior=1 => Commit anyway
        # no_changes_behavior=2 => Exception
        author_name = GeneralUtilities.str_none_safe(author_name).strip()
        author_email = GeneralUtilities.str_none_safe(author_email).strip()
        argument = ['commit', '--message', message]
        if(GeneralUtilities.string_has_content(author_name)):
            argument.append(f'--author="{author_name} <{author_email}>"')
        git_repository_has_uncommitted_changes = self.git_repository_has_uncommitted_changes(directory)

        if git_repository_has_uncommitted_changes:
            do_commit = True
            if stage_all_changes:
                self.git_stage_all_changes(directory)
        else:
            if no_changes_behavior == 0:
                GeneralUtilities.write_message_to_stdout(f"Commit '{message}' will not be done because there are no changes to commit in repository '{directory}'")
                do_commit = False
            if no_changes_behavior == 1:
                GeneralUtilities.write_message_to_stdout(f"There are no changes to commit in repository '{directory}'. Commit '{message}' will be done anyway.")
                do_commit = True
                argument.append('--allow-empty')
            if no_changes_behavior == 2:
                raise RuntimeError(f"There are no changes to commit in repository '{directory}'. Commit '{message}' will not be done.")

        if do_commit:
            GeneralUtilities.write_message_to_stdout(f"Commit changes in '{directory}'")
            self.run_program_argsasarray("git", argument, directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

        return self.git_get_current_commit_id(directory)

    @GeneralUtilities.check_arguments
    def git_create_tag(self, directory: str, target_for_tag: str, tag: str, sign: bool = False, message: str = None) -> None:
        argument = ["tag", tag, target_for_tag]
        if sign:
            if message is None:
                message = f"Created {target_for_tag}"
            argument.extend(["-s", f'-m "{message}"'])
        self.run_program_argsasarray("git", argument, directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_checkout(self, directory: str, branch: str) -> None:
        self.run_program_argsasarray("git", ["checkout", branch], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_merge_abort(self, directory: str) -> None:
        self.run_program_argsasarray("git", ["merge", "--abort"], directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_merge(self, directory: str, sourcebranch: str, targetbranch: str, fastforward: bool = True, commit: bool = True) -> str:
        self.git_checkout(directory, targetbranch)
        args = ["merge"]
        if not commit:
            args.append("--no-commit")
        if not fastforward:
            args.append("--no-ff")
        args.append(sourcebranch)
        self.run_program_argsasarray("git", args, directory, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)
        return self.git_get_current_commit_id(directory)

    @GeneralUtilities.check_arguments
    def git_undo_all_changes(self, directory: str) -> None:
        """Caution: This function executes 'git clean -df'. This can delete files which maybe should not be deleted. Be aware of that."""
        self.git_unstage_all_changes(directory)
        self.git_discard_all_unstaged_changes(directory)

    @GeneralUtilities.check_arguments
    def __undo_changes(self, repository: str) -> None:
        if(self.git_repository_has_uncommitted_changes(repository)):
            self.git_undo_all_changes(repository)

    @GeneralUtilities.check_arguments
    def __repository_has_changes(self, repository: str) -> bool:
        if(self.git_repository_has_uncommitted_changes(repository)):
            GeneralUtilities.write_message_to_stderr(f"'{repository}' contains uncommitted changes")
            return True
        else:
            return False

    @GeneralUtilities.check_arguments
    def git_fetch_or_clone_all_in_directory(self, source_directory: str, target_directory: str) -> None:
        for subfolder in GeneralUtilities.get_direct_folders_of_folder(source_directory):
            foldername = os.path.basename(subfolder)
            if self.is_git_repository(subfolder):
                source_repository = subfolder
                target_repository = os.path.join(target_directory, foldername)
                if os.path.isdir(target_directory):
                    # fetch
                    self.git_fetch(target_directory)
                else:
                    # clone
                    self.git_clone(target_repository, source_repository, include_submodules=True, mirror=True)

    @GeneralUtilities.check_arguments
    def is_git_repository(self, folder: str) -> bool:
        combined = os.path.join(folder, ".git")
        # TODO consider check for bare-repositories
        return os.path.isdir(combined) or os.path.isfile(combined)

    @GeneralUtilities.check_arguments
    def file_is_git_ignored(self, file_in_repository: str, repositorybasefolder: str) -> None:
        exit_code = self.run_program_argsasarray("git", ['check-ignore', file_in_repository], repositorybasefolder, throw_exception_if_exitcode_is_not_zero=False, verbosity=0)[0]
        if(exit_code == 0):
            return True
        if(exit_code == 1):
            return False
        raise Exception(f"Unable to calculate whether '{file_in_repository}' in repository '{repositorybasefolder}' is ignored due to git-exitcode {exit_code}.")

    @GeneralUtilities.check_arguments
    def discard_all_changes(self, repository: str) -> None:
        self.run_program_argsasarray("git", ["reset", "HEAD", "."], repository, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)
        self.run_program_argsasarray("git", ["checkout", "."], repository, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)

    @GeneralUtilities.check_arguments
    def git_get_current_branch_name(self, repository: str) -> str:
        result = self.run_program_argsasarray("git", ["rev-parse", "--abbrev-ref", "HEAD"], repository, throw_exception_if_exitcode_is_not_zero=True, verbosity=0)
        return result[1].replace("\r", "").replace("\n", "")

    @GeneralUtilities.check_arguments
    def export_filemetadata(self, folder: str, target_file: str, encoding: str = "utf-8", filter_function=None) -> None:
        folder = GeneralUtilities.resolve_relative_path_from_current_working_directory(folder)
        lines = list()
        path_prefix = len(folder)+1
        items = dict()
        for item in GeneralUtilities.get_all_files_of_folder(folder):
            items[item] = "f"
        for item in GeneralUtilities.get_all_folders_of_folder(folder):
            items[item] = "d"
        for file_or_folder, item_type in items.items():
            truncated_file = file_or_folder[path_prefix:]
            if(filter_function is None or filter_function(folder, truncated_file)):
                owner_and_permisssion = self.get_file_owner_and_file_permission(file_or_folder)
                user = owner_and_permisssion[0]
                permissions = owner_and_permisssion[1]
                lines.append(f"{truncated_file};{item_type};{user};{permissions}")
        lines = sorted(lines, key=str.casefold)
        with open(target_file, "w", encoding=encoding) as file_object:
            file_object.write("\n".join(lines))

    @GeneralUtilities.check_arguments
    def restore_filemetadata(self, folder: str, source_file: str, strict=False, encoding: str = "utf-8") -> None:
        for line in GeneralUtilities.read_lines_from_file(source_file, encoding):
            splitted: list = line.split(";")
            full_path_of_file_or_folder: str = os.path.join(folder, splitted[0])
            filetype: str = splitted[1]
            user: str = splitted[2]
            permissions: str = splitted[3]
            if (filetype == "f" and os.path.isfile(full_path_of_file_or_folder)) or (filetype == "d" and os.path.isdir(full_path_of_file_or_folder)):
                self.set_owner(full_path_of_file_or_folder, user, os.name != 'nt')
                self.set_permission(full_path_of_file_or_folder, permissions)
            else:
                if strict:
                    if filetype == "f":
                        filetype_full = "File"
                    if filetype == "d":
                        filetype_full = "Directory"
                    raise Exception(f"{filetype_full} '{full_path_of_file_or_folder}' does not exist")

    @GeneralUtilities.check_arguments
    def __verbose_check_for_not_available_item(self, configparser: ConfigParser, queried_items: list, section: str, propertyname: str) -> None:
        if self.__get_verbosity_for_exuecutor(configparser) > 0:
            for item in queried_items:
                self.__check_for_not_available_config_item(item, section, propertyname)

    @GeneralUtilities.check_arguments
    def __check_for_not_available_config_item(self, item, section: str, propertyname: str):
        if item == "<notavailable>":
            GeneralUtilities.write_message_to_stderr(f"Warning: The property '{section}.{propertyname}' which is not available was queried. "
                                                     + "This may result in errors or involuntary behavior")
            GeneralUtilities.print_stacktrace()

    @GeneralUtilities.check_arguments
    def __get_verbosity_for_exuecutor(self, configparser: ConfigParser) -> int:
        return self.get_number_value_from_configuration(configparser, 'other', 'verbose')

    @GeneralUtilities.check_arguments
    def __get_buildoutputdirectory(self, configparser: ConfigParser, runtime: str, current_release_information: dict[str, str]) -> str:
        result = self.get_item_from_configuration(configparser, 'dotnet', 'buildoutputdirectory', current_release_information)
        if self.get_boolean_value_from_configuration(configparser, 'dotnet', 'separatefolderforeachruntime', current_release_information):
            result = result+os.path.sep+runtime
        return result

    @GeneralUtilities.check_arguments
    def get_boolean_value_from_configuration(self, configparser: ConfigParser, section: str, propertyname: str, current_release_information: dict[str, str]) -> bool:
        try:
            value = configparser.get(section, propertyname)
            self.__check_for_not_available_config_item(value, section, propertyname)
            return configparser.getboolean(section, propertyname)
        except:
            try:
                return GeneralUtilities.string_to_boolean(self.get_item_from_configuration(configparser, section, propertyname, current_release_information))
            except:
                return False

    @GeneralUtilities.check_arguments
    def get_number_value_from_configuration(self, configparser: ConfigParser, section: str, propertyname: str) -> int:
        value = configparser.get(section, propertyname)
        self.__check_for_not_available_config_item(value, section, propertyname)
        return int(value)

    @GeneralUtilities.check_arguments
    def configuration_item_is_available(self, configparser: ConfigParser, sectioon: str, item: str) -> bool:
        if not configparser.has_option(sectioon, item):
            return False
        plain_value = configparser.get(sectioon, item)
        if GeneralUtilities.string_is_none_or_whitespace(plain_value):
            return False
        if plain_value == "<notavailable>":
            return False
        return True

    @GeneralUtilities.check_arguments
    def __calculate_version(self, configparser: ConfigParser, current_release_information: dict[str, str]) -> None:
        if "builtin.version" not in current_release_information:
            current_release_information['builtin.version'] = self.get_semver_version_from_gitversion(
                self.get_item_from_configuration(configparser, 'general', 'repository', current_release_information))

    @GeneralUtilities.check_arguments
    def get_item_from_configuration(self, configparser: ConfigParser, section: str, propertyname: str, current_release_information: dict[str, str]) -> str:

        now = datetime.now()
        current_release_information["builtin.year"] = str(now.year)
        current_release_information["builtin.month"] = str(now.month)
        current_release_information["builtin.day"] = str(now.day)

        result = self.__replace_underscores_for_buildconfiguration(f"__.{section}.{propertyname}.__", configparser, current_release_information)
        result = GeneralUtilities.strip_new_line_character(result)
        self.__verbose_check_for_not_available_item(configparser, [result], section, propertyname)
        return result

    @GeneralUtilities.check_arguments
    def get_items_from_configuration(self, configparser: ConfigParser, section: str, propertyname: str, current_release_information: dict[str, str]) -> list[str]:
        itemlist_as_string = self.__replace_underscores_for_buildconfiguration(f"__.{section}.{propertyname}.__", configparser, current_release_information)
        if not GeneralUtilities.string_has_content(itemlist_as_string):
            return []
        if ',' in itemlist_as_string:
            result = [item.strip() for item in itemlist_as_string.split(',')]
        else:
            result = [itemlist_as_string.strip()]
        self.__verbose_check_for_not_available_item(configparser, result, section, propertyname)
        return result

    @GeneralUtilities.check_arguments
    def __get_csprojfile_filename(self, configparser: ConfigParser, current_release_information: dict[str, str]) -> str:
        file = self.get_item_from_configuration(configparser, "dotnet", "csprojfile", current_release_information)
        file = GeneralUtilities.resolve_relative_path_from_current_working_directory(file)
        result = os.path.basename(file)
        return result

    @GeneralUtilities.check_arguments
    def __get_csprojfile_folder(self, configparser: ConfigParser, current_release_information: dict[str, str]) -> str:
        file = self.get_item_from_configuration(configparser, "dotnet", "csprojfile", current_release_information)
        file = GeneralUtilities.resolve_relative_path_from_current_working_directory(file)
        result = os.path.dirname(file)
        return result

    @GeneralUtilities.check_arguments
    def get_version_for_buildscripts(self, configparser: ConfigParser, current_release_information: dict[str, str]) -> str:
        return self.get_item_from_configuration(configparser, 'builtin', 'version', current_release_information)

    @GeneralUtilities.check_arguments
    def __replace_underscores_for_buildconfiguration(self, string: str, configparser: ConfigParser, current_release_information: dict[str, str]) -> str:
        # TODO improve performance: the content of this function must mostly be executed once at the begining of a create-release-process, not always again

        available_configuration_items = []

        available_configuration_items.append(["docker", "artefactdirectory"])
        available_configuration_items.append(["docker", "contextfolder"])
        available_configuration_items.append(["docker", "dockerfile"])
        available_configuration_items.append(["docker", "registryaddress"])
        available_configuration_items.append(["dotnet", "csprojfile"])
        available_configuration_items.append(["dotnet", "buildoutputdirectory"])
        available_configuration_items.append(["dotnet", "publishdirectory"])
        available_configuration_items.append(["dotnet", "runtimes"])
        available_configuration_items.append(["dotnet", "dotnetframework"])
        available_configuration_items.append(["dotnet", "buildconfiguration"])
        available_configuration_items.append(["dotnet", "filestosign"])
        available_configuration_items.append(["dotnet", "snkfile"])
        available_configuration_items.append(["dotnet", "testdotnetframework"])
        available_configuration_items.append(["dotnet", "localnugettargets"])
        available_configuration_items.append(["dotnet", "testbuildconfiguration"])
        available_configuration_items.append(["dotnet", "docfxfile"])
        available_configuration_items.append(["dotnet", "coveragefolder"])
        available_configuration_items.append(["dotnet", "coveragereportfolder"])
        available_configuration_items.append(["dotnet", "referencerepository"])
        available_configuration_items.append(["dotnet", "nugetsource"])
        available_configuration_items.append(["dotnet", "iconfile"])
        available_configuration_items.append(["dotnet", "nugetapikeyfile"])
        available_configuration_items.append(["general", "productname"])
        available_configuration_items.append(["general", "basefolder"])
        available_configuration_items.append(["general", "logfilefolder"])
        available_configuration_items.append(["general", "repository"])
        available_configuration_items.append(["general", "author"])
        available_configuration_items.append(["general", "description"])
        available_configuration_items.append(["prepare", "sourcebranchname"])
        available_configuration_items.append(["prepare", "targetbranchname"])
        available_configuration_items.append(["prepare", "gittagprefix"])
        available_configuration_items.append(["script", "premerge_program"])
        available_configuration_items.append(["script", "premerge_argument"])
        available_configuration_items.append(["script", "premerge_argument"])
        available_configuration_items.append(["script", "postmerge_program"])
        available_configuration_items.append(["script", "postmerge_argument"])
        available_configuration_items.append(["script", "postmerge_workingdirectory"])
        available_configuration_items.append(["other", "exportreferenceremotename"])
        available_configuration_items.append(["other", "exportreferencelocalbranchname"])
        available_configuration_items.append(["other", "releaserepository"])
        available_configuration_items.append(["other", "gpgidentity"])
        available_configuration_items.append(["other", "projecturl"])
        available_configuration_items.append(["other", "repositoryurl"])
        available_configuration_items.append(["other", "exportrepositoryremotename"])
        available_configuration_items.append(["other", "runtestcasesscript"])
        available_configuration_items.append(["python", "readmefile"])
        available_configuration_items.append(["python", "pythonsetuppyfile"])
        available_configuration_items.append(["python", "filesforupdatingversion"])
        available_configuration_items.append(["python", "pypiapikeyfile"])
        available_configuration_items.append(["python", "publishdirectoryforwhlfile"])

        for item in available_configuration_items:
            if configparser.has_option(item[0], item[1]):
                current_release_information[f"{item[0]}.{item[1]}"] = configparser.get(item[0], item[1])

        changed = True
        result = string
        while changed:
            changed = False
            for key, value in current_release_information.items():
                previousValue = result
                result = result.replace(f"__.{key}.__", str(value))
                if(not result == previousValue):
                    changed = True

        return result

    @GeneralUtilities.check_arguments
    def __create_dotnet_release_premerge(self, configurationfile: str, current_release_information: dict[str, str]):
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        if self.get_boolean_value_from_configuration(configparser, 'dotnet', 'createexe', current_release_information):
            self.dotnet_create_executable_release_premerge(configurationfile, current_release_information)
        else:
            self.dotnet_create_nuget_release_premerge(configurationfile, current_release_information)

    @GeneralUtilities.check_arguments
    def __create_dotnet_release_postmerge(self, configurationfile: str, current_release_information: dict[str, str]):
        configparser = ConfigParser()
        with(open(configurationfile, mode="r", encoding="utf-8")) as text_io_wrapper:
            configparser.read_file(text_io_wrapper)
        if self.get_boolean_value_from_configuration(configparser, 'dotnet', 'createexe', current_release_information):
            self.dotnet_create_executable_release_postmerge(configurationfile, current_release_information)
        else:
            self.dotnet_create_nuget_release_postmerge(configurationfile, current_release_information)

    @GeneralUtilities.check_arguments
    def __calculate_lengh_in_seconds(self, filename: str, folder: str) -> float:
        argument = f'-v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{filename}"'
        return float(self.run_program("ffprobe", argument, folder)[1])

    @GeneralUtilities.check_arguments
    def __create_thumbnails(self, filename: str, fps: float, folder: str, tempname_for_thumbnails: str) -> None:
        argument = f'-i "{filename}" -r {str(fps)} -vf scale=-1:120 -vcodec png {tempname_for_thumbnails}-%002d.png'
        self.run_program("ffmpeg", argument, folder)

    @GeneralUtilities.check_arguments
    def __create_thumbnail(self, outputfilename: str, folder: str, length_in_seconds: float, tempname_for_thumbnails: str, amount_of_images: int) -> None:
        duration = timedelta(seconds=length_in_seconds)
        info = GeneralUtilities.timedelta_to_simple_string(duration)
        next_square_number = str(int(math.sqrt(GeneralUtilities.get_next_square_number(amount_of_images))))
        argument = f'-title "{outputfilename} ({info})" -geometry +{next_square_number}+{next_square_number} {tempname_for_thumbnails}*.png "{outputfilename}.png"'
        self.run_program("montage", argument, folder)

    @GeneralUtilities.check_arguments
    def generate_thumbnail(self, file: str, frames_per_second: str, tempname_for_thumbnails: str = None) -> None:
        if tempname_for_thumbnails is None:
            tempname_for_thumbnails = "t"+str(uuid.uuid4())

        file = GeneralUtilities.resolve_relative_path_from_current_working_directory(file)
        filename = os.path.basename(file)
        folder = os.path.dirname(file)
        filename_without_extension = Path(file).stem

        try:
            length_in_seconds = self.__calculate_lengh_in_seconds(filename, folder)
            if(frames_per_second.endswith("fps")):
                # frames per second, example: frames_per_second="20fps" => 20 frames per second
                frames_per_second = round(float(frames_per_second[:-3]), 2)
                amounf_of_previewframes = int(math.floor(length_in_seconds*frames_per_second))
            else:
                # concrete amount of frame, examples: frames_per_second="16" => 16 frames for entire video
                amounf_of_previewframes = int(float(frames_per_second))
                frames_per_second = round(amounf_of_previewframes/length_in_seconds, 2)
            self.__create_thumbnails(filename, frames_per_second, folder, tempname_for_thumbnails)
            self.__create_thumbnail(filename_without_extension, folder, length_in_seconds, tempname_for_thumbnails, amounf_of_previewframes)
        finally:
            for thumbnail_to_delete in Path(folder).rglob(tempname_for_thumbnails+"-*"):
                file = str(thumbnail_to_delete)
                os.remove(file)

    @GeneralUtilities.check_arguments
    def merge_pdf_files(self, files, outputfile: str) -> None:
        # TODO add wildcard-option
        pdfFileMerger = PdfFileMerger()
        for file in files:
            pdfFileMerger.append(file.strip())
        pdfFileMerger.write(outputfile)
        pdfFileMerger.close()
        return 0

    @GeneralUtilities.check_arguments
    def SCShowMissingFiles(self, folderA: str, folderB: str):
        for file in GeneralUtilities.get_missing_files(folderA, folderB):
            GeneralUtilities.write_message_to_stdout(file)

    @GeneralUtilities.check_arguments
    def SCCreateEmptyFileWithSpecificSize(self, name: str, size_string: str) -> int:
        if size_string.isdigit():
            size = int(size_string)
        else:
            if len(size_string) >= 3:
                if(size_string.endswith("kb")):
                    size = int(size_string[:-2]) * pow(10, 3)
                elif(size_string.endswith("mb")):
                    size = int(size_string[:-2]) * pow(10, 6)
                elif(size_string.endswith("gb")):
                    size = int(size_string[:-2]) * pow(10, 9)
                elif(size_string.endswith("kib")):
                    size = int(size_string[:-3]) * pow(2, 10)
                elif(size_string.endswith("mib")):
                    size = int(size_string[:-3]) * pow(2, 20)
                elif(size_string.endswith("gib")):
                    size = int(size_string[:-3]) * pow(2, 30)
                else:
                    GeneralUtilities.write_message_to_stderr("Wrong format")
            else:
                GeneralUtilities.write_message_to_stderr("Wrong format")
                return 1
        with open(name, "wb") as f:
            f.seek(size-1)
            f.write(b"\0")
        return 0

    @GeneralUtilities.check_arguments
    def SCCreateHashOfAllFiles(self, folder: str) -> None:
        for file in GeneralUtilities.absolute_file_paths(folder):
            with open(file+".sha256", "w+", encoding="utf-8") as f:
                f.write(GeneralUtilities.get_sha256_of_file(file))

    @GeneralUtilities.check_arguments
    def SCCreateSimpleMergeWithoutRelease(self, repository: str, sourcebranch: str, targetbranch: str, remotename: str, remove_source_branch: bool) -> None:
        commitid = self.git_merge(repository, sourcebranch, targetbranch, False, True)
        self.git_merge(repository, targetbranch, sourcebranch, True, True)
        created_version = self.get_semver_version_from_gitversion(repository)
        self.git_create_tag(repository, commitid, f"v{created_version}", True)
        self.git_push(repository, remotename, targetbranch, targetbranch, False, True)
        if (GeneralUtilities.string_has_nonwhitespace_content(remotename)):
            self.git_push(repository, remotename, sourcebranch, sourcebranch, False, True)
        if(remove_source_branch):
            self.git_remove_branch(repository, sourcebranch)

    @GeneralUtilities.check_arguments
    def sc_organize_lines_in_file(self, file: str, encoding: str, sort: bool = False, remove_duplicated_lines: bool = False, ignore_first_line: bool = False,
                                  remove_empty_lines: bool = True, ignored_start_character: list = list()) -> int:
        if os.path.isfile(file):

            # read file
            lines = GeneralUtilities.read_lines_from_file(file, encoding)
            if(len(lines) == 0):
                return 0

            # store first line if desiredpopd

            if(ignore_first_line):
                first_line = lines.pop(0)

            # remove empty lines if desired
            if remove_empty_lines:
                temp = lines
                lines = []
                for line in temp:
                    if(not (GeneralUtilities.string_is_none_or_whitespace(line))):
                        lines.append(line)

            # remove duplicated lines if desired
            if remove_duplicated_lines:
                lines = GeneralUtilities.remove_duplicates(lines)

            # sort lines if desired
            if sort:
                lines = sorted(lines, key=lambda singleline: self.__adapt_line_for_sorting(singleline, ignored_start_character))

            # reinsert first line
            if ignore_first_line:
                lines.insert(0, first_line)

            # write result to file
            GeneralUtilities.write_lines_to_file(file, lines, encoding)

            return 0
        else:
            GeneralUtilities.write_message_to_stdout(f"File '{file}' does not exist")
            return 1

    @GeneralUtilities.check_arguments
    def __adapt_line_for_sorting(self, line: str, ignored_start_characters: list):
        result = line.lower()
        while len(result) > 0 and result[0] in ignored_start_characters:
            result = result[1:]
        return result

    @GeneralUtilities.check_arguments
    def SCGenerateSnkFiles(self, outputfolder, keysize=4096, amountofkeys=10) -> int:
        GeneralUtilities.ensure_directory_exists(outputfolder)
        for _ in range(amountofkeys):
            file = os.path.join(outputfolder, str(uuid.uuid4())+".snk")
            argument = f"-k {keysize} {file}"
            self.run_program("sn", argument, outputfolder)

    @GeneralUtilities.check_arguments
    def __merge_files(self, sourcefile: str, targetfile: str) -> None:
        with open(sourcefile, "rb") as f:
            source_data = f.read()
        with open(targetfile, "ab") as fout:
            merge_separator = [0x0A]
            fout.write(bytes(merge_separator))
            fout.write(source_data)

    @GeneralUtilities.check_arguments
    def __process_file(self, file: str, substringInFilename: str, newSubstringInFilename: str, conflictResolveMode: str) -> None:
        new_filename = os.path.join(os.path.dirname(file), os.path.basename(file).replace(substringInFilename, newSubstringInFilename))
        if file != new_filename:
            if os.path.isfile(new_filename):
                if filecmp.cmp(file, new_filename):
                    send2trash.send2trash(file)
                else:
                    if conflictResolveMode == "ignore":
                        pass
                    elif conflictResolveMode == "preservenewest":
                        if(os.path.getmtime(file) - os.path.getmtime(new_filename) > 0):
                            send2trash.send2trash(file)
                        else:
                            send2trash.send2trash(new_filename)
                            os.rename(file, new_filename)
                    elif(conflictResolveMode == "merge"):
                        self.__merge_files(file, new_filename)
                        send2trash.send2trash(file)
                    else:
                        raise Exception('Unknown conflict resolve mode')
            else:
                os.rename(file, new_filename)

    @GeneralUtilities.check_arguments
    def SCReplaceSubstringsInFilenames(self, folder: str, substringInFilename: str, newSubstringInFilename: str, conflictResolveMode: str) -> None:
        for file in GeneralUtilities.absolute_file_paths(folder):
            self.__process_file(file, substringInFilename, newSubstringInFilename, conflictResolveMode)

    @GeneralUtilities.check_arguments
    def __check_file(self, file: str, searchstring: str) -> None:
        bytes_ascii = bytes(searchstring, "ascii")
        bytes_utf16 = bytes(searchstring, "utf-16")  # often called "unicode-encoding"
        bytes_utf8 = bytes(searchstring, "utf-8")
        with open(file, mode='rb') as file_object:
            content = file_object.read()
            if bytes_ascii in content:
                GeneralUtilities.write_message_to_stdout(file)
            elif bytes_utf16 in content:
                GeneralUtilities.write_message_to_stdout(file)
            elif bytes_utf8 in content:
                GeneralUtilities.write_message_to_stdout(file)

    @GeneralUtilities.check_arguments
    def SCSearchInFiles(self, folder: str, searchstring: str) -> None:
        for file in GeneralUtilities.absolute_file_paths(folder):
            self.__check_file(file, searchstring)

    @GeneralUtilities.check_arguments
    def __print_qr_code_by_csv_line(self, displayname, website, emailaddress, key, period) -> None:
        qrcode_content = f"otpauth://totp/{website}:{emailaddress}?secret={key}&issuer={displayname}&period={period}"
        GeneralUtilities.write_message_to_stdout(f"{displayname} ({emailaddress}):")
        GeneralUtilities.write_message_to_stdout(qrcode_content)
        self.run_program("qr", [qrcode_content])

    @GeneralUtilities.check_arguments
    def SCShow2FAAsQRCode(self, csvfile: str) -> None:
        separator_line = "--------------------------------------------------------"
        for line in GeneralUtilities.read_csv_file(csvfile, True):
            GeneralUtilities.write_message_to_stdout(separator_line)
            self.__print_qr_code_by_csv_line(line[0], line[1], line[2], line[3], line[4])
        GeneralUtilities.write_message_to_stdout(separator_line)

    @GeneralUtilities.check_arguments
    def SCUpdateNugetpackagesInCsharpProject(self, csprojfile: str) -> int:
        outdated_packages = self.get_nuget_packages_of_csproj_file(csprojfile, True)
        GeneralUtilities.write_message_to_stdout("The following packages will be updated:")
        for outdated_package in outdated_packages:
            GeneralUtilities.write_message_to_stdout(outdated_package)
            self.update_nuget_package(csprojfile, outdated_package)
        GeneralUtilities.write_message_to_stdout(f"{len(outdated_packages)} package(s) were updated")
        return len(outdated_packages) > 0

    @GeneralUtilities.check_arguments
    def SCUploadFileToFileHost(self, file: str, host: str) -> int:
        try:
            GeneralUtilities.write_message_to_stdout(self.upload_file_to_file_host(file, host))
            return 0
        except Exception as exception:
            GeneralUtilities.write_exception_to_stderr_with_traceback(exception, traceback)
            return 1

    @GeneralUtilities.check_arguments
    def SCFileIsAvailableOnFileHost(self, file: str) -> int:
        try:
            if self.file_is_available_on_file_host(file):
                GeneralUtilities.write_message_to_stdout(f"'{file}' is available")
                return 0
            else:
                GeneralUtilities.write_message_to_stdout(f"'{file}' is not available")
                return 1
        except Exception as exception:
            GeneralUtilities.write_exception_to_stderr_with_traceback(exception, traceback)
            return 2

    @GeneralUtilities.check_arguments
    def SCCalculateBitcoinBlockHash(self, block_version_number: str, previousblockhash: str, transactionsmerkleroot: str, timestamp: str, target: str, nonce: str) -> str:
        # Example-values:
        # block_version_number: "00000020"
        # previousblockhash: "66720b99e07d284bd4fe67ff8c49a5db1dd8514fcdab61000000000000000000"
        # transactionsmerkleroot: "7829844f4c3a41a537b3131ca992643eaa9d093b2383e4cdc060ad7dc5481187"
        # timestamp: "51eb505a"
        # target: "c1910018"
        # nonce: "de19b302"
        header = str(block_version_number + previousblockhash + transactionsmerkleroot + timestamp + target + nonce)
        return binascii.hexlify(hashlib.sha256(hashlib.sha256(binascii.unhexlify(header)).digest()).digest()[::-1]).decode('utf-8')

    @GeneralUtilities.check_arguments
    def SCChangeHashOfProgram(self, inputfile: str) -> None:
        valuetoappend = str(uuid.uuid4())

        outputfile = inputfile + '.modified'

        shutil.copy2(inputfile, outputfile)
        with open(outputfile, 'a', encoding="utf-8") as file:
            # TODO use rcedit for .exe-files instead of appending valuetoappend ( https://github.com/electron/rcedit/ )
            # background: you can retrieve the "original-filename" from the .exe-file like discussed here:
            # https://security.stackexchange.com/questions/210843/ is-it-possible-to-change-original-filename-of-an-exe
            # so removing the original filename with rcedit is probably a better way to make it more difficult to detect the programname.
            # this would obviously also change the hashvalue of the program so appending a whitespace is not required anymore.
            file.write(valuetoappend)

    @GeneralUtilities.check_arguments
    def __adjust_folder_name(self, folder: str) -> str:
        result = os.path.dirname(folder).replace("\\", "/")
        if result == "/":
            return ""
        else:
            return result

    @GeneralUtilities.check_arguments
    def __create_iso(self, folder, iso_file) -> None:
        created_directories = []
        files_directory = "FILES"
        iso = pycdlib.PyCdlib()
        iso.new()
        files_directory = files_directory.upper()
        iso.add_directory("/" + files_directory)
        created_directories.append("/" + files_directory)
        for root, _, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)
                with(open(full_path, "rb").read()) as text_io_wrapper:
                    content = text_io_wrapper
                    path_in_iso = '/' + files_directory + self.__adjust_folder_name(full_path[len(folder)::1]).upper()
                    if path_in_iso not in created_directories:
                        iso.add_directory(path_in_iso)
                        created_directories.append(path_in_iso)
                    iso.add_fp(BytesIO(content), len(content), path_in_iso + '/' + file.upper() + ';1')
        iso.write(iso_file)
        iso.close()

    @GeneralUtilities.check_arguments
    def SCCreateISOFileWithObfuscatedFiles(self, inputfolder: str, outputfile: str, printtableheadline, createisofile, extensions) -> None:
        if (os.path.isdir(inputfolder)):
            namemappingfile = "name_map.csv"
            files_directory = inputfolder
            files_directory_obf = files_directory + "_Obfuscated"
            self.SCObfuscateFilesFolder(inputfolder, printtableheadline, namemappingfile, extensions)
            os.rename(namemappingfile, os.path.join(files_directory_obf, namemappingfile))
            if createisofile:
                self.__create_iso(files_directory_obf, outputfile)
                shutil.rmtree(files_directory_obf)
        else:
            raise Exception(f"Directory not found: '{inputfolder}'")

    @GeneralUtilities.check_arguments
    def SCFilenameObfuscator(self, inputfolder: str, printtableheadline, namemappingfile: str, extensions: str) -> None:
        obfuscate_all_files = extensions == "*"
        if(not obfuscate_all_files):
            obfuscate_file_extensions = extensions.split(",")

        if (os.path.isdir(inputfolder)):
            printtableheadline = GeneralUtilities.string_to_boolean(printtableheadline)
            files = []
            if not os.path.isfile(namemappingfile):
                with open(namemappingfile, "a", encoding="utf-8"):
                    pass
            if printtableheadline:
                GeneralUtilities.append_line_to_file(namemappingfile, "Original filename;new filename;SHA2-hash of file")
            for file in GeneralUtilities.absolute_file_paths(inputfolder):
                if os.path.isfile(os.path.join(inputfolder, file)):
                    if obfuscate_all_files or self.__extension_matchs(file, obfuscate_file_extensions):
                        files.append(file)
            for file in files:
                hash_value = GeneralUtilities.get_sha256_of_file(file)
                extension = Path(file).suffix
                new_file_name_without_path = str(uuid.uuid4())[0:8] + extension
                new_file_name = os.path.join(os.path.dirname(file), new_file_name_without_path)
                os.rename(file, new_file_name)
                GeneralUtilities.append_line_to_file(namemappingfile, os.path.basename(file) + ";" + new_file_name_without_path + ";" + hash_value)
        else:
            raise Exception(f"Directory not found: '{inputfolder}'")

    @GeneralUtilities.check_arguments
    def __extension_matchs(self, file: str, obfuscate_file_extensions) -> bool:
        for extension in obfuscate_file_extensions:
            if file.lower().endswith("."+extension.lower()):
                return True
        return False

    @GeneralUtilities.check_arguments
    def SCHealthcheck(self, file: str) -> int:
        lines = GeneralUtilities.read_lines_from_file(file)
        for line in reversed(lines):
            if not GeneralUtilities.string_is_none_or_whitespace(line):
                if "RunningHealthy (" in line:  # TODO use regex
                    GeneralUtilities.write_message_to_stderr(f"Healthy running due to line '{line}' in file '{file}'.")
                    return 0
                else:
                    GeneralUtilities.write_message_to_stderr(f"Not healthy running due to line '{line}' in file '{file}'.")
                    return 1
        GeneralUtilities.write_message_to_stderr(f"No valid line found for healthycheck in file '{file}'.")
        return 2

    @GeneralUtilities.check_arguments
    def SCObfuscateFilesFolder(self, inputfolder: str, printtableheadline, namemappingfile: str, extensions: str) -> None:
        obfuscate_all_files = extensions == "*"
        if(not obfuscate_all_files):
            if "," in extensions:
                obfuscate_file_extensions = extensions.split(",")
            else:
                obfuscate_file_extensions = [extensions]
        newd = inputfolder+"_Obfuscated"
        shutil.copytree(inputfolder, newd)
        inputfolder = newd
        if (os.path.isdir(inputfolder)):
            for file in GeneralUtilities.absolute_file_paths(inputfolder):
                if obfuscate_all_files or self.__extension_matchs(file, obfuscate_file_extensions):
                    self.SCChangeHashOfProgram(file)
                    os.remove(file)
                    os.rename(file + ".modified", file)
            self.SCFilenameObfuscator(inputfolder, printtableheadline, namemappingfile, extensions)
        else:
            raise Exception(f"Directory not found: '{inputfolder}'")

    @GeneralUtilities.check_arguments
    def upload_file_to_file_host(self, file: str, host: str) -> int:
        if(host is None):
            return self.upload_file_to_random_filesharing_service(file)
        elif host == "anonfiles.com":
            return self.upload_file_to_anonfiles(file)
        elif host == "bayfiles.com":
            return self.upload_file_to_bayfiles(file)
        GeneralUtilities.write_message_to_stderr("Unknown host: "+host)
        return 1

    @GeneralUtilities.check_arguments
    def upload_file_to_random_filesharing_service(self, file: str) -> int:
        host = randrange(2)
        if host == 0:
            return self.upload_file_to_anonfiles(file)
        if host == 1:
            return self.upload_file_to_bayfiles(file)
        return 1

    @GeneralUtilities.check_arguments
    def upload_file_to_anonfiles(self, file) -> int:
        return self.upload_file_by_using_simple_curl_request("https://api.anonfiles.com/upload", file)

    @GeneralUtilities.check_arguments
    def upload_file_to_bayfiles(self, file) -> int:
        return self.upload_file_by_using_simple_curl_request("https://api.bayfiles.com/upload", file)

    @GeneralUtilities.check_arguments
    def upload_file_by_using_simple_curl_request(self, api_url: str, file: str) -> int:
        # TODO implement
        return 1

    @GeneralUtilities.check_arguments
    def file_is_available_on_file_host(self, file) -> int:
        # TODO implement
        return 1

    def run_testcases_for_python_project(self, repository_folder: str):
        self.run_program("coverage", "run -m pytest", repository_folder)
        self.run_program("coverage", "xml", repository_folder)
        GeneralUtilities.ensure_directory_exists(os.path.join(repository_folder, "Other/TestCoverage"))
        coveragefile = os.path.join(repository_folder, "Other/TestCoverage/TestCoverage.xml")
        GeneralUtilities.ensure_file_does_not_exist(coveragefile)
        os.rename(os.path.join(repository_folder, "coverage.xml"), coveragefile)

    @GeneralUtilities.check_arguments
    def get_nuget_packages_of_csproj_file(self, csproj_file: str, only_outdated_packages: bool) -> bool:
        self.run_program("dotnet", f'restore --disable-parallel --force --force-evaluate "{csproj_file}"')
        if only_outdated_packages:
            only_outdated_packages_argument = " --outdated"
        else:
            only_outdated_packages_argument = ""
        stdout = self.run_program("dotnet", f'list "{csproj_file}" package{only_outdated_packages_argument}')[1]
        result = []
        for line in stdout.splitlines():
            trimmed_line = line.replace("\t", "").strip()
            if trimmed_line.startswith(">"):
                result.append(trimmed_line[2:].split(" ")[0])
        return result

    @GeneralUtilities.check_arguments
    def update_nuget_package(self, csproj_file: str, name: str) -> None:
        self.run_program("dotnet", f'add "{csproj_file}" package {name}')

    @GeneralUtilities.check_arguments
    def get_file_permission(self, file: str) -> str:
        """This function returns an usual octet-triple, for example "0700"."""
        ls_output = self.__ls(file)
        return self.__get_file_permission_helper(ls_output)

    @GeneralUtilities.check_arguments
    def __get_file_permission_helper(self, ls_output: str) -> str:
        permissions = ' '.join(ls_output.split()).split(' ')[0][1:]
        return str(self.__to_octet(permissions[0:3]))+str(self.__to_octet(permissions[3:6]))+str(self.__to_octet(permissions[6:9]))

    @GeneralUtilities.check_arguments
    def __to_octet(self, string: str) -> int:
        return int(self.__to_octet_helper(string[0])+self.__to_octet_helper(string[1])+self.__to_octet_helper(string[2]), 2)

    @GeneralUtilities.check_arguments
    def __to_octet_helper(self, string: str) -> str:
        if(string == "-"):
            return "0"
        else:
            return "1"

    @GeneralUtilities.check_arguments
    def get_file_owner(self, file: str) -> str:
        """This function returns the user and the group in the format "user:group"."""
        ls_output = self.__ls(file)
        return self.__get_file_owner_helper(ls_output)

    @GeneralUtilities.check_arguments
    def __get_file_owner_helper(self, ls_output: str) -> str:
        try:
            splitted = ' '.join(ls_output.split()).split(' ')
            return f"{splitted[2]}:{splitted[3]}"
        except Exception as exception:
            raise ValueError(f"ls-output '{ls_output}' not parsable") from exception

    @GeneralUtilities.check_arguments
    def get_file_owner_and_file_permission(self, file: str) -> str:
        ls_output = self.__ls(file)
        return [self.__get_file_owner_helper(ls_output), self.__get_file_permission_helper(ls_output)]

    @GeneralUtilities.check_arguments
    def __ls(self, file: str) -> str:
        file = file.replace("\\", "/")
        GeneralUtilities.assert_condition(os.path.isfile(file) or os.path.isdir(file), f"Can not execute 'ls' because '{file}' does not exist")
        result = self.run_program_argsasarray("ls", ["-ld", file])
        GeneralUtilities.assert_condition(result[0] == 0, f"'ls -ld {file}' resulted in exitcode {str(result[0])}. StdErr: {result[2]}")
        GeneralUtilities.assert_condition(not GeneralUtilities.string_is_none_or_whitespace(result[1]), f"'ls' of '{file}' had an empty output. StdErr: '{result[2]}'")
        return result[1]

    @GeneralUtilities.check_arguments
    def set_permission(self, file_or_folder: str, permissions: str, recursive: bool = False) -> None:
        """This function expects an usual octet-triple, for example "700"."""
        args = []
        if recursive:
            args.append("--recursive")
        args.append(permissions)
        args.append(file_or_folder)
        self.run_program_argsasarray("chmod", args)

    @GeneralUtilities.check_arguments
    def set_owner(self, file_or_folder: str, owner: str, recursive: bool = False, follow_symlinks: bool = False) -> None:
        """This function expects the user and the group in the format "user:group"."""
        args = []
        if recursive:
            args.append("--recursive")
        if follow_symlinks:
            args.append("--no-dereference")
        args.append(owner)
        args.append(file_or_folder)
        self.run_program_argsasarray("chown", args)

    # <run programs>

    @GeneralUtilities.check_arguments
    def __run_program_argsasarray_async_helper(self, program: str, arguments_as_array: list[str] = [], working_directory: str = None, verbosity: int = 1,
                                               print_errors_as_information: bool = False, log_file: str = None, timeoutInSeconds: int = 600, addLogOverhead: bool = False,
                                               title: str = None, log_namespace: str = "", arguments_for_log:  list[str] = None) -> Popen:
        # Verbosity:
        # 0=Quiet (No output will be printed.)
        # 1=Normal (If the exitcode of the executed program is not 0 then the StdErr will be printed.)
        # 2=Full (Prints StdOut and StdErr of the executed program.)
        # 3=Verbose (Same as "Full" but with some more information.)

        if arguments_for_log is None:
            arguments_for_log = ' '.join(arguments_as_array)
        else:
            arguments_for_log = ' '.join(arguments_for_log)
        working_directory = self.__adapt_workingdirectory(working_directory)
        cmd = f'{working_directory}>{program} {arguments_for_log}'

        if GeneralUtilities.string_is_none_or_whitespace(title):
            info_for_log = cmd
        else:
            info_for_log = title

        if verbosity == 3:
            GeneralUtilities.write_message_to_stdout(f"Run '{info_for_log}'.")

        if isinstance(self.program_runner, ProgramRunnerEpew):
            custom_argument = CustomEpewArgument(print_errors_as_information, log_file, timeoutInSeconds, addLogOverhead, title, log_namespace, verbosity, arguments_for_log)
        else:
            custom_argument = None
        popen: Popen = self.program_runner.run_program_argsasarray_async_helper(program, arguments_as_array, working_directory, custom_argument)
        return popen

    # Return-values program_runner: Exitcode, StdOut, StdErr, Pid

    @GeneralUtilities.check_arguments
    def run_program_argsasarray(self, program: str, arguments_as_array: list[str] = [], working_directory: str = None, verbosity: int = 1,
                                print_errors_as_information: bool = False, log_file: str = None, timeoutInSeconds: int = 600, addLogOverhead: bool = False,
                                title: str = None, log_namespace: str = "", arguments_for_log:  list[str] = None, throw_exception_if_exitcode_is_not_zero: bool = True) -> tuple[int, str, str, int]:

        mock_loader_result = self.__try_load_mock(program, ' '.join(arguments_as_array), working_directory)
        if mock_loader_result[0]:
            return mock_loader_result[1]

        start_datetime = datetime.utcnow()
        process = self.__run_program_argsasarray_async_helper(program, arguments_as_array, working_directory, verbosity, print_errors_as_information, log_file,
                                                              timeoutInSeconds, addLogOverhead, title, log_namespace, arguments_for_log)
        pid = process.pid
        stdout, stderr = process.communicate()
        stdout = GeneralUtilities.bytes_to_string(stdout).replace('\r', '')
        stderr = GeneralUtilities.bytes_to_string(stderr).replace('\r', '')
        exit_code = process.wait()
        end_datetime = datetime.utcnow()

        if arguments_for_log is None:
            arguments_for_log = ' '.join(arguments_as_array)
        else:
            arguments_for_log = ' '.join(arguments_for_log)

        duration: timedelta = end_datetime-start_datetime
        cmd = f'{working_directory}>{program} {arguments_for_log}'

        if GeneralUtilities.string_is_none_or_whitespace(title):
            info_for_log = cmd
        else:
            info_for_log = title

        if verbosity == 3:
            GeneralUtilities.write_message_to_stdout(f"Run '{info_for_log}'.")

        if isinstance(self.program_runner, ProgramRunnerEpew):
            pass
        else:
            if verbosity == 1 and exit_code != 0:
                self.__write_output(print_errors_as_information, stderr)
            if verbosity == 2:
                GeneralUtilities.write_message_to_stdout(stdout)
                self.__write_output(print_errors_as_information, stderr)
            if verbosity == 3:
                GeneralUtilities.write_message_to_stdout(stdout)
                self.__write_output(print_errors_as_information, stderr)
                formatted = self.__format_program_execution_information(title=info_for_log, program=program, argument=arguments_for_log, workingdirectory=working_directory)
                GeneralUtilities.write_message_to_stdout(f"Finished '{info_for_log}'. Details: '{formatted}")

        if throw_exception_if_exitcode_is_not_zero and exit_code != 0:
            formatted = self.__format_program_execution_information(exit_code, stdout, stderr, program, arguments_for_log, working_directory, info_for_log, pid, duration)
            raise ValueError(f"Finished '{info_for_log}'. Details: '{formatted}")

        result = (exit_code, stdout, stderr, pid)
        return result

    # Return-values program_runner: Exitcode, StdOut, StdErr, Pid
    @GeneralUtilities.check_arguments
    def run_program(self, program: str, arguments:  str = "", working_directory: str = None, verbosity: int = 1,
                    print_errors_as_information: bool = False, log_file: str = None, timeoutInSeconds: int = 600, addLogOverhead: bool = False,
                    title: str = None, log_namespace: str = "", arguments_for_log:  list[str] = None, throw_exception_if_exitcode_is_not_zero: bool = True) -> tuple[int, str, str, int]:
        return self.run_program_argsasarray(program, GeneralUtilities.arguments_to_array(arguments), working_directory, verbosity, print_errors_as_information,
                                            log_file, timeoutInSeconds, addLogOverhead, title, log_namespace, arguments_for_log, throw_exception_if_exitcode_is_not_zero)

    # Return-values program_runner: Pid
    @GeneralUtilities.check_arguments
    def run_program_argsasarray_async(self, program: str, arguments_as_array: list[str] = [], working_directory: str = None, verbosity: int = 1,
                                      print_errors_as_information: bool = False, log_file: str = None, timeoutInSeconds: int = 600, addLogOverhead: bool = False,
                                      title: str = None, log_namespace: str = "", arguments_for_log:  list[str] = None) -> int:

        mock_loader_result = self.__try_load_mock(program, ' '.join(arguments_as_array), working_directory)
        if mock_loader_result[0]:
            return mock_loader_result[1]

        process: Popen = self.__run_program_argsasarray_async_helper(program, arguments_as_array, working_directory, verbosity,
                                                                     print_errors_as_information, log_file, timeoutInSeconds, addLogOverhead, title, log_namespace, arguments_for_log)
        return process.pid

    # Return-values program_runner: Pid
    @GeneralUtilities.check_arguments
    def run_program_async(self, program: str, arguments: str = "",  working_directory: str = None, verbosity: int = 1,
                          print_errors_as_information: bool = False, log_file: str = None, timeoutInSeconds: int = 600, addLogOverhead: bool = False,
                          title: str = None, log_namespace: str = "", arguments_for_log:  list[str] = None) -> int:
        return self.run_program_argsasarray_async(program, GeneralUtilities.arguments_to_array(arguments), working_directory, verbosity,
                                                  print_errors_as_information, log_file, timeoutInSeconds, addLogOverhead, title, log_namespace, arguments_for_log)

    @GeneralUtilities.check_arguments
    def __try_load_mock(self, program: str, arguments: str, working_directory: str) -> tuple[bool, tuple[int, str, str, int]]:
        if self.mock_program_calls:
            try:
                return [True, self.__get_mock_program_call(program, arguments, working_directory)]
            except LookupError:
                if not self.execute_program_really_if_no_mock_call_is_defined:
                    raise
        return [False, None]

    @GeneralUtilities.check_arguments
    def __adapt_workingdirectory(self, workingdirectory: str) -> str:
        if workingdirectory is None:
            return os.getcwd()
        else:
            return GeneralUtilities.resolve_relative_path_from_current_working_directory(workingdirectory)

    @GeneralUtilities.check_arguments
    def __write_output(self, print_errors_as_information, stderr):
        if print_errors_as_information:
            GeneralUtilities.write_message_to_stdout(stderr)
        else:
            GeneralUtilities.write_message_to_stderr(stderr)

    @GeneralUtilities.check_arguments
    def __format_program_execution_information(self, exitcode: int = None,  stdout: str = None, stderr: str = None, program: str = None, argument: str = None,
                                               workingdirectory: str = None, title: str = None, pid: int = None, execution_duration: timedelta = None):
        result = ""
        if(exitcode is not None and stdout is not None and stderr is not None):
            result = f"{result} Exitcode: {exitcode}; StdOut: '{stdout}'; StdErr: '{stderr}'"
        if(pid is not None):
            result = f"Pid: '{pid}'; {result}"
        if(program is not None and argument is not None and workingdirectory is not None):
            result = f"Command: '{workingdirectory}> {program} {argument}'; {result}"
        if(execution_duration is not None):
            result = f"{result}; Duration: '{str(execution_duration)}'"
        if(title is not None):
            result = f"Title: '{title}'; {result}"
        return result.strip()

    @GeneralUtilities.check_arguments
    def verify_no_pending_mock_program_calls(self):
        if(len(self.__mocked_program_calls) > 0):
            raise AssertionError(
                "The following mock-calls were not called:\n"+",\n    ".join([self.__format_mock_program_call(r) for r in self.__mocked_program_calls]))

    @GeneralUtilities.check_arguments
    def __format_mock_program_call(self, r) -> str:
        r: ScriptCollectionCore.__MockProgramCall = r
        return f"'{r.workingdirectory}>{r.program} {r.argument}' (" \
            f"exitcode: {GeneralUtilities.str_none_safe(str(r.exit_code))}, " \
            f"pid: {GeneralUtilities.str_none_safe(str(r.pid))}, "\
            f"stdout: {GeneralUtilities.str_none_safe(str(r.stdout))}, " \
            f"stderr: {GeneralUtilities.str_none_safe(str(r.stderr))})"

    @GeneralUtilities.check_arguments
    def register_mock_program_call(self, program: str, argument: str, workingdirectory: str, result_exit_code: int, result_stdout: str, result_stderr: str,
                                   result_pid: int, amount_of_expected_calls=1):
        "This function is for test-purposes only"
        for _ in itertools.repeat(None, amount_of_expected_calls):
            mock_call = ScriptCollectionCore.__MockProgramCall()
            mock_call.program = program
            mock_call.argument = argument
            mock_call.workingdirectory = workingdirectory
            mock_call.exit_code = result_exit_code
            mock_call.stdout = result_stdout
            mock_call.stderr = result_stderr
            mock_call.pid = result_pid
            self.__mocked_program_calls.append(mock_call)

    @GeneralUtilities.check_arguments
    def __get_mock_program_call(self, program: str, argument: str, workingdirectory: str):
        result: ScriptCollectionCore.__MockProgramCall = None
        for mock_call in self.__mocked_program_calls:
            if((re.match(mock_call.program, program) is not None)
               and (re.match(mock_call.argument, argument) is not None)
               and (re.match(mock_call.workingdirectory, workingdirectory) is not None)):
                result = mock_call
                break
        if result is None:
            raise LookupError(f"Tried to execute mock-call '{workingdirectory}>{program} {argument}' but no mock-call was defined for that execution")
        else:
            self.__mocked_program_calls.remove(result)
            return (result.exit_code, result.stdout, result.stderr, result.pid)

    @GeneralUtilities.check_arguments
    class __MockProgramCall:
        program: str
        argument: str
        workingdirectory: str
        exit_code: int
        stdout: str
        stderr: str
        pid: int

    # </run programs>

    @GeneralUtilities.check_arguments
    def extract_archive_with_7z(self, unzip_program_file: str, zipfile: str, password: str, output_directory: str) -> None:
        password_set = not password is None
        file_name = Path(zipfile).name
        file_folder = os.path.dirname(zipfile)
        argument = "x"
        if password_set:
            argument = f"{argument} -p\"{password}\""
        argument = f"{argument} -o {output_directory}"
        argument = f"{argument} {file_name}"
        return self.run_program(unzip_program_file, argument, file_folder)

    @GeneralUtilities.check_arguments
    def get_internet_time(self) -> datetime:
        response = ntplib.NTPClient().request('pool.ntp.org')
        return datetime.fromtimestamp(response.tx_time)

    @GeneralUtilities.check_arguments
    def system_time_equals_internet_time(self, maximal_tolerance_difference: timedelta) -> bool:
        return abs(datetime.now() - self.get_internet_time()) < maximal_tolerance_difference

    @GeneralUtilities.check_arguments
    def system_time_equals_internet_time_with_default_tolerance(self) -> bool:
        return self.system_time_equals_internet_time(self.__get_default_tolerance_for_system_time_equals_internet_time())

    @GeneralUtilities.check_arguments
    def check_system_time(self, maximal_tolerance_difference: timedelta):
        if not self.system_time_equals_internet_time(maximal_tolerance_difference):
            raise ValueError("System time may be wrong")

    @GeneralUtilities.check_arguments
    def check_system_time_with_default_tolerance(self) -> None:
        self.check_system_time(self.__get_default_tolerance_for_system_time_equals_internet_time())

    @GeneralUtilities.check_arguments
    def __get_default_tolerance_for_system_time_equals_internet_time(self) -> timedelta:
        return timedelta(hours=0, minutes=0, seconds=3)

    @GeneralUtilities.check_arguments
    def get_semver_version_from_gitversion(self, folder: str) -> str:
        return self.get_version_from_gitversion(folder, "MajorMinorPatch")

    @GeneralUtilities.check_arguments
    def get_version_from_gitversion(self, folder: str, variable: str) -> str:
        # called twice as workaround for issue 1877 in gitversion ( https://github.com/GitTools/GitVersion/issues/1877 )
        result = self.run_program_argsasarray("gitversion", ["/showVariable", variable], folder)
        result = self.run_program_argsasarray("gitversion", ["/showVariable", variable], folder)
        return GeneralUtilities.strip_new_line_character(result[1])

    def push_nuget_build_artifact_for_project_in_standardized_project_structure(self, push_script_file: str, codeunitname: str,
                                                                                registry_address: str = "nuget.org", api_key: str = None):
        build_artifact_folder = GeneralUtilities.resolve_relative_path(
            f"../../Submodules/{codeunitname}/{codeunitname}/Other/Build/BuildArtifact", os.path.dirname(push_script_file))
        self.push_nuget_build_artifact_of_repository_in_common_file_structure(self.find_file_by_extension(build_artifact_folder, "nupkg"),
                                                                              registry_address, api_key)

    @GeneralUtilities.check_arguments
    def create_release_for_project_in_standardized_release_repository_format(self, projectname: str, create_release_file: str,
                                                                             project_has_source_code: bool, remotename: str, build_artifacts_target_folder: str, push_to_registry_scripts:
                                                                             dict[str, str], verbosity: int = 1, reference_repository_remote_name: str = None,
                                                                             reference_repository_branch_name: str = "main", build_repository_branch="main",
                                                                             public_repository_url: str = None, build_py_arguments: str = ""):

        folder_of_create_release_file_file = os.path.abspath(os.path.dirname(create_release_file))

        build_repository_folder = GeneralUtilities.resolve_relative_path(f"..{os.path.sep}..", folder_of_create_release_file_file)
        if self.git_repository_has_uncommitted_changes(build_repository_folder):
            raise ValueError(f"Repository '{build_repository_folder}' has uncommitted changes.")

        self.git_checkout(build_repository_folder, build_repository_branch)

        repository_folder = GeneralUtilities.resolve_relative_path(f"Submodules{os.path.sep}{projectname}", build_repository_folder)
        mergeToStableBranchInformation = ScriptCollectionCore.MergeToStableBranchInformationForProjectInCommonProjectFormat(repository_folder)
        mergeToStableBranchInformation.verbosity = verbosity
        mergeToStableBranchInformation.project_has_source_code = project_has_source_code
        mergeToStableBranchInformation.push_source_branch = True
        mergeToStableBranchInformation.push_source_branch_remote_name = remotename
        mergeToStableBranchInformation.push_target_branch = True
        mergeToStableBranchInformation.push_target_branch_remote_name = remotename
        mergeToStableBranchInformation.merge_target_as_fast_forward_into_source_after_merge = True
        mergeToStableBranchInformation.build_py_arguments = build_py_arguments
        new_project_version = self.standardized_tasks_merge_to_stable_branch_for_project_in_common_project_format(mergeToStableBranchInformation)

        createReleaseInformation = ScriptCollectionCore.CreateReleaseInformationForProjectInCommonProjectFormat(repository_folder, build_artifacts_target_folder,
                                                                                                                projectname, public_repository_url,
                                                                                                                mergeToStableBranchInformation.targetbranch)
        createReleaseInformation.verbosity = verbosity
        createReleaseInformation.build_py_arguments = build_py_arguments
        if project_has_source_code:
            createReleaseInformation.push_artifact_to_registry_scripts = push_to_registry_scripts
            self.standardized_tasks_release_buildartifact_for_project_in_common_project_format(createReleaseInformation)

            self.git_commit(createReleaseInformation.reference_repository, f"Added reference of {projectname} v{new_project_version}")
            if reference_repository_remote_name is not None:
                self.git_push(createReleaseInformation.reference_repository, reference_repository_remote_name, reference_repository_branch_name,
                              reference_repository_branch_name,  verbosity=verbosity)
        self.git_commit(build_repository_folder, f"Added {projectname} release v{new_project_version}")
        return new_project_version
