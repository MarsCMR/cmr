#from django.http import HttpResponse
#from django.template import RequestContext, loader
#from django.shortcuts import render
#from django.http import Http404

#from todo.models import Todo
#from todo.models import Step

#def index(todo):
#    report_list = Report.objects.all()
#    template = loader.get_template('report/index.html')
#    #context = RequestContext(request, {
#    #    'report_list': report_list,
#    #})
#    context = {'report_list':report_list}
#    return render(request, 'report/index.html', context)
#    #return HttpResponse(template.render(context))
#
#def detail(request, report_id):
#    try:
#        report = Report.objects.get(pk=report_id)
#    except Report.DoesNotExist:
#        raise Http404("Report does not exist")
#    return render(request, 'report/detail.html', {'report':report})
