from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import *
from .serializers import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.utils import IntegrityError
from logisticsapp.views import convertBase64

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


class FilesizeApi(APIView):
    def get(self,request):
        data = request.data
        if request.query_params:
            file_obj = Filesize.objects.filter(id=request.query_params['id']).values('id','file_type','size')
            return Response({'data': file_obj})
        else:
            file_obj = Filesize.objects.values('id','file_type','size')
            return Response({'data': file_obj})

    def post(self,request):
        data = request.data
        file_type=data.get('file_type')
        # print('file_type',file_type)
        size=data.get('size')
        if Filesize.objects.filter(file_type__iexact=file_type).exists():
            return Response({'error':'File type already exists!!!'},status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            remark_obj= Filesize.objects.create(file_type=file_type,size=size)
            return Response({'data':'File type Successfully Added!!'})

    def put(self,request,pk):
        data = request.data
        file_type=data.get('file_type')
        size=data.get('size')
        if Filesize.objects.filter(id=pk).exists():
            Filesize.objects.filter(id=pk).update(file_type=file_type,size=size)
            return Response({'message': 'Filesize is updated'})
        else:
            return Response({'error':'Filesize id is not found'},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,pk):
        data = request.data
        if Filesize.objects.filter(id=pk).exists():
            Filesize.objects.filter(id=pk).delete()
            return Response({'message': 'Filesize is deleted'})
        else:
            return Response({'error':'Filesize id is not found'},status=status.HTTP_404_NOT_FOUND)


class QueriesApi(APIView):
    def get(self, request):
        data = request.data
        if request.query_params:
            query_obj = Queries.objects.filter(id=request.query_params['id']).values('id', 'isfor',
                                                                                     'isfor__user_role_name',
                                                                                     'questions', 'answer', 'status')
            return Response({'data': query_obj})
        else:
            query_obj = Queries.objects.all().values('id', 'isfor', 'isfor__user_role_name', 'questions', 'answer',
                                                     'status')
            return Response({'data': query_obj})

    def post(self, request):
        data = request.data
        isfor = data['isfor']
        questions = data['questions']
        answer = data['answer']
        status = data['status']
        # print(status,'ddddddddd===??????')
        if UserRoleRef.objects.filter(id=isfor).exists():
            obj = UserRoleRef.objects.get(id=data['isfor'])
            # print('obj=====>>',obj)
            Queries.objects.create(questions=questions, answer=answer, status=status, isfor_id=obj.id)
            return Response({'message': 'Query is created'})
        else:
            return Response({'error': 'Query id is not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        data = request.data
        isfor = data['isfor']
        questions = data['questions']
        answer = data['answer']
        status = data['status']
        if Queries.objects.filter(id=pk).exists():
            Queries.objects.filter(id=pk).update(questions=questions, answer=answer, status=status, isfor=isfor)
            return Response({'message': 'Query is updated'})
        else:
            return Response({'error': 'aboutus id not found'}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, pk):
        data = request.data
        if Queries.objects.filter(id=pk).exists():
            Queries.objects.filter(id=pk).delete()
            return Response({'message': 'Query is deleted'})
        else:
            return Response({'error': 'Query id is not found'}, status=status.HTTP_404_NOT_FOUND)


class LanguageApi(APIView):
    def get(self, request):
        data = request.data
        if request.query_params:
            query_obj = Language.objects.filter(id=request.query_params['id']).values('id', 'name')
            return Response({'data': query_obj})
        else:
            query_obj = Language.objects.all().values('id', 'name')
            return Response({'data': query_obj})

    def post(self, request):
        data = request.data
        name = data['name']
        if Language.objects.filter(name__iexact=name).exists():
            return Response({'error': 'language already exists!!!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            lang_obj = Language.objects.create(name=name)
            return Response({'message': 'Successfully added Language'})

    def put(self, request, pk):
        data = request.data
        name = data.get('name')

        if Language.objects.filter(id=pk).exists():

            lang_obj = Language.objects.filter(id=pk).update(name=name)
            return Response({'message': 'Successfully update Language'})
        else:
            return Response({'error': 'Language id not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        data = request.data
        if Language.objects.filter(id=pk).exists():
            lang_obj = Language.objects.filter(id=pk).delete()
            return Response({'message': 'Successfully delete Language'})
        else:
            return Response({'error': 'Language id not found!!'}, status=status.HTTP_404_NOT_FOUND)

class SubscriptionplanApi(APIView):
    def get(self,request):
        data = request.data
        if request.query_params:
            query_obj = Subscriptionplan.objects.filter(id=request.query_params['id']).values('id','time_period','validity_days','amount','type_of_service','status')
            return Response({'data':query_obj})
        else:
            query_obj = Subscriptionplan.objects.all().values('id','time_period','validity_days','amount','type_of_service','status')
            return Response({'data':query_obj})

    def post(self,request):
        data = request.data
        time_period = data['time_period']
        validity_days=data['validity_days']
        amount = data['amount']
        type_of_service=data['type_of_service']
        status=data['status']

        Subscriptionplan.objects.create(time_period=time_period,validity_days=validity_days,amount=amount,type_of_service=type_of_service,status=status)
        return Response({'message': 'Query is created'})

    def put(self,request,pk):
        data = request.data
        time_period = data['time_period']
        validity_days=data['validity_days']
        amount = data['amount']
        type_of_service=data['type_of_service']
        status=data['status']
        if Subscriptionplan.objects.filter(id=pk).exists():
            Subscriptionplan.objects.filter(id=pk).update(time_period=time_period,validity_days=validity_days,amount=amount,type_of_service=type_of_service,status=status)
            return Response({'message': 'Query is updated'})
        else:
            return Response({'error':'aboutus id not found'})

    def delete(self,request,pk):
        data = request.data
        if Subscriptionplan.objects.filter(id=pk).exists():
            Subscriptionplan.objects.filter(id=pk).delete()
            return Response({'message': 'Query is deleted'})
        else:
            return Response({'error':'Query id is not found'},status=status.HTTP_404_NOT_FOUND)


class AboutusApi(APIView):
    def get(self,request):
        id = request.query_params.get('id')
        if id:
            all_data = Aboutus.objects.filter(id=request.query_params['id']).values('id','logo','heading','paragraph','phone_number','email','alternate_phone_number','text')

            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
            return Response({'result':{'status':'GET by Id','data':all_data}})

        else:
            all_data = Aboutus.objects.all().values()
            return Response({'result':{'status':'GET','data':all_data}})

    def post(self,request):
        data = request.data
        logo = data['logo']
        heading=data['heading']
        paragraph=data['paragraph']
        phone_number=data['phone_number']
        alternate_phone_number=data['alternate_phone_number']
        text=data['text']
        email  =data['email']
        logo=data['logo']
        if Aboutus.objects.exists():
            # converted_logo = convertBase64(logo, 'logo', heading, "logos")
            return Response({'error':'Data already present in the DB!!'},status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            converted_logo = convertBase64(logo, 'logo', heading, "logos")
            about = Aboutus.objects.create(logo=converted_logo,heading=heading,paragraph=paragraph,phone_number=phone_number,alternate_phone_number=alternate_phone_number,email=email,text=text)
            return Response({'message':'Successfully added Aboutus'})

    def put(self,request,pk):
        data = request.data
        logo=data.get('logo')
        heading=data['heading']
        paragraph=data['paragraph']
        phone_number=data['phone_number']
        alternate_phone_number=data['alternate_phone_number']
        text=data['text']
        email  =data['email']
        if Aboutus.objects.filter(id=pk).exists():
            converted_logo = convertBase64(logo, 'logo', heading, "logos")
            Aboutus.objects.filter(id=pk).update(logo=converted_logo,heading=heading,paragraph=paragraph,phone_number=phone_number,alternate_phone_number=alternate_phone_number,text=text,email=email)
            return Response({'message':'Successfully update Aboutus'})
        else:
            return Response({'error':'aboutus id not found'},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,pk):
        data = request.data
        if Aboutus.objects.filter(id=pk).exists():
            Aboutus.objects.filter(id=pk).delete()
            return Response({'message':'Successfully delete Aboutus'})
        else:
            return Response({'error':'aboutus id not found!!'},status=status.HTTP_404_NOT_FOUND)


class BookingDistanceApiView(APIView):

    def get(self, request):
        booking_distances = BookingDistance.objects.all()
        serializer = BookingDistanceSerializer(booking_distances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        threshold_value = data.get('threshold_value')
        incremented_value = data.get('incremented_value')
        description = data.get('description')

        if not (threshold_value and incremented_value and description ):
            return Response({"message": "Missing required field"}, status=status.HTTP_400_BAD_REQUEST)

        distance = BookingDistance.objects.create(threshold_value=threshold_value,
                                                  incremented_value=incremented_value,description=description)
        serializer = BookingDistanceSerializer(distance)
        return Response({"message": "Data added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        try:
            distance = BookingDistance.objects.get(pk=pk)
        except BookingDistance.DoesNotExist:
            return Response({"message": "Booking distance not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data

        threshold_value = data.get('threshold_value')
        incremented_value = data.get('incremented_value')
        description = data.get('description')

        if threshold_value is not None:
            distance.threshold_value = threshold_value

        if incremented_value is not None:
            distance.incremented_value = incremented_value

        if description is not None:
            distance.description = description

        distance.save()

        serializer = BookingDistanceSerializer(distance)
        return Response({"message": "Data updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        try:
            booking_distance = BookingDistance.objects.get(pk=pk)
        except BookingDistance.DoesNotExist:
            return Response({"error": "Booking distance not found."}, status=status.HTTP_404_NOT_FOUND)

        booking_distance.delete()
        return Response({"Message": "Data deleted succesfully."},status=status.HTTP_204_NO_CONTENT)
