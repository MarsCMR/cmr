# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime
from django.contrib import admin
from django import forms
from models import Todo
from models import Step
from django.utils import dateformat
from django.utils.safestring import SafeUnicode
from urlparse import urlparse
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.conf import settings

class TodoAdminForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(TodoAdminForm, self).__init__(*args, **kwargs)
		self.fields['title'].widget.attrs = {'size':'80'}

		self.fields['task'].widget.attrs = {'rows':3, 'cols':'80'}
		#self.fields['taskdetail'].widget.attrs = {'rows':10, 'cols':'80'}
		self.fields['memo'].widget.attrs = {'rows':2, 'cols':'80'}
		if self.instance.limitdate:
			if self.instance.status < '4' and self.instance.limitdate < date.today():
				self.fields['limitdate'].widget.attrs = {'class':'vDateFieldBgPink'}
				self.fields['limitdate'].help_text = u'対応期限を過ぎています'

	# 完了日とSTSの関連チェック
	def clean_finishdate(self):
		date = self.cleaned_data['finishdate']
		status = self.cleaned_data['status']
        	if status == '4' and date is None:
			# 状況を完了にしているのに完了日を設定していない場合にエラーとします
			raise forms.ValidationError(u'完了にする場合、完了日も入力してください。')
		return date

	# 開始日とSTSの関連チェック
	def clean_startdate(self):
		date = self.cleaned_data['startdate']
		status = self.cleaned_data['status']
        	if status == '0' and date is None:
			# 状況を未着手にしているのに開始日を設定していない場合にエラーとします
			raise forms.ValidationError(u'未着手の場合、開始日を入力してください。')
		return date

class StepAdminForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(StepAdminForm, self).__init__(*args, **kwargs)
		if 'process' in self.fields:
			if len(self.instance.process) == 0:
				# 新規入力フォームの場合
				self.fields['process'].widget.attrs = {'rows':3, 'cols':80}
				self.fields['process'].widget.attrs['class'] = 'vAddContentsArea'
				self.fields['required_time'].widget.attrs = {'size':'6'}
				self.fields['actual_time'].widget.attrs = {'size':'6'}
			else:
				lfcnt = self.instance.process.count('\n')
				self.fields['process'].widget.attrs = {'rows':lfcnt + 2, 'cols':50, 'class':'vExistContentsArea'}
				self.fields['required_time'].widget.attrs = { 'size':'6', 'class':'vExistContentsArea'}
				self.fields['actual_time'].widget.attrs = { 'size':'6', 'class':'vExistContentsArea'}

'''
StepInline: タスク詳細記載Class
タスク詳細を一覧表示させるためのクラスです。
'''
class AddStepInline(admin.StackedInline):
	model = Step
	form = StepAdminForm
	extra = 0

	fieldsets = [
		(None, {'fields': [('process','required_time','actual_time',), ]}),
	]

	def has_change_permission(self, todo, obj=None):
		return False

class StepInline(admin.StackedInline):
	model = Step
	form = StepAdminForm
	extra = 0

	#readonly_fields = ()

	fieldsets = [
		(None, {'fields': [('process','required_time','actual_time',)] }),
	]

	#ordering = ('todo.id',)

	def has_add_permission(self, todo):
		return False

'''
StatusFilter: 状態フィルタClass
右側に表示される状態フィルタ
'''
class StatusFilter(admin.SimpleListFilter):
	title = u'状態'
	parameter_name = 'status'

	""" lookupsはフィルタを表示する際に呼ばれる関数です"""
	def lookups(self, request, model_admin):
		choice = ((u'UNFIN', u'★未完了'),(u'OTHER', u'☆保留／中止'),(u'FIN', u'完了'), )
		return choice

	""" querysetはフィルタが実行された際に呼ばれる関数です"""
	def queryset(self, request, queryset):
		if self.value() is None or self.value() == 'ALL':
			# 全てとなっている場合、全部返します
			return queryset
		if self.value() == 'UNFIN':
			# UNFINすなわち未完了が指定された場合、未着手／対応中／完了待ちのタスクを返します
			return queryset.filter(status__in=[u'0', u'1', u'2', u'3'])
		if self.value() == 'OTHER':
			# OHTERすなわち保留＆中止が指定された場合、保留と中止のタスクを返します
			return queryset.filter(status__in=[u'5', u'6'])
		if self.value() == 'FIN':
			# FINすなわち完了が指定された場合、完了のタスクを返します
			return queryset.filter(status__in=[u'4'])


class TodoAdmin(admin.ModelAdmin):
	actions = None
	save_on_top = True
	search_fields = ('title', 'task', 'taskdetail', 'memo',)
	readonly_fields = ('task_no',)
	list_filter = (StatusFilter,'priority',)
	ordering = ('status','priority','limitdate')
        form = TodoAdminForm

	list_display = ('task_no', 'title', 'status4list', 'priority', 'limitdate4list',)
	list_display_links = ('title',)
	fieldsets = [
	(u'概要', {'fields': ['task_no','title', ('priority', 'status','limitdate',),('startdate', 'finishdate',),'task', ('memo',), ]}),
	]
	inlines = [AddStepInline, StepInline]

	""" changelist_viewは一覧が表示される際に呼ばれる関数です。 """
	def changelist_view(self, request, extra_context=None):
		if request.META.has_key('HTTP_REFERER'):
			o = urlparse(request.META['HTTP_REFERER'])
			if not o.path.endswith("/todo/") and not request.GET.has_key('status'):
				# statusに関するクエリパラメータが無い場合、すなわち初期表示などの場合
				q = request.GET.copy()
				q['status'] = 'UNFIN'  # このように状況フィルタを強制的にUNFIN(未完了)にしています。
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()
		return super(TodoAdmin,self).changelist_view(request, extra_context=extra_context)


admin.site.register(Todo, TodoAdmin)
#admin_site.register(Step, StepAdmin)
