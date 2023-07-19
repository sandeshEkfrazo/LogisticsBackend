from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import *

# Create your views here.

# @method_decorator([AutorizationRequired], name='dispatch')
class StatusView(APIView):
    def get(self,request):
        id = request.query_params.get('id')
        if id:
            all_data = Status.objects.filter(id=id).values()

            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = Status.objects.all().values()
            return Response({'result':{'status':'GET','data':all_data}})

    def post(self,request):
        data = request.data
        status_name=data.get('status_name')
        colour=data['colour']

        selected_page_no =1
        page_number = request.GET.get('page')
        if page_number:
            selected_page_no = int(page_number)

        try:
            emp_role = Status.objects.create(
                        status_name=status_name,
                        colour=colour
                    )
            posts = Status.objects.all().values()
            paginator = Paginator(posts,10)
            try:
                page_obj = paginator.get_page(selected_page_no)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        status_name=data.get('status_name')
        colour=data.get('colour')

        try:
            emp_role= Status.objects.filter(id=pk).update(status_name=status_name,
                                                            colour=colour,
                                            )

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})

    def delete(self,request,pk):
        test = (0,{})
        all_values = Status.objects.filter(id=pk).delete()
        if test == all_values:

            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'result':{'status':'deleted'}})