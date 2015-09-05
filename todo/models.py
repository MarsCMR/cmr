
# coding:utf-8

from datetime import date
from datetime import datetime
from django.db import models
from django.utils import dateformat
from django.utils.safestring import SafeUnicode
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
import logging


STATUS_STS = (
	(u'0', u'未着手'),
	(u'1', u'対応中(順調)'),
	(u'2', u'対応中(遅延)'),
	(u'3', u'完了待ち'),
	(u'4', u'完了'),
	(u'5', u'保留'),
	(u'6', u'中止'),
)

STATUS_PRIORITY = (
	(u'0', u'最高'),
	(u'1', u'高'),
	(u'2', u'中'),
	(u'3', u'低'),
)


class Todo(models.Model):

	title = models.CharField(u"タイトル",max_length=300,blank=True,null=False)
	task = models.TextField(u"対応内容",blank=True,null=True)
	taskdetail = models.TextField(u"タスク",blank=True,null=True)
	priority = models.CharField(u"優先度", max_length=1, choices=STATUS_PRIORITY, null=False)
	status = models.CharField(u"STS", max_length=1, choices=STATUS_STS, null=False)
	limitdate = models.DateField(u"★期限",blank=True,null=True)
	startdate = models.DateField(u"開始日",blank=True,null=True)
	finishdate = models.DateField(u"完了日",blank=True,null=True)
	memo = models.TextField(u"メモ",blank=True,null=True)

	class Meta:
		verbose_name = u'タスク'
		verbose_name_plural = u'タスク一覧'

	#def __unicode__(self):
		#return u'{0} {1}'.format(self.startdate, self.limitdate)

	def __unicode__(self):
		return u'{0}'.format(self.title)

	def task_no(self):
		#logger.info(u"%s" % self)    
		try:
			#logger.info(u"ID: %d, Name: %s" % (self.id, self.title))    
			return u'{0:04d}'.format(self.id)
		except:
		        #logger.info(u"except")    
			return u'自動採番'
	task_no.short_description = u'タスク番号'

	#list一覧の期限日付表示制御
	def limitdate4list(self):
		if self.limitdate is None:
			return u''
		else:
			if self.status < '4' and self.limitdate < date.today():
				return SafeUnicode(u'<span style="color:#FF6666;font-weight:bold;">{0}</span>'.format(dateformat.format(self.limitdate, 'y/m/d(D)')))
			else:
				return dateformat.format(self.limitdate, 'y/m/d(D)')
	limitdate4list.short_description = u'★期限'
	limitdate4list.admin_order_field = 'limitdate'

	#list一覧のSTS表示
	def status4list(self):
		if self.status is None:
			return u''
		else:
		
			#超過日数計算
			if self.status in ['0', '1', '2', '3']:
				if self.limitdate.toordinal() > date.today().toordinal():
					count = self.limitdate.toordinal() - date.today().toordinal()
					message = u'(' + u'残り' + str(count) + u'日' + u')'
				elif self.limitdate.toordinal() == date.today().toordinal():
					message = u'(本日期限)'	
				else:
					count = date.today().toordinal() - self.limitdate.toordinal()		
					message = u'(' +  u'超過' + str(count) + u'日' + u')'
				
			#STS色変更
			if self.status == '0':
				return SafeUnicode(u'<span style="color:#999999;";text-align: right>{0}{1}</span>'.format(u'未着手　',message))
			if self.status == '1':
				return SafeUnicode(u'<span style="color:#000000;font-weight:bold;">{0}{1}</span>'.format(u'順調　　',message))	
			if self.status == '2':
				return SafeUnicode(u'<span style="color:#FF6666;font-weight:bold;">{0}{1}</span>'.format(u'遅延　　',message))
			if self.status == '3':
				return SafeUnicode(u'<span style="color:#000000;">{0}{1}</span>'.format(u'完了待ち',message))				
			if self.status == '4':
				return SafeUnicode(u'<span style="color:#000000;">{0}</span>'.format(u'完了'))				
			if self.status == '5':
				return SafeUnicode(u'<span style="color:#CCCCCC;">{0}</span>'.format(u'保留'))			
			if self.status == '6':
				return SafeUnicode(u'<span style="color:#CCCCCC;">{0}</span>'.format(u'中止'))										
			else:
				return self.status
	status4list.short_description = u'STS'
	status4list.admin_order_field = 'status'
	
'''
Situation: stepClass
'''
class Step(models.Model):
	todo = models.ForeignKey(Todo, unique=False)
	process = models.TextField(u"タスク詳細")
	required_time = models.DecimalField(u"予定工数(MD)",max_digits=3, decimal_places=2,blank=False,null=True,validators=[MinValueValidator(0.01),MaxValueValidator(9)])
	actual_time = models.DecimalField(u"実績工数(MD)",max_digits=3, decimal_places=2,blank=True,null=True,validators=[MinValueValidator(0.01),MaxValueValidator(9)])

	class Meta:
		verbose_name = u'詳細'
		verbose_name_plural = u'一覧'
