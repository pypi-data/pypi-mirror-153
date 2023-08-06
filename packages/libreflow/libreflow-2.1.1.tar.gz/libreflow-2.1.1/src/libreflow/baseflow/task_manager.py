import os
import time
from kabaret import flow
from kabaret.flow_contextual_dict import get_contextual_dict
from kabaret.app.ui.gui.icons import gui

from ..resources.icons import gui, libreflow
from .runners import CHOICES_ICONS


DEFAULT_PATH_FORMAT = '{film}/{sequence}/{shot}/{task}/{file_mapped_name}/{revision}/{film}_{sequence}_{shot}_{file_base_name}'


def get_icon(file_name):
    _, ext = os.path.splitext(file_name)
    icon = ('icons.gui', 'folder-white-shape')
    if ext:
        icon = CHOICES_ICONS.get(
            ext[1:], ('icons.gui', 'text-file-1')
        ) 

    return icon


# Task default files
# -------------------------


class SelectDefaultFileAction(flow.Action):

    _default_file = flow.Parent()
    _map          = flow.Parent(2)

    def needs_dialog(self):
        return False
    
    def allow_context(self, context):
        return False
    
    def run(self, button):
        if self._default_file.exists.get():
            return
        
        self._default_file.create.set(
            not self._default_file.create.get()
        )
        self._map.touch()


class TaskDefaultFileViewItem(flow.SessionObject):
    """
    Describes a default file to be created in the list of
    files of a task.
    """
    file_name   = flow.Param()
    path_format = flow.Param()
    create      = flow.BoolParam()
    exists      = flow.BoolParam()

    select      = flow.Child(SelectDefaultFileAction)


class TaskDefaultFileView(flow.DynamicMap):

    _task = flow.Parent(2)

    def __init__(self, parent, name):
        super(TaskDefaultFileView, self).__init__(parent, name)
        self._cache = None
        self._cache_ttl = 5
        self._cache_birth = None
        self._cache_key = None

    @classmethod
    def mapped_type(cls):
        return TaskDefaultFileViewItem

    def mapped_names(self, page_num=0, page_size=None):
        cache_key = (page_num, page_size)
        if (
            self._cache is None
            or self._cache_key != cache_key
            or self._cache_birth < time.time() - self._cache_ttl
        ):
            self._mng.children.clear()

            mgr = self.root().project().get_task_manager()
            default_files = mgr.get_task_files(
                self._task.name(), enabled_only=True
            )

            self._cache = {}

            for file_name, path_format, optional in default_files:
                n = file_name.replace('.', '_')
                self._cache[n] = dict(
                    file_name=file_name,
                    path_format=path_format,
                    create=not optional,
                    exists=self._file_exists(file_name)
                )
            
            self._cache_birth = time.time()
            self._cache_key = cache_key
        
        return self._cache.keys()
    
    def columns(self):
        return ['Do create', 'File']
    
    def _configure_child(self, child):
        self.mapped_names()
        child.file_name.set(self._cache[child.name()]['file_name'])
        child.path_format.set(self._cache[child.name()]['path_format'])
        child.create.set(self._cache[child.name()]['create'])
        child.exists.set(self._cache[child.name()]['exists'])
    
    def _fill_row_cells(self, row, item):
        row['Do create'] = ''
        row['File'] = item.file_name.get()
    
    def _fill_row_style(self, style, item, row):
        style['File_icon'] = get_icon(item.file_name.get())
        style['Do create_activate_oid'] = item.select.oid()

        if item.exists.get():
            style['Do create_icon'] = ('icons.gui', 'check-box-empty-dark')
            for col in self.columns():
                style['%s_foreground-color' % col] = '#4e5255'
        elif item.create.get():
            style['Do create_icon'] = ('icons.gui', 'check')
        else:
            style['Do create_icon'] = ('icons.gui', 'check-box-empty')
    
    def _file_exists(self, file_name):
        name, ext = os.path.splitext(file_name)
        if ext:
            exists = self._task.files.has_file(name, ext[1:])
        else:
            exists = self._task.files.has_folder(name)
        return exists


class CreateTaskDefaultFiles(flow.Action):

    files = flow.Child(TaskDefaultFileView)

    _task = flow.Parent()

    def get_buttons(self):
        task = self._task.name()
        self.message.set(f'<h2>Create {task} default files</h2>')
        return ['Create', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        for df in self.files.mapped_items():
            if df.create.get() and not df.exists.get():
                self._create_file(df)
    
    def _create_file(self, default_file):
        file_name = default_file.file_name.get()
        name, ext = os.path.splitext(file_name)
        if ext:
            self._task.files.add_file(
                name, ext[1:],
                display_name=file_name,
                tracked=True,
                default_path_format=default_file.path_format.get()
            )
        else:
            self._task.files.add_folder(
                name,
                display_name=file_name,
                tracked=True,
                default_path_format=default_file.path_format.get()
            )


# Default file presets
# -------------------------


class PathFormatValue(flow.values.SessionValue):

    def revert_to_default(self):
        settings = get_contextual_dict(self, 'settings')
        path_format = settings.get('path_format')
        if path_format is None:
            super(PathFormatValue, self).revert_to_default()
        else:
            self.set(path_format)


class CreateDefaultFileAction(flow.Action):
    """
    Allows to create a default file in the parent map.
    """

    ICON = ('icons.gui', 'plus-sign-in-a-black-circle')

    file_name   = flow.SessionParam('').ui(
        placeholder='layout.blend'
    )
    path_format = flow.SessionParam(DEFAULT_PATH_FORMAT, PathFormatValue).ui(
        placeholder='{film}/{shot}/{file}/{revision}'
    )
    enabled     = flow.SessionParam(True).ui(editor='bool')
    optional    = flow.SessionParam(False).ui(editor='bool')

    _map = flow.Parent()

    def get_buttons(self):
        self.message.set('<h2>Create a default file</h2>')
        self.path_format.revert_to_default()
        return ['Add', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        elif not self._filename_is_valid():
            return self.get_result(close=False)
        
        mapped_name = self.file_name.get().replace('.', '_')
        path_format = self.path_format.get() or None # Consider empty path format as undefined

        df = self._map.add(mapped_name)
        df.file_name.set(self.file_name.get())
        df.enabled.set(self.enabled.get())
        df.optional.set(self.optional.get())
        df.path_format.set(path_format)

        self._map.touch()
    
    def _filename_is_valid(self):
        title = '<h2>Create a default file</h2>'

        if self.file_name.get() == '':
            self.message.set((
                f'{title}<font color=#D66700>'
                'File name must not be empty.</font>'
            ))
            return False
        
        for df in self._map.mapped_items():
            if self.file_name.get() == df.file_name.get():
                self.message.set((
                    f'{title}<font color=#D66700>A default file '
                    f'named <b>{self.file_name.get()}</b> already '
                    'exists. Please choose another name.</font>'
                ))
                return False
        
        return True


class DefaultFile(flow.Object):
    """
    Defines a preset used to create a file in the project.
    """

    file_name   = flow.Param()
    path_format = flow.Param()
    enabled     = flow.BoolParam(False)
    optional    = flow.BoolParam(False)


class DefaultFiles(flow.Map):

    add_dft_file = flow.Child(CreateDefaultFileAction).ui(
        label='Add default file'
    )

    @classmethod
    def mapped_type(cls):
        return DefaultFile
    
    def columns(self):
        return ['Enabled', 'Name']
    
    def _fill_row_cells(self, row, item):
        row['Name'] = item.file_name.get()
        row['Enabled'] = ''
    
    def _fill_row_style(self, style, item, row):
        style['Name_icon'] = get_icon(item.file_name.get())
        style['Enabled_icon'] = (
            'icons.gui',
            'check' if item.enabled.get() else 'check-box-empty'
        )


# Task UI types
# -------------------------


class TaskColor(flow.values.SessionValue):

    DEFAULT_EDITOR = 'choice'

    def choices(self):
        mgr = self.root().project().get_task_manager()
        return mgr.template_colors.get()
    
    def update_default_value(self):
        choices = self.choices()
        if choices:
            self._value = choices[0]
        self.touch()


class EditTaskColorAction(flow.Action):

    color = flow.SessionParam(None, TaskColor)

    _task_color = flow.Parent()

    def get_buttons(self):
        self.color.update_default_value()
        return ['Save', 'Cancel']
    
    def allow_context(self, context):
        return context and context.endswith('.inline')
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        self._task_color.set(self.color.get())


class EditableTaskColor(flow.values.Value):

    edit = flow.Child(EditTaskColorAction)


# Default tasks
# -------------------------


class EditDefaultTaskFile(flow.Action):
    """
    Allows to edit a default task's file.
    """

    ICON = ('icons.libreflow', 'edit-blank')

    path_format = flow.SessionParam(DEFAULT_PATH_FORMAT, PathFormatValue).ui(
        placeholder='{film}/{shot}/{file}/{revision}'
    )
    enabled     = flow.SessionParam().ui(editor='bool')
    optional    = flow.SessionParam().ui(editor='bool')

    _dft_file   = flow.Parent()
    _map        = flow.Parent(2)
    _dft_task   = flow.Parent(3)

    def get_buttons(self):
        self.message.set(f'<h2>Edit default file {self._dft_file.file_name.get()}</h2>')
        self.path_format.set(self._dft_file.path_format.get())
        self.enabled.set(self._dft_file.enabled.get())
        self.optional.set(self._dft_file.optional.get())

        buttons = ['Save']
        mgr = self.root().project().get_task_manager()
        task_template = mgr.task_templates[self._dft_task.template.get()]

        if task_template.files.has_mapped_name(self._dft_file.name()):
            buttons.append('Restore default')
        
        return buttons + ['Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return

        if button == 'Restore default':
            self._map.edits.remove(self._dft_file.name())
        else:
            if self._map.edits.has_mapped_name(self._dft_file.name()):
                dft_file = self._map.edits[self._dft_file.name()]
            else:
                mgr = self.root().project().get_task_manager()
                task_template = mgr.task_templates[self._dft_task.template.get()]
                file_name = task_template.files[self._dft_file.name()].file_name.get()
                dft_file = self._map.edits.add(self._dft_file.name())
                dft_file.file_name.set(file_name)
            
            dft_file.path_format.set(self.path_format.get())
            dft_file.enabled.set(self.enabled.get())
            dft_file.optional.set(self.optional.get())


        self._map.touch()


class AddDefaultTaskFileEdit(flow.Action):
    """
    Allows to add a file in the files of a default task.
    """

    file_name   = flow.SessionParam('').ui(label='Name')
    path_format = flow.SessionParam(DEFAULT_PATH_FORMAT, PathFormatValue)
    enabled     = flow.SessionParam(True).ui(editor='bool')
    optional    = flow.SessionParam(False).ui(editor='bool')

    _map = flow.Parent()

    def get_buttons(self):
        self.message.set('<h2>Add default task file</h2>')
        self.path_format.revert_to_default()
        return ['Add', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        elif not self._filename_is_valid():
            self.message.set((
                f'<font color=#D66700>A default file '
                f'named <b>{self.file_name.get()}</b> already '
                'exists. Please choose another name.</font>'
            ))
            return self.get_result(close=False)
        
        file_name = self.file_name.get()
        df = self._map.edits.add(file_name.replace('.', '_'))
        df.file_name.set(self.file_name.get())
        df.path_format.set(self.path_format.get())
        df.enabled.set(self.enabled.get())
        df.optional.set(self.optional.get())

        self._map.touch()
    
    def _filename_is_valid(self):
        title = '<h2>Add default task file</h2>'

        if self.file_name.get() == '':
            self.message.set((
                f'{title}<font color=#D66700>'
                'File name must not be empty.</font>'
            ))
            return False
        
        for df in self._map.mapped_items():
            if self.file_name.get() == df.file_name.get():
                self.message.set((
                    f'{title}<font color=#D66700>A default file '
                    f'named <b>{self.file_name.get()}</b> already '
                    'exists. Please choose another name.</font>'
                ))
                return False
        
        return True


class DefaultTaskFile(flow.SessionObject):

    file_name   = flow.Param().ui(editable=False)
    path_format = flow.Param().ui(editable=False)
    enabled     = flow.BoolParam().ui(editable=False)
    optional    = flow.BoolParam().ui(editable=False)
    is_edit     = flow.BoolParam().ui(editable=False)

    edit        = flow.Child(EditDefaultTaskFile)


class DefaultTaskFiles(flow.DynamicMap):

    edits = flow.Child(DefaultFiles).ui(hidden=True)

    add_dft_file = flow.Child(AddDefaultTaskFileEdit).ui(label='Add default file')

    _default_task = flow.Parent()

    def mapped_names(self, page_num=0, page_size=None):
        self._mng.children.clear()

        mgr = self.root().project().get_task_manager()
        task_template = mgr.task_templates[self._default_task.template.get()]
        default_names = task_template.files.mapped_names()
        edit_names = set(self.edits.mapped_names())

        self._cache = {}

        # Collect default files (potentially edited)
        for name in default_names:
            data = {}
            if name in edit_names:
                default_file = self.edits[name]
                data['is_edit'] = True
                edit_names.remove(name)
            else:
                default_file = task_template.files[name]
                data['is_edit'] = False
            data.update(dict(
                file_name=default_file.file_name.get(),
                path_format=default_file.path_format.get(),
                enabled=default_file.enabled.get(),
                optional=default_file.optional.get()
            ))
            self._cache[name] = data
        
        # Collect remaining edits
        for name in edit_names:
            default_file = self.edits[name]
            data = dict(
                file_name=default_file.file_name.get(),
                path_format=default_file.path_format.get(),
                enabled=default_file.enabled.get(),
                optional=default_file.optional.get(),
                is_edit=True
            )
            self._cache[name] = data
        
        return self._cache.keys()
    
    @classmethod
    def mapped_type(cls):
        return DefaultTaskFile
    
    def _configure_child(self, child):
        child.file_name.set(self._cache[child.name()]['file_name'])
        child.path_format.set(self._cache[child.name()]['path_format'])
        child.enabled.set(self._cache[child.name()]['enabled'])
        child.optional.set(self._cache[child.name()]['optional'])
        child.is_edit.set(self._cache[child.name()]['is_edit'])
    
    def columns(self):
        return ['Enabled', 'Name']
    
    def _fill_row_cells(self, row, item):
        row['Name'] = item.file_name.get()
        row['Enabled'] = ''
    
    def _fill_row_style(self, style, item, row):
        style['Name_icon'] = get_icon(item.file_name.get())
        style['Enabled_icon'] = (
            'icons.gui',
            'check' if item.enabled.get() else 'check-box-empty'
        )
        style['activate_oid'] = item.edit.oid()


class TaskTemplateName(flow.values.SessionValue):

    DEFAULT_EDITOR = 'choice'

    def choices(self):
        mgr = self.root().project().get_task_manager()
        return mgr.task_templates.mapped_names()
    
    def update_default_value(self):
        choices = self.choices()
        if choices:
            self._value = choices[0]
        self.touch()


class EditTaskTemplateNameAction(flow.Action):

    template = flow.SessionParam(None, TaskTemplateName)

    _task_template = flow.Parent()

    def get_buttons(self):
        self.template.update_default_value()
        return ['Save', 'Cancel']
    
    def allow_context(self, context):
        return context and context.endswith('.inline')
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        self._task_template.set(self.template.get())


class EditableTaskTemplateName(flow.values.Value):

    edit = flow.Child(EditTaskTemplateNameAction)


class CreateDefaultTaskAction(flow.Action):

    ICON = ('icons.gui', 'plus-sign-in-a-black-circle')

    task_name    = flow.SessionParam('')
    display_name = flow.SessionParam('')
    template     = flow.SessionParam(None, TaskTemplateName)
    position     = flow.SessionParam(0).ui(editor='int')
    enabled      = flow.SessionParam(True).ui(
        editor='bool',
        tooltip='Dictates if the task must appear in the UI by default')
    optional     = flow.SessionParam(False).ui(
        editor='bool',
        tooltip='Dictates if the task must be created automatically')

    _map      = flow.Parent()

    def get_buttons(self):
        self.template.update_default_value()

        if len(self.template.choices()) == 0:
            self.message.set((
                '<h2>Add default task</h2>'
                '<font color=#D5000D>Please add a template '
                'before creating a default task.</font>'
            ))
            return ['Cancel']
        
        self.message.set('<h2>Add default task</h2>')
        return ['Add', 'Cancel']

    def run(self, button):
        if button == 'Cancel':
            return
        
        self._map.add_default_task(
            self.task_name.get(),
            self.display_name.get(),
            self.template.get(),
            self.position.get(),
            self.enabled.get(),
            self.optional.get()
        )


class DefaultTask(flow.Object):
    """
    Defines a set of presets used to create a task in the project.

    These presets include UI elements (display name and position),
    dictate if the associated tasks are enabled in the project and
    optional at creation time.
    In addition, each default task has a task template, and holds
    a set of parameters and a list of default files used to
    override the template's defaults.
    """

    display_name = flow.Param()
    position     = flow.IntParam(0)
    enabled      = flow.BoolParam(True)
    optional     = flow.BoolParam(False)

    # Template and parameters overriding its configuration
    template     = flow.Param(None, EditableTaskTemplateName).ui(editable=False)
    color        = flow.Param(None, EditableTaskColor)
    icon         = flow.Param()
    files        = flow.Child(DefaultTaskFiles).ui(expanded=True)

    def get_color(self):
        color = self.color.get()

        if color is None:
            mgr = self.root().project().get_task_manager()
            tp = mgr.task_templates[self.template.get()]
            color = tp.color.get()
        
        return color

    def get_icon(self):
        icon = self.icon.get()

        if icon is None:
            mgr = self.root().project().get_task_manager()
            tp = mgr.task_templates[self.template.get()]
            icon = tp.icon.get()
        
        return icon


class DefaultTasks(flow.Map):

    add_dft_task = flow.Child(CreateDefaultTaskAction).ui(
        label='Add default task'
    )

    @classmethod
    def mapped_type(cls):
        return DefaultTask

    def add_default_task(self, name, display_name, template_name, position=-1, enabled=True, optional=False):
        if position < 0:
            position = len(self)
        
        dt = self.add(name)
        dt.display_name.set(display_name)
        dt.template.set(template_name)
        dt.enabled.set(enabled)
        dt.optional.set(optional)
        self._mapped_names.set_score(name, position)
        
        self.touch()
    
    def _fill_row_style(self, style, item, row):
        style['icon'] = item.get_icon()
        style['foreground-color'] = item.get_color()


# Task templates
# -------------------------


class CreateTaskTemplateAction(flow.Action):

    ICON = ('icons.gui', 'plus-sign-in-a-black-circle')

    template_name = flow.SessionParam('').ui(label='Name')
    color         = flow.SessionParam(None, TaskColor)

    _map = flow.Parent()

    def get_buttons(self):
        self.color.update_default_value()
        self.message.set('<h2>Add task template</h2>')
        return ['Add', 'Cancel']

    def run(self, button):
        if button == 'Cancel':
            return
        
        tt = self._map.add(self.template_name.get())
        tt.color.set(self.color.get())
        self._map.touch()


class TaskTemplate(flow.Object):
    """
    A task template defines a generic task configuration,
    which can be overriden by default tasks.
    """
    
    color = flow.Param(None, EditableTaskColor)
    icon  = flow.Param(('icons.gui', 'cog-wheel-silhouette'))
    files = flow.Child(DefaultFiles).ui(expanded=True)


class TaskTemplates(flow.Map):

    add_template = flow.Child(CreateTaskTemplateAction)

    @classmethod
    def mapped_type(cls):
        return TaskTemplate
    
    def _fill_row_style(self, style, item, row):
        style['icon'] = item.icon.get()
        style['foreground-color'] = item.color.get()


# Task manager
# -------------------------


class TaskManager(flow.Object):
    """
    The task manager embeds an ordered list of default task
    names and a list of task templates
    """

    default_tasks  = flow.Child(DefaultTasks).ui(expanded=True)
    task_templates = flow.Child(TaskTemplates).ui(expanded=True)
    template_colors = flow.OrderedStringSetParam().ui(hidden=True)

    def get_task_color(self, task_name):
        dt = self.default_tasks[task_name]
        return dt.get_color()
    
    def get_task_icon(self, task_name):
        dt = self.default_tasks[task_name]
        return dt.get_icon()

    def get_task_files(self, task_name, enabled_only=False):
        """
        Returns a list of tuples describing the default files
        of a task with the given name.
        
        Tuples follow the layout (<file name>, <path format>).
        """
        files = []
        if self.default_tasks.has_mapped_name(task_name):
            dt = self.default_tasks[task_name]
            files = [
                (
                    df.file_name.get(),
                    df.path_format.get(),
                    df.optional.get(),
                )
                for df in dt.files.mapped_items()
                if not enabled_only or df.enabled.get()
            ]
        
        return files
