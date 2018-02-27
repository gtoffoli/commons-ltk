from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField, AutoSlugField
from django_dag.models import node_factory, edge_factory

from .vocabularies import Language


PORT_TYPE_CHOICES = (
    (1, 'in'),
    (2, 'out'),)

"""TaskType class.

Together with the related classes, TaskType defines the requirements,
the outputs and the callable implementing a kind of atomic process.

"""
class TaskType(models.Model):
    name = models.TextField(verbose_name=_('name'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    callable = models.TextField(blank=True, verbose_name=_('callable'))
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('creator'), related_name='task_type_created')
    modified = ModificationDateTimeField(_('modified'))

    class Meta:
        verbose_name = _('task type')
        verbose_name_plural = _('task tipes')

"""ParameterType class.

ParameterType supports the enumeration of different type of parameters,
including the constraints on the ranges of their values.

"""
class ParameterType(models.Model):
    name = models.TextField(verbose_name=_('name'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('creator'), related_name='parameter_type_created')
    modified = ModificationDateTimeField(_('modified'))

    class Meta:
        verbose_name = _('parameter type')
        verbose_name_plural = _('parameter tipes')

"""TargetType class.

TargetType supports the enumeration of different type of targets.

"""
class TargetType(models.Model):
    name = models.TextField(verbose_name=_('name'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('creator'), related_name='target_type_created')
    modified = ModificationDateTimeField(_('modified'))

    class Meta:
        verbose_name = _('target type')
        verbose_name_plural = _('target tipes')

"""TaskFormalParameter class.

The instances of this class, matching a task type with a parameter type,
define the parameters affecting the behaviour of the callable associated to tasks of a certain type.
They also specify if a parameter is required and possibly its default value.

"""
class TaskFormalParameter(models.Model):
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, verbose_name=_('target type'))
    parameter_type = models.ForeignKey(ParameterType, on_delete=models.CASCADE, verbose_name=_('parameter type'))
    order = models.IntegerField(blank=True, default=0)
    required = models.IntegerField(default=0, null=True, verbose_name='required')
    default_value = models.TextField(blank=True, verbose_name=_('parameter value'))

    class Meta:
        verbose_name = _('task formal parameter')
        verbose_name_plural = _('task formal parameters')

"""TaskFormalTarget class.

The instances of this class, matching a task type with a target type,
define number, name and type of the input targets to be processed by the callable
associated to tasks of a certain type, with possible defaults,
as well as number, name and type of the output targets. 

"""
class TaskFormalTarget(models.Model):
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, verbose_name=_('target type'))
    target_type = models.ForeignKey(TargetType, on_delete=models.CASCADE, verbose_name=_('parameter type'))
    required = models.IntegerField(default=0, null=True, verbose_name='required')
    default_value = models.TextField(blank=True, verbose_name=_('parameter value'))

    class Meta:
        verbose_name = _('task formal parameter')
        verbose_name_plural = _('task formal parameters')

"""Pipeline class.

The role of instances of this class is to define pipeline templates.

"""
class Pipeline(models.Model):
    label = models.TextField(blank=True, verbose_name=_('label'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('creator'), related_name='pipeline_created')
    modified = ModificationDateTimeField(_('modified'))

    class Meta:
        verbose_name = _('pipeline')
        verbose_name_plural = _('pipeline')

    def run(self):
        pass

"""Target.

A target is a node in a pipeline.

"""
class Target(node_factory('Task')):
    label = models.TextField(blank=True, verbose_name=_('label'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    target_type = models.ForeignKey(TargetType, on_delete=models.CASCADE, verbose_name=_('target_of_type'))
    reference = models.TextField(blank=True, verbose_name=_('reference'))
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('creator'), related_name='target_created')
    modified = ModificationDateTimeField(_('modified'))

    class Meta:
        verbose_name = _('target')
        verbose_name_plural = _('targets')

"""Task.

A Task is an edege in a Pipeline.

"""
class Task(edge_factory('Target', concrete = False)):
    label = models.TextField(blank=True, verbose_name=_('label'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, verbose_name=_('task_of_type'))
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('pipeline'))
    parameters = JSONField('Parameters')
    state = models.IntegerField(default=0, null=True, verbose_name='task state')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('creator'), related_name='task_created')
    modified = ModificationDateTimeField(_('modified'))

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('task')

    def run(self):
        pass

"""PipelineRun.

A PipelineRun represents the execution of a Pipeline.

"""
class PipelineRun(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, verbose_name=_('pipeline template'), related_name='pipeline_run')
    executor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('creator'), related_name='pipeline_executed')
    start_time = models.DateTimeField(_('modified'))
    end_time = models.DateTimeField(_('modified'))

    class Meta:
        verbose_name = _('pipeline execution')
        verbose_name_plural = _('pipeline executions')

    def run(self):
        pass

"""TaskRun.

A TaskRun represents the execution of a Task
possibly inside the exection of a Pipeline

"""
class TaskRun(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name=_('task'))
    pipeline_run = models.ForeignKey(PipelineRun, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('pipeline_execution'))
    state = models.IntegerField(default=0, null=True, verbose_name='task state')
    executor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('creator'), related_name='task_executed')
    start_time = models.DateTimeField(_('modified'))
    end_time = models.DateTimeField(_('modified'))

    class Meta:
        verbose_name = _('task execution')
        verbose_name_plural = _('task executions')

    def run(self):
        pass
