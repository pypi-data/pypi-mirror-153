from kabaret import flow
from kabaret.flow_entities.entities import Entity, Property

from ..utils.kabaret.flow_entities.entities import EntityView
from .file import FileSystemMap
from .maputils import SimpleCreateAction
from .task_manager import CreateTaskDefaultFiles


class Task(Entity):
    """
    Defines an arbitrary task containing a list of files.

    Instances provide the `task` and `task_display_name` keys
    in their contextual dictionary (`settings` context).
    """
    
    display_name = Property().ui(hidden=True)
    enabled      = Property().ui(hidden=True, editor='bool')

    files = flow.Child(FileSystemMap).ui(
        expanded=True,
        action_submenus=True,
        items_action_submenus=True
    )

    @classmethod
    def get_source_display(cls, oid):
        split = oid.split('/')
        return f'{split[3]} · {split[5]} · {split[7]} · {split[9]}'
    
    def get_default_contextual_edits(self, context_name):
        if context_name == 'settings':
            return dict(
                task=self.name(),
                task_display_name=self.display_name.get(),
            )


class TaskCollection(EntityView):
    """
    Defines a collection of tasks.
    """

    add_task = flow.Child(SimpleCreateAction)

    @classmethod
    def mapped_type(cls):
        return flow.injection.injectable(Task)
    
    def collection_name(self):
        mgr = self.root().project().get_entity_manager()
        return mgr.get_task_collection().collection_name()


class DefaultTaskName(flow.values.SessionValue):

    DEFAULT_EDITOR = 'choice'

    def choices(self):
        mgr = self.root().project().get_task_manager()
        return mgr.default_tasks.mapped_names()
    
    def update_default_value(self):
        choices = self.choices()
        if choices:
            self._value = choices[0]
        self.touch()


class CreateDefaultTasksAction(flow.Action):
    """
    Allows to create a task among the default tasks defined
    in the project's task manager.
    """

    ICON = ('icons.gui', 'plus-sign-in-a-black-circle')

    task = flow.Param(None, DefaultTaskName)

    _map = flow.Parent()

    def get_buttons(self):
        self.task.update_default_value()
        return ['Add', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        task_name = self.task.get()
        mgr = self.root().project().get_task_manager()
        dt = mgr.default_tasks[task_name]
        t = self._map.add(task_name)
        t.display_name.set(dt.display_name.get())
        self._map.touch()


class ManagedTask(Task):
    """
    A ManagedTask provides features handled by the task
    manager of the project.
    """

    create_dft_files = flow.Child(CreateTaskDefaultFiles).ui(
        label='Create default files'
    )


class ManagedTaskCollection(TaskCollection):

    add_dft_task = flow.Child(CreateDefaultTasksAction).ui(
        label='Add default task'
    )

    @classmethod
    def mapped_type(cls):
        return flow.injection.injectable(ManagedTask)

    def _fill_row_style(self, style, item, row):
        mgr = self.root().project().get_task_manager()
        style['icon'] = mgr.get_task_icon(item.name())
        style['foreground-color'] = mgr.get_task_color(item.name())
