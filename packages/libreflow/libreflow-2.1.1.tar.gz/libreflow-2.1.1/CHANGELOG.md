# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)[^1].

<!---
Types of changes

- Added for new features.
- Changed for changes in existing functionality.
- Deprecated for soon-to-be removed features.
- Removed for now removed features.
- Fixed for any bug fixes.
- Security in case of vulnerabilities.

-->

## [Unreleased]

## [2.1.1] - 2022-06-01

### Added

* A new type of task (`libreflow.baseflow.task.ManagedTask`), providing features (e.g., the creation of a list of default files) which use the task manager.
* A new type of task collection (`libreflow.baseflow.task.ManagedTaskCollection`). This collection uses, for each of its task, the icon and color defined by its associated default task in the task manager. It also provides an action to create a default task among those defined in the task manager.
* Actions to add and edit a default file of a task.

### Fixed

* Make the terminal automatically close when RV is closed.

## [2.1.0] - 2022-05-17

### Added

* An `EntityManager` object which manages the collections of common entities (films, sequences, shots, departments, files, revisions, synchronisation statutes).
* Revision maps provide the `file_base_name` and `file_mapped_name` entries in their contextual dictionary, which are respectively the real name of the parent file on the file system without its extension, and its mapped name in the flow.
* As for other entities, the `Task` and `TaskCollection` classes have been defined to allow to manage tasks, in a single Mongo collection for the entire project.
* A `task_manager` module to manage the creation of tasks based on default tasks.

### Changed

* Redefine films, sequences and shots as Mongo entities.
* Films, sequences, shots, files, revisions and synchronisation statutes are retrieved by default from the global entity collections provided by the project's entity manager, assuming the project provides the latter in the `get_entity_manager()` method.
* If no default path format is provided to the `FileSystemMap` `add_file()` and `add_folder()` methods, the file/folder is created with the path format in the contextual dictionary by default, if defined.

### Removed

* Unused `kitsu_name()` and `kitsu_id()` method of the project class.

## [2.0.13] - 2022-05-13

### Added

* Use Sentry to monitor jobs flow worker events. The Sentry SDK is initialised before starting a `JobsWorkerSession`, assuming the project Data Source Name (DSN) is provided in the `SENTRY_DSN` environment variable. When the job executed by the worker encounters an error, an exception is raised after the status of the job is updated, ensuring that the error is reported to Sentry.

### Fixed

* Make the `Reveal In Explorer` option reveal the latest available revision.
* Gazu wrapper's `get_shots()` method: tasks undefined in Kitsu are skipped in the filtering.
* An exception is raised whenever the `get_path()` method of a revision is called while its relative path is undefined (i.e., the value of its `path` property is an empty string or `None`).

## [2.0.12] - 2022-04-26

### Fixed

* Get around the error raised by Gazu upon the upload of some video files.

### Added

* Mark Sequence:
  - mark current and total time codes if provided in the marking template, as `tc` and `total_tc` respectively
  - update the text font
  - remove gray bands

### Changed

* Gazu wrapper: allow to specify multiple statutes for a given task in the `get_shot()` method filter.

## [2.0.11] - 2022-04-21

### Added

* One can specify the `--force-delete` argument to the jobs cleanup session to force job deletion.
* Gazu wrapper: add a method to upload a preview on a shot task, given the names of the shot and the sequence it belongs to.

### Changed

* Gazu wrapper: allow to get a list of shots filtered by their current statutes on given tasks

## [2.0.10] - 2022-03-30

### Added

* Render AfterEffects playblast/Publish and Render Playblast: allow to choose the render resolution.
  - Whenever the option dialog opens, the parameter value is reset to the value stored in the project's **action value store**.
* A module `action_values` which defines classes to be used by actions to manage a set of default values (typically that of their parameters), which can be overriden at the project and site scopes.

### Changed

* Utility functions related to context values are located in the `libreflow.utils.flow.context_values` module.

### Fixed

* Make sure that the last revision oid of each file created during playblast rendering is updated, so that it can show up in the file map.

## [2.0.9] - 2022-03-21

### Added

* A WAV file template
* Operators in Kitsu API wrapper to update the status of a shot's task

## [2.0.8] - 2022-03-15

### Added

* A new module allowing to browse through project entries. It provides for that purpose:
1. an `Actor` and commands to index and search through projects on the current cluster
2. `SearchFlowView`s (inherited from Kabaret's base flow views) which embed a search bar at their top.  
In order make this type of view available in the GUI, one must register the `SearchFlowViewPlugin` plugin type in the session plugins.

## [2.0.7] - 2022-03-13

### Added

* AfterEffects templates used for rendering (render settings, movie and audio output modules) can be configured in the settings of the current site.
* An option to export a temporary audio track of an AfterEffects scene, which may be used by image sequence marking option to generate a playblast. This option assumes a template named `audio_only` is available in the output module templates of the AfterEffects session used for rendering.

### Fixed

* File maps appearing empty when touched from other sessions, because properties of some entities are not yet set: these maps now update their cache whenever an accessed file property is not found in it.
* Render AfterEffects playblasts:
  - Ensure that paths to the revisions created during rendering and marking are generated using the path formats of the files they belong to.
  - Generate the playblast with the scene audio track, if it exists.

## [2.0.6] - 2022-03-13

### Added

* Tracked file class provides the `add_revision` method to add a revision a generic way.
* Working site type is now injectable
* WAV file format

## [2.0.5] - 2022-02-22

### Added

* File lock can be enabled/disabled in the project settings (with option `Enable File Lock`).
* Indicate the sync status of the last revision displayed in the file list with colors.

## [2.0.4] - 2022-02-16

### Fixed

* The matching between the selected and the displayed values of a param with a preset, which could differ if the preset couldn't be applied: in this case, the param is reverted to its default value.
* Playblast rendering at sequence level

## [2.0.3] - 2022-02-09

### Added

* An option in playblast rendering actions to scale the render resolution given a percentage.

## [2.0.2] - 2022-02-03

### Changed

* Hide dependency request option on working copies.
* A warning dialog shows up when one is about to download a revision already available locally.

### Added

* Icons for revision options

### Fixed

* File upload to Kitsu
* Force stored revision paths to contain slashes (`/`) only to ensure they are correctly interpreted by Unix systems when revisions are synced.
* Waiting download jobs which reference revisions unavailable on the exchange server are not processed.
* When submitted, a synchronisation job stored the local path of the referenced revision, rooted at the current site's root directory. This ineluctably raised a conflict when the job was processed from another site with a different root path.  
  Instead, only the revision relative path is stored, and its local path is computed on the fly, when the job is processed.

## [2.0.1] - 2022-02-02

### Added

* Added a path format property to file objects, used by default to generate revision paths.
* A system allowing to configure and create default files.

### Fixed

* Ensure local paths are valid on Windows, Linux and MacOS systems.
* Fix tracked file `is_empty` method when used to check if the file is empty on the current site.

## [2.0.0] - 2022-01-28

### IMPORTANT NOTE

This 2.x version of Libreflow embed many changes, including way more speed for map components, using a MongoDB service. Thus, it requires the setup of a MongoDB for Libreflow to work.

### Changed

* Use `kabaret.flow_entities` extension to manage file system objects (files, revisions, synchronisation statutes) and site synchronisation queues in a Mongo database.
* Encapsulate file transfert operations in a single object hold by the exchange site.
* Revision paths are stored in the database.
* Revision paths can be generated and updated based on the content of the revision's contextual settings.
* Hide file publish option on locked files and when the current user has no working copy on them.

### Added

* Add an action to test the connection to the file exchange server.

### Fixed

* Warn the user when an unavailable revision is double-clicked.
* Hide revision request option if the revision is already available on the exchange server.
* Hide revision upload option if the revision isn't available.
* Hide user's bookmarks if not registered in the project's users.
* Hide Kitsu options if the project's Kitsu settings aren't configured.

## [1.6.30] - 2021-12-16

### Added

* A preset system for each user which pre-fills option parameters (available for *Upload to Kitsu*, publication and playblast rendering options)

## [1.6.29] - 2021-12-03

### Fixed

* Temporary forced gazu dependency version, as latest version is making trouble to connect

## [1.6.28] - 2021-11-30

### Fixed

* Publish from history: fix window display error
* Publish from history: ensure that the revision is uploaded (when *Upload After Publish* enabled) and Blender dependencies are saved.

## [1.6.27] - 2021-11-25

### Changed

* Add -autoRetime 0 option to RV launcher, so that sequences with different frame rates are kept in sync.

### Added

* Playblast: add options to reduce texture sizes and set target texture size
* Publish: hide *Upload After Publish* option for files matching one of the patterns provided in the project settings

## [1.6.26] - 2021-11-15

### Changed

* Improve synchronization job management: show requested revisions in the history, reset erroneous jobs

### Added

* A site option to automatically upload playblasts to the exchange server while they are being uploaded to Kitsu.

### Fixed

* Don't store parameters of user environment variable creation dialog in the DB, to avoid access conflicts between sessions.

## [1.6.25] - 2021-11-08

### Fixed

* Add a missed synchronization icon, preventing the project root page to display entirely.

## [1.6.24] - 2021-11-08

### Changed

* Do not copy in current folder anymore when publishing.

### Fixed

* Correct the warning message that appears when opening a file edited by other users.
* So far, site environment variables could only be redefined for a single OS. These variables have now one value for each OS (Linux, Darwin or Windows), active depending on the OS being used.
* Fix crash when trying to create a tracked folder's empty working copy folder while it already exists.
* Create a user's profile upon the first login
* Users can log in using their Kitsu desktop login or email

## [1.6.23] - 2021-10-14

### Added

* The possibility to select the columns to display in the job list, by right-clicking on the list header.
* Application versions can be overriden in a department's contextual environment. This can be achieved creating a variable that follows the naming convention `<RUNNER_NAME>_VERSION` in the environment map of a department (option `Show Environment`).  
  **NB:** In order for overrides to be effective, one must have defined the executable paths corresponding to the runner overriden versions, either in the system, site or user environment. For instance, setting Blender version used in a given department to `2.93` requires the `BLENDER_2_93_EXEC_PATH` variable to be set up. Otherwise, the application will launch in its default version.

## [1.6.22] - 2021-09-30

### Added

* A launchable session which deletes jobs emitted before a given date, daily at a given time. Additionally, the cleaning process can stop on some days of the week specified by the user.
* Allow users to add sequences to their bookmarks.

### Fixed

* The job view now reacts to job creation and deletion events. This allows two optimisations:
  - Items are added/removed as jobs are created/deleted, without a complete refresh of the list
  - The job list is built once, the first time the view is shown
* First step toward chaining jobs: When generating the playblast of an AfterEffects scene, ensure the generated image sequence is marked only when the job in charge of the rendering has terminated.

## [1.6.21] - 2021-09-20

### Fixed

* Speed up the display time of the waiting job count on the synchronization section, updating a counter at site level as files are requested and synchronized.
* Allow to upload playblasts to Kitsu in tasks of different types.

## [1.6.20] - 2021-09-13

### Added

* A parameter to set the MinIO server bucket name, which can be set in the current exchange site.
* `Upload after publish` option is now enabled by default for all files matching one of the patterns provided in the projet settings.

### Fixed

* Site names are cached in the order defined in the current site, improving the time for histories to display.
* Prevent users from synchronizing files if the exchange server is not configured.

## [1.6.19] - 2021-09-09

### Fixed

* Download MinIO's intermediate files in a folder at the project's root path, named `.tmp`, to ensure that the drive of intermediate files is the same as that of the final downloaded files.
  - Fixes 1.6.18 synchronisation error occuring at download when the project root drive and the OS temporary folder drive differ.

## [1.6.18] - 2021-09-07

### Fixed

* Minimise the risk of exceeding the maximum path length on Windows when using MinIO API to download a file from the exchange server, using a custom intermediate temporary file.

## [1.6.17] - 2021-09-01

### Added

* A new session to periodically clear synchronisation jobs.
* An option to compare the playblasts of two tasks of a shot in Shotgun RV. Available tasks: layout, blocking, animation, compositing

### Changed

* Remove unused options (locking, open with...) on files.
* Rework the _Publish and playblast_ option for Blender files, and define it for AfterEffects files. Make this option accessible right under the _Publish_ option.

### Fixed

* Ensure that image sequence rendering and playblast generation for AfterEffects scenes are **processed the same way: locally or on a jobs node session**. In the latter case, ensure that both steps are **handled in the same pool**.
* Add `fileseq` to the project's dependencies, needed to render AfterEffects playblasts.
* Prevent the user from publishing in a non-editable file, and from creating a working copy when the file is double-clicked.

## [1.6.16] - 2021-08-24

### Added

* An option to upload all playblasts of a sequence to the right tasks in Kitsu.
  - If a task type is provided in the Kitsu data of a task (in the dependency template), it is used in priority for all files belonging to this task.
* An option to request revisions towards multiple sites, with an automatic source site selection option.

### Changed

* Do not pack AfterEffects playblast images after they have been rendered (cf. 1.6.12 folder packing update).
* Mark playblast images with the name of the original AfterEffects scene (or the containing folder's, if it doesn't exist) instead of the resulting playblast name.

### Fixed

* One can validate credentials pressing the Enter key.

## [1.6.15] - 2021-08-17

### Fixed

* Handle synchronization errors, now reported in the log of jobs.

## [1.6.14] - 2021-08-11

### Fixed

* Options to request a single revision and its dependencies.

## [1.6.13] - 2021-08-03

### Added

* Each site can define a custom list of site names to change their display order in file histories and request option windows (these now include `Request` and `Request as` options available on a single revision).
* OBJ file format
* The possibility to define shot elements that are not requestable, which can be achieved adding a `requestable` entry in the data of the element in the shot dependency template.

### Changed

* Request actions have been revised.

## [1.6.12] - 2021-07-20

### Changed

* The content of a tracked folder revision is packed/unpacked only when it needs to be uploaded to/downloaded from the exchange server.

## [1.6.11] - 2021-07-19

### Added

* A set of job and action classes to render playblasts of After Effects scenes. The procedure is made in two steps:
  - The image sequence rendering. This step can be achieved in a subprocess or using a job.
  - The marking of images to generate the playblast. When using the `Render Image Sequence`, this step is handled in a job by default. This step is also available as a standalone option on any tracked folder which contains at least one image; in this case, the generate of the playblast can be achieved in a subprocess or using a job.

### Changed

* By default, a file's history displays only the synchronisation statutes of sites considered as active on the project.
* Display synchronisation statutes and site short names by default in a file's history.

* Sequence playblast rendering action has been update in order to render playblasts of After Effects scenes existing (depending on the defined shot dependencies).

### Fixed

* Ensure that the source site and creator of sequence marking jobs are the same as those of the image rendering jobs.

## [1.6.10] - 2021-07-07

### Fixed

* Sequence playblast rendering action dialog:
  - Make the first available head revision be the default selected revision
  - Make unavailable revisions unselectable
* Ensure runner types are registered when the project root is touched. This fixes the case where a runner is not found when launching an application, because the project root has not been accessed at least once.
* Systematically remove the content of the `current` revision folder when a revision is made current. This prevents the packaging of files already present in the `current` folder, making the archive grow each time a revision is made current.

## [1.6.9] - 2021-07-01

### Fixed

* Make runner id accessible to the submitted job when rendering a playblast.

## [1.6.8] - 2021-07-01

### Fixed

* The setting of the environment variable holding a runner executable path has been moved, so that every RunAction which aims at opening a file properly updates the current environment before launching its corresponding runner.

## [1.6.7] - 2021-06-28

### Added

* An action to render playblasts of Blender scenes of a whole sequence.  
**Note:** This early version needs the different tasks of a shot (e.g., layout, animation, etc.) to be explicitly defined in a dependency template named `shot`.

### Changed

* An application executable path is searched in the different environments just before launching the application, in the following order of priority: System environment > user environment > site environment.

### Fixed

* Added status icons with lowercase names to prevent resource lookup error on Linux.

## [1.6.6] - 2021-06-23

### Fixed

* When a user logs in, the Libreflow ID (computed from the Kitsu ID) is changed to lowercase before the map of users is looked up. This prevents multiple users from having the same IDs with different character cases, and thus ensures the same behaviour in Windows and Linux when the user creates and access working copies.

## [1.6.5] - 2021-06-09

### Fixed

* All files in a tracked folder working copy are properly zipped when a publication is made.
* Make the revision upload after publication work again.
* Make *Keep editing* option work again when publishing a working copy from a file history.

### Added

* Brute-force integration of the `kabaret.jobs` module implementation (with subtle corrections) to manage jobs.
* Based on `kabaret.jobs`, the possibility for studios to handle playblast renderings as jobs.
  - Jobs can be submitted in one of the pools of the current site.
  - The feature can be used choosing the `Submit job` option when rendering a playblast.
* Adaptations of `kabaret.jobs`:
  - Make view's job filter case-sensitive, and include pool name in filtering attributes
  - Provide a job with a label and definable owner and creator
  - Define a JOBS_DEFAULT_FILTER environment variable, usable by the JobsView as a default filter. If not explicitly provided at session startup, the variable defaults to the current site name.

## [1.6.4] - 2021-05-27

### Added

* Allow Kitsu admin sites to upload playblasts toward any Kitsu task type available for the project.

### Changed

* Users are warned whenever one or more users have a working copy on a file, but are not prevented anymore from publishing in that case.
* Reference revision name in the dialog to create a working copy is set to the file's last publication name by default (if it exists).

## [1.6.3] - 2021-05-21

### Fixed

* Copy of runner command to clipboard is handled by native Qt application clipboard object, instead of TKinter features (not integrated to Python main package on all LInux distributions).
* A new action to request elements related to a shot (assets, scenes, misc), including their dependencies.

## [1.6.2] - 2021-05-20

### Added

* Runner implementation provides additional information, such as the command used, the time of the last run, etc.
* A panel in the `SubprocessView` displays information about the currently selected runner.
* A new option in the `SubprocessView` menu allows to hide completed runner instances.

### Fixed

* A runner instance is now identified by a Universal Unique Identifier, which eases its deletion in the subprocess manager.

## [1.6.1] - 2021-05-11

### Added

* A new flow utility function `get_context_value` can be used to recursively find and concatenate the values of all flow params of a given name declared in the parents of an object, including itself. To improve the flexibility of the context value parameterisation, the function makes use of the contextual dict when param values are specified between braces.

## [1.6.0] - 2021-05-11

### Added

* A new `kabaret.subprocess_manager` utility module has been created to redefine and extend the core classes of the original Kabaret extension.
  - Core classes have been extended to keep track of runner instances.
  - A bunch of commands has been added to manage the underlying processes of these instances (launch, terminate, kill).
  - A new view, which inherits from the original `SubprocessView`, lists all the runners instanciated from the current session, and allow to display the output of the subprocess launched by the selected runner in the list. For now, the list has to be manually refreshed.
* A shortcut to the current site's job queue is available in the *Synchronization* section of the project's root page.

### Changed

* The base runner class has been adapted as required by the first version of the `SubprocessView`. Notable changes are:
  - The redirection of both *stdout* and *stderr* of the subprocess to the same file.
  - Additional data and operators to manage the subprocess, usable by the actor commands.

### Fixed

* The SubprocessManager does not add a runner's data in the list of runner infos if it has not run at least once. This is a temporary check which prevents from accessing unavailable data about a subprocess, because currently not provided by some runner types (e.g. `DefaultEditor`).

## [1.5.12] - 2021-05-07

### Fixed

* Exchange sites have been removed from the `RequestAs` action's lists of requesting and requested sites.
* The revision published in a target file is automatically made current. Consequently, the last comment in the file list updates to the published revision's comment.
* Revision upload after publishing into another file has been fixed.

### Added

* A new action allows to upload a published revision on the exchange server.

## [1.5.11] - 2021-05-04

### Changed

* Playblast upload dialog messages have been reworked.

### Fixed

* An additional test checks if the current's user data retrieved with Kitsu API provides the user's role. If not, the user is considered as not having the required rights to upload the target playblast while not assigned to the corresponding task.

## [1.5.10] - 2021-04-30

### Fixed

* The revision drop-down menu display isn't raising an error anymore when the file reference is not set.

### Added

* The option to use simplified rigs has been made available on the action dialog to publish and render a playblast.
* JSX file format is available.

## [1.5.9] - 2021-04-22

### Fixed

* Kitsu entity data is retrieved only when the preview uploading action shows up or run (not in the constructor). This fixes an issue occuring whenever the action object was instantiated, since it tried to get data from flow object not yet instantiated.

## [1.5.8] - 2021-04-22

### Fixed

* Checking if a user is assigned to a Kitsu task is done exclusively by the preview uploading action. This means the internal function used to upload a preview assumes the user has sufficient rights.

## [1.5.7] - 2021-04-22

### Changed

* Kitsu supervisors and studio managers can upload previews regardless of their task assignment.

## [1.5.6] - 2021-04-22

### Changed

* Two choice values have been redefined to select a file's revision:
  - One list all available revisions of the file
  - The other list all available published revisions
* Revision type (working copy or publication) is no longer checked from the revision creator's name but a name pattern (currently, `v\d\d\d`).

## [1.5.5] - 2021-04-21

### Added

* A new action allows to upload files with eligible names as Kitsu previews. For now, uploadable files are defined in the project's Kitsu configuration.

### Changed

* Change time format in log files, to make it human readable

## [1.5.4] - 2021-04-20

### Fixed

* Single files are checked to see if they match a folder in the flow, before checking if they match a file. It prevents folders containing a single file from being considered files.

## [1.5.3] - 2021-04-20

### Added

* Two new features of the Blender playblast are used by the playblast action:
  - to enable the use of low-definition rigs in the Blender scene, available as a checkbox
  - to print on the sequence the name of the selected revision
* A new action `GetDependencies` allows to summarise dependency information of a given object and request all those which can be requested.
  - As of now, real dependencies are collected from the Blender Asset Tracer tracing result. The feature is thus truly practical for Blender files, and dependencies related to files of any other format remain theoretical.

### Changed

* Open file action displays by default last revision, or user's working copy if it does not exist.
* A revision is systematically made current when published.

### Fixed

* Project root path is added to the environment when opening a revision from a file history.
* File relation to department has been temporarily removed, allowing to define files elsewhere than in a department.
* Users can publish in files which are not related to a department in the flow.

## [1.5.2] - 2021-04-16

### Added

* Login page shows up when accessing bookmarks if user is not connected to Kitsu.

## [1.5.1] - 2021-04-02

### Fixed

* Publishing into another file creates the necessary intermediate directories when the target file has not been created on the current site.

## [1.5.0] - 2021-04-01

### Added

* JSON file format has been made available.
* libreflow.utils.b3d has been created with a wrapper for python-expressions to handle specific launch cases on windows.

### Fixed

* The python expression wrapper is applied to playblasts so they work when Blender is called through a .bat file.

## [1.4.3] - 2021-03-30

* Force Kabaret version to 2.2.0rc2

## [1.4.2] - 2021-03-26

### Changed

* Allow the creation of working copies only on authorised files.

### Fixed

* A workaround has been added to make GUI display on latest MacOS version ([Kabaret issue #96](https://gitlab.com/kabaretstudio/kabaret/-/issues/96)).
* Requested and requesting sites are properly taken into account when requesting revisions.

### Added

* An additional parameter on revisions indicates if they are ready for synchronisation. A typical use case motivating this change is to prevent files not entirely created and initialised to be synchronised.
* An action now allows to request (for both source and target sites) elements of a given sequence.
  - Requestable elements: sets, characters, props, sound files, storyboards and layout scenes
* An action allows to resize all PNG images in a tracked folder revision into another tracked folder. Resulting tracked folder has the same name of source folder suffixed with *_half*.
* Revision oid pattern has been updated:
  - to include multiple subpatterns separated by `;`
  - so that each subpattern can include multiple substrings in the form `{substring0, substring1, ...}`
* A new action now allows to remove jobs emitted for a site before a given date, and of given type and status.

## [1.4.1] - 2021-03-22

### Fixed

* Redefinition of TrackedFolder `open` and `history` related types have been removed, as it mistakenly redefined the same relations in the TrackedFile class.
* Force the indices of `open` and `history` in TrackedFolder relation list to be the same as for TrackedFile in order to bypass submenu display issue.

## [1.4.0] - 2021-03-22

### Changed

* The way the names of new users are computed has been updated to take into account mail IDs.
* User class is now injectable

### Added

* A warning message appears in home page when the computed name of a new user is already registered in the project's user list.
* Revisions now hold a dict of dependencies stored at publication. This feature applies exclusively for Blender files using pil library `blender-asset-tracer` (aka BAT) which is now mandatory.


### Fixed

* Submenus show up again when right clicking on tracked folders.

## [1.3.4] - 2021-03-18

### Changed

* Publish action has been made injectable.
* Some improvements on advanced action dialogs have been made (message content, reset of file reference).

## [1.3.3] - 2021-03-16

### Added

* Action for requesting file revisions now displays a list of found oids given a wildcard-based oid pattern (** not supported).
* Using *[last]* keyword in the pattern allows to get the latest published revision of a file. For instance, according to how the base flow is currently designed, `/project/sequences/*/shots/*/departments/*/files/*/history/revisions/[last]` allows to retrieve the latest publications of all files of the project named `project`.

## [1.3.2] - 2021-03-15

### Fixed

* Action for requesting file revisions does not stop anymore when it falls onto a revision already available on requesting site, or not available on requested site.
* Current user is stored when profile has not already been registered.

### Changed

* Actions on tracked files have been refined and reorganised.

## Added

* Two new actions on tracked files allow respectively:
  - to publish changes made in a file into another file
  - to create a working copy on a file from a selected revision of another file
* Users can now publish their changes made to a file from their working copy in the revision history.

## [1.3.1] - 2021-03-10

### Changed

* project settings are now injectable

## [1.3.0] - 2021-03-10

### Added

* File maps now display tracked element latest revisions and their availability. These can be requested directly from the file map.

### Changed

* Site definitions have been updated to distinguish working and exchange sites. 
* Exchange server configuration is held by the project's exchange site.
* A working site's job queue can be accessed by right-clicking on its entry in the site map.
* Default exchange site has been renamed as *default_site*, to be distinguished from default working site.

### Fixed

* Job emission date is stored as a floating point timestamp (not a formatted date string anymore) to be easily processed.
* Corrections on file list UI for untracked items.
* Publication option is not available anymore when rendering a playblast on a Blender file if the user hasn't a working copy on this file. This fixes an error which causes the resulting publication to be empty.

## [1.2.8] - 2021-03-10

### Fixed

* Logout from project has been fixed.

## [1.2.7] - 2021-03-09

### Fixed

* Subprocess environments are updated with the current site's root path. In particular, this makes root path, required in scene builder, accessible in Blender environment whenever a Blender scene is opened from Libreflow.

### Added

* Subprocess extra environments also include the current user name and contextual settings.

## [1.2.6] - 2021-03-05

### Fixed

* Added FBX file format in PyPI package data to make FBX template available.

## [1.2.5] - 2021-03-01

* Omitted in 1.2.4: *script* folder made as a valid Python package.

## [1.2.4] - 2021-03-01

### Added

* An action to batch revisions request as another site (currently not publicly available).

### Changed

* A new Blender template file.

### Fixed

* *script* folder made as a valid Python package.
* Project object is systematically touched when accessed from a home page widget to ensure user environment update.

## [1.2.3] - 2021-02-15

### Added

MP4, Illustrator and FBX file formats support

### Changed

* Actions to render a Blender file playblast is available in the base flow. Moreover, rendering a revision playblast generate a revision of the same index in a .mov tracked file.  
* Map clearing action relations have been removed to prevent unfortunate deletions.  
* Folder hierarchy in which user settings are stored has been changed to *<user_folder>/.libreflow/<project_name>/<user_name>/<user_settings>.*. This allows:  
  - a single user to be part of multiple projects
  - multiple users to authenticate on a project on the same workstation.
* Revisions display the time elapsed since their publication

## [1.2.2] - 2021-02-09

### Fixed

- Change *Request* action allowing context condition

## [1.2.1] - 2021-02-09

### Changed

- User name is now computed from Kitsu ID at first connection
- Files and folders of any type can be revealed in file explorer

## [1.2.0] - 2021-02-08

### Changed

- Bookmarks have been changed from a local json file to a dedicated map on the project's flow. #12
- File extensions and icons are now constants
- Revisions and TrackedFiles are now injectable
- A site can now request file revisions for other sites, if authorized (*request_files_from_anywhere* BoolParam).

### Added

- The project thumbnail flow can now be saved within the project admin/project settings area. So the thumbnail is available from anywhere no matter the site or OS. The old system is still present. #13

### Deprecated
- The old system for the thumbnail will soon be removed.

### Fixed
- At publish of a trackedFolder on python 3.7 an error appears because of a 3.8 update of stdlib shutil. Made a dirty fix for that.

## [1.1.7] - 2021-02-04

### Added

Users can log out from the project, sending them back to the login page.

### Fixed

User Kitsu id and the one used in the flow are distinguished, in order to ensure users are identified with a unique flow id which matches the pattern of a valid Python attribute, as required by Kabaret features. This currently implies users working on the project to be registered in this map.

## [1.1.6] - 2021-02-01

### Fixed

File data formats have been added in *setup.py* to make template files available within PyPI package.
Unforgivable hard-coded paths of several scripts have been changed for relative ones.

## [1.1.5] - 2021-01-29

### Fixed

Fix revision playblast rendering: Get playblast folder path from *Computed* department path.

## [1.1.4] - 2021-01-29

### Fixed

Fix revision upload: *Revision.get_relative_path()* gets parent file Computed path, instead of wrongly accessing *get_contextual_dict*.

## [1.1.3] - 2021-01-29

### Fixed

Until now, the computation of *File* and *Revision* paths implied implying a costly non-linear look-up of contextual edits, and long wait for maps to display. There is now only one contextual settings look-up to compute a *Department* path, from which department's file paths are computed and cached.

## [1.1.2] - 2021-01-21

### Fixed

User environment map items are now *SessionValue*s to make environment variable values stored at session's scope.

## [1.1.1] - 2021-01-20

### Fixed

MinIO and timeago added in setuptools requirements.

## [1.1.0] - 2021-01-20

*Multisite v1 release*

### Added 

- A ComputedParam named `root_dir` is now available in admin and it's cached as requiered by issue #4. A function `get_root()` at the Project level use it and is able to provide the root folder of the project according to the operative system. Call it from anywhere in the flow with `self.root().project().get_root()`.
- `CHANGELOG.md`, `LICENCE` and `AUTORS` files have been added to the repo
- **Multi-site** file synchronization features (related to issue #5):
  - Add and configure project's sites (type - studio, user or exchange -, per-OS root directories, exchange server properties)
  - Request tracked file's revisions unavailable on current site for download, based on a job submission feature
  - A `SynchronizeFile` action allow users to process files they requested, and files other sites requested from theirs. This currently uses a MinIO client.
  - Retrieve the current site and exchange site in the flow with `self.root().project().[get_current_site()|get_exchange_site()]`
  - UI improvement: revision history maps can toggle site sync statuses
- Runners redirect their logs in a file placed in the user folder (bce8aadf)
- A new `DefaultRunner` is available to let the OS choose the default application for a given file path.
- Previews and renders of AfterEffects file revisions can be launched at revision and episode level, given AfterEffectsRender render settings and output module templates
- Playblasts of blender file revisions can be made with an action (*preview* folder created in department's files if not already added)
- Md5 hash is computed for publishes for later features (cc0478e8)

### Changed

- According to the new `get_root()` function added and requiered by issue #4, the default contextual dict doens't provide a `ROOT_DIR` value anymore. Calls to that value have been changed, and you must define `ROOT_DIR_WINDOWS`, `ROOT_DIR_LINUX` and/or `ROOT_DIR_MAC` in the admin panel.
- Cosmetic changes to get some maps expanded or not (832605d8).
- There is no need to manually specify the user folder anymore: project's `get_user_folder()` method now returns the path to a `.libreflow` in the user's home directory.
- For sake of readability, file maps showcase the time elapsed since file last modification, instead of date (59d364a8).

## [1.0.3] - 2020-12-24

### Fixed

issue #7 libreflow icons are missing from the distributed package (and also the example packages where not accessible)

## [1.0.2-1.0.1] - 2020-12-23

Initial public commit and pypi setup. This version is an early version of libreflow. It includes a baseflow and examples flows overriding the baseflow. We have been working on departments, files, file version history, and stuff like that.

### Fixed

issue #6 : Pip Package is now ready for use


[^1]: Except we started libreflow MAJOR version number at 1, as we consider our in-house previous flow being version 0.