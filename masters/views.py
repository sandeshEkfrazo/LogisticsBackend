from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import *
from .serializers import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.utils import IntegrityError
from logisticsapp.views import convertBase64
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from logistics_project.pagination import CustomPagination
from django.utils.decorators import method_decorator
from account.auth import authorization_required
# Create your views here.

@method_decorator([authorization_required], name='dispatch')
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
            queryset = Status.objects.all()

            # Apply pagination
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            # Serialize paginated data
            serializer = StatusSerializer(paginated_queryset, many=True)
            if self.request.query_params.get('page_size') is None and self.request.query_params.get('page') is None:
                return Response({'result':{'status':'GET','data':queryset.values()}})
            else:
                return paginator.get_paginated_response(serializer.data)

    def post(self,request):
        data = request.data
        status_name=data.get('status_name')
        colour=data['colour']

        selected_page_no =1
        page_number = request.GET.get('page')

        if Status.objects.filter(Q(status_name=status_name)).exists():
            return Response({'message': 'status name already exists'}, status=status.HTTP_404_NOT_FOUND)
        else:
            Status.objects.create(
                        status_name=status_name,
                        colour=colour
                    )

            return Response({'message': 'status created successfully'})

    def put(self,request,pk):
        data = request.data
        status_name=data.get('status_name')
        colour=data.get('colour')

        if Status.objects.filter(~Q(id=pk) & Q(status_name=status_name)).exists():
            return Response({'message': 'status name already exists'}, status=status.HTTP_404_NOT_FOUND)
        else:
            Status.objects.filter(id=pk).update(
                        status_name=status_name,
                        colour=colour
                    )

            return Response({'message': 'status created successfully'})
        
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


@method_decorator([authorization_required], name='dispatch')
class FilesizeApi(APIView):
    def get(self,request):
        data = request.data
        if request.query_params.get('id'):
            file_obj = Filesize.objects.filter(id=request.query_params['id']).values('id','file_type','size')
            return Response({'data': file_obj})
        else:
            # file_obj = Filesize.objects.values('id','file_type','size')
            # return Response({'data': file_obj})

            queryset = Filesize.objects.all()

            # Apply pagination
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            # Serialize paginated data
            serializer = FileSizeSerializer(paginated_queryset, many=True)
            if self.request.query_params.get('page_size') is None and self.request.query_params.get('page') is None:
                return Response({'data': queryset.values('id','file_type','size')})
            else:
                return paginator.get_paginated_response(serializer.data)

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
        if Filesize.objects.filter(~Q(id=pk) & Q(file_type=file_type)).exists():
            return Response({'error': 'File type name already taken'}, status=status.HTTP_404_NOT_FOUND)
        else:
            Filesize.objects.filter(id=pk).update(file_type=file_type,size=size)
            return Response({'message': 'Filesize is updated'})
        # else:
        #     return Response({'error':'Filesize id is not found'},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,pk):
        data = request.data
        if Filesize.objects.filter(id=pk).exists():
            Filesize.objects.filter(id=pk).delete()
            return Response({'message': 'Filesize is deleted'})
        else:
            return Response({'error':'Filesize id is not found'},status=status.HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class QueriesApi(APIView):
    def get(self, request):
        data = request.data
        if request.query_params.get('id'):
            query_obj = Queries.objects.filter(id=request.query_params['id']).values('id', 'isfor',
                                                                                     'isfor__user_role_name',
                                                                                     'questions', 'answer', 'status')
            return Response({'data': query_obj})
        else:
            # query_obj = Queries.objects.all().values('id', 'isfor', 'isfor__user_role_name', 'questions', 'answer',
            #                                          'status')
            # return Response({'data': query_obj})

            queryset = Queries.objects.all()

            # Apply pagination
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            # Serialize paginated data
            serializer = QueriesSerializer(paginated_queryset, many=True)
            if self.request.query_params.get('page_size') is None and self.request.query_params.get('page') is None:
                return Response({'data': queryset.values('id', 'isfor', 'isfor__user_role_name', 'questions', 'answer','status')})
            else:
                return paginator.get_paginated_response(serializer.data)

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

@method_decorator([authorization_required], name='dispatch')
class LanguageApi(APIView):
    def get(self, request):
        data = request.data
        if request.query_params.get('id'):
            query_obj = Language.objects.filter(id=request.query_params['id']).values('id', 'name')
            return Response({'data': query_obj})
        else:
            # query_obj = Language.objects.all().values('id', 'name')
            # return Response({'data': query_obj})

            queryset = Language.objects.all()

            # Apply pagination
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            # Serialize paginated data
            serializer = LanguageSerializer(paginated_queryset, many=True)
            if self.request.query_params.get('page_size') is None and self.request.query_params.get('page') is None:
                return Response({'data': queryset.values('id', 'name')})
            else:
                return paginator.get_paginated_response(serializer.data)

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

            if Language.objects.filter(~Q(id=pk) & Q(name=name)).exists():
                return Response({'error': 'Language name already taken'}, status=status.HTTP_406_NOT_ACCEPTABLE)

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

# @method_decorator([authorization_required], name='dispatch')
class SubscriptionplanApi(APIView):
    def get(self,request):
        data = request.data
        if request.query_params.get('id'):
            query_obj = Subscriptionplan.objects.filter(id=request.query_params['id']).values('id','time_period','validity_days','amount','type_of_service','status')
            
            return Response({'data':query_obj})
        else:
            # query_obj = Subscriptionplan.objects.all().values('id','time_period','validity_days','amount','type_of_service','status')
            # return Response({'data':query_obj})

            queryset = Subscriptionplan.objects.all()

            # Apply pagination
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            # Serialize paginated data
            serializer = SubscriptionSerializer(paginated_queryset, many=True)
            if self.request.query_params.get('page_size') is None and self.request.query_params.get('page') is None:
                return Response({'data': queryset.values('id','time_period','validity_days','amount','type_of_service','status')})
            else:
                return paginator.get_paginated_response(serializer.data)

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

@method_decorator([authorization_required], name='dispatch')
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
            queryset = Aboutus.objects.all()

            # Apply pagination
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            # Serialize paginated data
            serializer = AboutusSerializer(paginated_queryset, many=True)
            if self.request.query_params.get('page_size') is None and self.request.query_params.get('page') is None:
                return Response({'data': queryset.values()})
            else:
                return paginator.get_paginated_response(serializer.data)
            # all_data = Aboutus.objects.all().values()
            # return Response({'result':{'status':'GET','data':all_data}})

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
        last_km_value = data.get('last_km_value')

        if not (threshold_value and incremented_value and description and last_km_value):
            return Response({"message": "Missing required field"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            distance = BookingDistance.objects.get()
            # If a record exists, raise an exception with the error message
            return Response ({"message": "You are allowed to add only one data."}, status=status.HTTP_400_BAD_REQUEST)
            # raise ValidationError("Data already exists. Use PUT request to update it.")
        except BookingDistance.DoesNotExist:
            # If a record doesn't exist, create a new one
            distance = BookingDistance.objects.create(threshold_value=threshold_value,
                                                      incremented_value=incremented_value,
                                                      description=description,
                                                      last_km_value=last_km_value)

        serializer = BookingDistanceSerializer(distance)
        return Response({"message": "Data added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    # def post(self, request):
    #     data = request.data
    #     threshold_value = data.get('threshold_value')
    #     incremented_value = data.get('incremented_value')
    #     description = data.get('description')
    #     last_km_value = data.get('last_km_value')
    #
    #     if not (threshold_value and incremented_value and description and last_km_value ):
    #         return Response({"message": "Missing required field"}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     distance = BookingDistance.objects.create(threshold_value=threshold_value,
    #                                               incremented_value=incremented_value,description=description,last_km_value=last_km_value)
    #     serializer = BookingDistanceSerializer(distance)
    #     return Response({"message": "Data added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        try:
            distance = BookingDistance.objects.get(pk=pk)
        except BookingDistance.DoesNotExist:
            return Response({"message": "Booking distance not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data

        threshold_value = data.get('threshold_value')
        incremented_value = data.get('incremented_value')
        description = data.get('description')
        last_km_value = data.get('last_km_value')

        if threshold_value is not None:
            distance.threshold_value = threshold_value

        if incremented_value is not None:
            distance.incremented_value = incremented_value

        if description is not None:
            distance.description = description

        if last_km_value is not None:
            distance.last_km_value  = last_km_value

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


class CustomizavleTimeSearchApiView(APIView):

    def get(self, request):
        time = Timesearch.objects.all()
        serializer = TimeSerachSerializer(time, many=True)
        return Response({"data" : serializer.data}, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        threshold_value = data.get('threshold_value')
        incremented_value = data.get('incremented_value')
        description = data.get('description')
        last_km_value = data.get('last_km_value')

        if not (threshold_value and incremented_value and description and last_km_value):
            return Response({"message": "Missing required field"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            distance = BookingDistance.objects.get()
            # If a record exists, raise an exception with the error message
            return Response ({"message": "You are allowed to add only one data."}, status=status.HTTP_400_BAD_REQUEST)
            # raise ValidationError("Data already exists. Use PUT request to update it.")
        except BookingDistance.DoesNotExist:
            # If a record doesn't exist, create a new one
            distance = BookingDistance.objects.create(threshold_value=threshold_value,
                                                      incremented_value=incremented_value,
                                                      description=description,
                                                      last_km_value=last_km_value)

        serializer = BookingDistanceSerializer(distance)
        return Response({"message": "Data added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def post(self, request):
        data = request.data
        time = data.get('time')
        description = data.get('description')


        if not (time and description ):
            return Response({"message": "Missing required field"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            timeSearch = Timesearch.objects.get()
            return Response({"message": "You are allowed to add only one data."},
                        status=status.HTTP_400_BAD_REQUEST)
        except Timesearch.DoesNotExist:


            timeSearch = Timesearch.objects.create(time=time,description=description)
        serializer = TimeSerachSerializer(timeSearch)
        return Response({"message": "Data added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        try:
            searchtime = Timesearch.objects.get(pk=pk)
        except Timesearch.DoesNotExist:
            return Response({"message": "Data not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data

        time = data.get('time')
        description = data.get('description')


        if time is not None:
            searchtime.time = time

        if description is not None:
            searchtime.time = time


        searchtime.save()

        serializer = TimeSerachSerializer(searchtime)
        return Response({"message": "Data updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        try:
            searchtime = Timesearch.objects.get(pk=pk)
        except Timesearch.DoesNotExist:
            return Response({"error": " not found."}, status=status.HTTP_404_NOT_FOUND)

        searchtime.delete()
        return Response({"Message": "Data deleted succesfully"},status=status.HTTP_204_NO_CONTENT)