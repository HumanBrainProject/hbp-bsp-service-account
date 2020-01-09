# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from service_account.settings import ENABLED_HPC as HPC
from service_account.settings import DEFAULT_PROJECT


class Hpc(models.Model):
    name = models.CharField(max_length=100)
    host_institution = models.CharField(max_length=100)
    acronym = models.CharField(max_length=50)
    cpus = models.IntegerField()
    gpus = models.IntegerField()


class Project(models.Model):
    name = models.CharField(max_length=100)
    hpc = models.CharField(max_length=20, choices=HPC)
    init_time = models.IntegerField()
    init_space = models.FloatField()
    time_left = models.IntegerField(null=True)
    space_left = models.FloatField(null=True)
    user_time = models.IntegerField(default=18000000)  # time_left in seconds - 18,000,000 s = 5000 h
    user_space = models.FloatField(default=10000000)  # space_left in KB - 10,000,000 KB = 10 GB

    class Meta:
        unique_together = (('name', 'hpc'),)

    def __str__(self):
        return '<hpc:("' + str(self.hpc) + '", name:("' + str(self.name) + '")>'

    def save(self, *args, **kwargs):
        if not self.time_left:
            self.time_left = self.init_time
        if not self.space_left:
            self.space_left = self.init_space
        return super(Project, self).save(*args, **kwargs)

    def print_all(self):
        print '{\n' \
            + '     id: "' + str(self.id) + '"\n' \
            + '     hpc: "' + str(self.hpc) + '"\n' \
            + '     init_time: "' + str(self.init_time) + '"\n' \
            + '     init_space: "' + str(self.init_space) + '"\n' \
            + '     time_left: "' + str(self.time_left) + '"\n' \
            + '     space_left: "' + str(self.space_left) + '"\n' \
            + '     user_time: "' + str(self.user_time) + '"\n' \
            + '     user_space: "' + str(self.user_space) + '"\n' \
            + '}'


class User(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    institution = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=2, blank=True)
    is_admin = models.BooleanField(default=False)
    # groups identify the projects id
    groups = models.CharField(max_length=100, default='')
    # banned from project by id in the form like: "1, 2, 3..."
    banned_from = models.CharField(max_length=100, default='')

    def __str__(self):
        return '<id:("' + str(self.id) + '"), username:("' + str(self.username) + '")>'

    def print_all(self):
        print '{\n' \
            + '  id: "' + str(self.id) + '"\n' \
            + '  username: "' + str(self.username) + '"\n' \
            + '  email: "' + str(self.email) + '"\n' \
            + '  institution: "' + str(self.institution) + '"\n' \
            + '  country: "' + str(self.country) + '"\n' \
            + '  is_admin: "' + str(self.is_admin) + '"\n' \
            + '  groups: "' + str(self.groups) + '"\n' \
            + '  banned_from: "' + str(self.banned_from) + '"\n' \
            + '}'

    def add_group(self, project_id):
        if not isinstance(project_id, str):
            project_id = str(project_id)
        if project_id in self.groups.split(','):
            return None
        self.groups += project_id + ','
        self.save()

    def remove_group(self, project_id):
        if not isinstance(project_id, str):
            project_id = str(project_id)
        if project_id in self.groups.split(','):
            self.groups = self.groups.replace(project_id + ',', '')
            self.save()
        else:
            raise ValueError

    def ban(self, project_id):
        if not isinstance(project_id, str):
            project_id = str(project_id)
        if project_id in self.groups.split(','):
            return None
        self.banned_from += project_id + ','
        self.save()

    def unban(self, project_id):
        if not isinstance(project_id, str):
            project_id = str(project_id)
        if project_id in self.banned_from.split(','):
            self.banned_from = self.banned_from.replace(project_id + ',', '')
            self.save()
        else:
            raise ValueError

    def save(self, *args, **kwargs):
        if self.institution == '' or not self.institution:
            self.institution = 'UNKNOWN'
        if self.country == '' or not self.country:
            self.country = 'IT'
        if self.groups == '':
            for h in HPC:
		project = Project.objects.get(hpc=h[0], name=DEFAULT_PROJECT[h[0]])
                self.groups += str(project.id) + ','
        return super(User, self).save(*args, **kwargs)


class Quota(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    time_left = models.IntegerField(blank=True, null=True)
    space_left = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = (('user', 'project'),)

    def __str__(self):
        return '<user:"(' + str(self.user) + '"), project:("' + str(self.project) + '"), ' \
                '(time_left:"' + str(self.time_left) + '", space_left:"' + str(self.space_left) + '")>'

    def save(self, *args, **kwargs):
        if not self.time_left:
            self.time_left = self.project.user_time
        if not self.space_left:
            self.space_left = self.project.user_space
        return super(Quota, self).save(*args, **kwargs)

    def add(self, time=None, space=None):
        if time:
            self.time_left += time
        if space:
            self.space_left += space
        self.save()

    def sub(self, time=None, space=None):
        if time:
            if self.time_left - time < 0:
                raise ValueError
            self.time_left -= time
        if space:
            if self.space_left - space < 0:
                raise ValueError
            self.space_left -= space
        self.save()


class Job(models.Model):
    job_id = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100, blank=True, default='')
    init_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    runtime = models.FloatField()
    stage = models.CharField(max_length=20)
    terminal_stage = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)

    class Meta:
        unique_together = (('job_id', 'project'),)

    def __str__(self):
        return '<owner(' + str(self.owner) + '), job_id(' + str(self.job_id) + '), project(' + str(self.project) + ')>'

    def print_all(self):
        print '{\n' \
              + '  id: "' + str(self.id) + '"\n' \
              + '  job_id: "' + str(self.job_id) + '"\n' \
              + '  owner: "' + str(self.owner) + '"\n' \
              + '  project: "' + str(self.project) + '"\n' \
              + '  init_date: "' + str(self.init_date) + '"\n' \
              + '  end_date: "' + str(self.end_date) + '"\n' \
              + '  runtime: "' + str(self.runtime) + '"\n' \
              + '  stage: "' + str(self.stage) + '"\n' \
              + '  terminal_stage: "' + str(self.terminal_stage) + '"\n' \
              + '  failed: "' + str(self.failed) + '"\n' \
              + '}'
