from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, ProfileCreateSerializer, UserDetailsSerilizer, DayDataSerializer
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth import authenticate
from datetime import date
from datetime import timedelta
import datetime
import random
from .models import *

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        userSerializer = UserRegisterSerializer(data = request.data['user'])
        
        if userSerializer.is_valid():
            #save the user
            user = userSerializer.save()
            user.set_password(userSerializer.data['password'])
            user.save()

            #save the profile
            request.data['profile']['user'] = user.id
            profileSerializer = ProfileCreateSerializer(data = request.data['profile'])
            if profileSerializer.is_valid():
                newProfile = profileSerializer.save()

                responseData = {
                    "token": AuthToken.objects.create(user)[1],
                    "user":UserDetailsSerilizer(user).data
                }

                return Response(responseData, status=201)
            return Response(profileSerializer.errors, status=400)
        return Response(userSerializer.errors, status=400)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        user = authenticate(username = request.data['email'], password = request.data['password'])
        if user is not None:
            responseData = {
                "token": AuthToken.objects.create(user)[1],
                "user":UserDetailsSerilizer(user).data
            }
            return Response(responseData, status=200)
        return Response({'Msg': 'Invlid Details'}, status=401)


class DataToday(APIView):
    def get(self, request, *args, **kwargs):
        today = date.today()
        print(today.weekday)
        print("Today is: ", today)


        userProfile = UserProfile.objects.filter(user__username = 'ian10@gmail.com').first()

        #create todays data
        # today_new = UserData(day = today, user = userProfile)
        # today_new.save()
        # userTodayData = UserData.objects.filter(day = today, user = userProfile).first()
        # current_value = 79.950
        # for j in range(1, 25):
        #     print(current_value)
        #     add = round(random.uniform(0, 0.3), 2)
        #     current_value += add
        #     print(current_value)
        #     userTodayData.__dict__['hour_'+str(j)] = current_value
        # userTodayData.save()
        
        # Yesterday date
        yesterday = today - timedelta(days = 1)

        # juzi
        before_yesterday = yesterday - timedelta(days = 1)

        print("Yesterday was: ", yesterday)

        current_hour = datetime.datetime.today().hour

        userProfile = UserProfile.objects.filter(user__username = 'ian10@gmail.com').first()
        # userDayData = UserData(day = before_yesterday, user = userProfile)
        # userDayData.save()

        #regenerate 2 days ago data.
        # day_before_2_days_ago = before_yesterday - timedelta(days = 1)
        # day_before_2_days_ago_reading = UserData.objects.filter(user = userProfile, day = day_before_2_days_ago).first().hour_24
        
        # before_yesterday_data = UserData.objects.filter(day = before_yesterday, user = userProfile).first()
        # current_value = float(day_before_2_days_ago_reading)
        # for j in range(1, 25):
        #     print(current_value)
        #     add = round(random.uniform(0, 0.3), 2)
        #     current_value += add
        #     print(current_value)
        #     before_yesterday_data.__dict__['hour_'+str(j)] = current_value
        # before_yesterday_data.save()

        yesterday_reading = UserData.objects.filter(user = userProfile, day = yesterday).first().hour_24
        before_yesterday_reading = UserData.objects.filter(user = userProfile, day = before_yesterday).first().hour_24
        today_reading = UserData.objects.filter(user = userProfile, day = today).first()

        print(today_reading)
        print(yesterday_reading)

        today_data = []
        for i in range(1, 25):
            if i == 1:
                today_data.append(float(today_reading.__dict__['hour_'+str(i)]) - float(yesterday_reading))
            else:

                today_data.append(float(today_reading.__dict__['hour_'+str(i)]) - float(today_reading.__dict__['hour_'+str(i-1)]))
        
        print(today_data)

        data = {
            'yester_reading': yesterday_reading - before_yesterday_reading,
            'today_reading':today_reading.__dict__['hour_'+str(current_hour)] - yesterday_reading,
            'today_data': today_data
        }


        return Response({'Data': data}, status=200)

class ReceiveData(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        return Response({'Msg': 'Success'}, status=201)
    def get(self, request, *args, **kwargs):
        print(request.data)
        return Response({'Msg':'success'}, status=200)
    
class WeeksData(APIView):
    def get(self, request, *args, **kwargs):
        #get current hour reading
        today = date.today()
        current_hour = datetime.datetime.today().hour

        userProfile = UserProfile.objects.filter(user__username = 'ian10@gmail.com').first()
        #get last week saturady 24 hour
        #if it's saturday
        week_day = today.isocalendar().weekday
        if(week_day == 5):
            day_difference = 7
        else:
            day_difference = (week_day + 1) % 7
        
        last_day_last_week = today - timedelta(days = day_difference)
        print('last day week 1:', last_day_last_week)

        last_day_two_week = today - timedelta(days = day_difference+7)
        print('last day week 2:', last_day_two_week)

        #get the data
        userProfile = UserProfile.objects.filter(user__username = 'ian10@gmail.com').first()
        count = 1
        this_week_data = []

        while (count <= day_difference):
            current_day = last_day_last_week + timedelta(days = count)
            previous_day = current_day - timedelta(days = 1)

            previous_day_reading = UserData.objects.filter(user = userProfile, day = previous_day).first().hour_24

            if count == day_difference:
                current_hour = datetime.datetime.today().hour
                current_day_reading = UserData.objects.filter(user = userProfile, day = current_day).first().__dict__['hour_'+str(current_hour)]
            else:
                 current_day_reading = UserData.objects.filter(user = userProfile, day = current_day).first().hour_24
            
            this_week_data.append(current_day_reading - previous_day_reading)
            count += 1
        
        #differences
        last_week_reading = UserData.objects.filter(user = userProfile, day = last_day_last_week).first().hour_24
        print('last week reading', last_week_reading)
        amount_this_week = current_day_reading - last_week_reading
        amount_last_week = last_week_reading - UserData.objects.filter(user = userProfile, day = last_day_two_week).first().hour_24


        data = {
            'week_data': this_week_data,
            'amount_last_week': amount_last_week,
            'amount_this_week': amount_this_week
        }
        
        return Response({'data': data}, status=200)

class MonthlyData(APIView):
    def get(self, request, *args, **kwargs):
        today = date.today()
        now = datetime.datetime.now()
        current_hour = now.hour
        current_month = now.month
        userProfile = UserProfile.objects.filter(user__username = 'ian10@gmail.com').first()
        print(current_hour)

        if now.year % 4 == 0:
            feb = 29
        else:
            feb = 28
        months = [31,feb,31,30,31,30,31,31,30,31,30,31]
        months_data = []
        for i in range(1, current_month+1):
            current_month_last_day = date(now.year, i, months[i-1])

            if i == 1:
                last_month_last_day = date(now.year, i, months[i])
            else:
                last_month_last_day = date(now.year, i-1, months[i-2])

            if i == 1:
                first_day_jan = date(now.year, 1, 1) #to be changed to read dec 31 hour 24
                last_reading_last_month = UserData.objects.filter(day=first_day_jan, user = userProfile).first().hour_1
            else:
                 last_reading_last_month = UserData.objects.filter(day=last_month_last_day, user = userProfile).first().hour_24
            
            if i+1 == current_month:
                last_reading_current_month = UserData.objects.filter(day=today, user = userProfile).first().__dict__['hour_'+str(current_hour)]
            else:
                last_reading_current_month = UserData.objects.filter(day=current_month_last_day, user = userProfile).first().hour_24
           

            amount_spent = last_reading_current_month - last_reading_last_month

            months_data.append(amount_spent)
        
        #expenditure between last month and this month
        if current_month == 1:
            last_month_expenditure = 0
        else:
            last_month_last_day = date(today.year, current_month-1, months[current_month-2])
            last_2_months_last_day = date(today.year, current_month-2, 1)
            reading_last_day_of_1_month_ago = UserData.objects.filter(day=last_month_last_day, user = userProfile).first().hour_24
            reading_last_day_of_2_months_ago = UserData.objects.filter(day=last_2_months_last_day, user = userProfile).first().hour_24

            last_month_expenditure = reading_last_day_of_1_month_ago - reading_last_day_of_2_months_ago

        data = {
            'month_data': months_data,
            'last_month_expenditure': last_month_expenditure,
            'this_month_expenditure': months_data[-1]
        }

        return Response({'data': data})


class Test(APIView):
    def get(self, request, *args, **kwargs):
        #delete all the days
        # all_data = User.objects.all()
        # for data in all_data:
        #     data.delete()

        
        # new_user = User(username='ian10@gmail.com', email='ian10@gmail.com')
        # new_user.set_password('12345678')
        # new_user.save()
        # userProfile = UserProfile(user = new_user, firstName = 'Ian', lastName = 'Mark', meterNumber = '123456789', phoneNumber = '0796417598')
        # userProfile.save()

        #userProfile = UserProfile.objects.filter(user__username = 'ian10@gmail.com').first()
        
        # today = date.today()
        # current_value = 0
        # data = {}
        # for i in range(21, -1, -1):
        #     current_day = today - timedelta(days=i)
        #     userDayData = UserData.objects.filter(day = current_day, user = userProfile).first()
        #     # userDayData.save()            
            
        #     # for j in range(1, 25):
        #     #     print(current_value)
        #     #     add = round(random.uniform(0, 0.3), 2)
        #     #     current_value += add
        #     #     print(current_value)
        #     #     userDayData.__dict__['hour_'+str(j)] = current_value
        #     #     userDayData.save()
            
        #     current_day_data = DayDataSerializer(UserData.objects.filter(user = userProfile, day = current_day).first()).data
        #     data[i] = current_day_data

        #create dummy data for the whole of this year
        # first_day_of_the_year = date(2023, 1, 1)
        # current_reading = 20
        # for i in range(365):
        #     current_day = first_day_of_the_year + timedelta(days=i)
        #     new_data = UserData(day = current_day, user = userProfile)
        #     for k in range(1, 25):
        #         print(current_reading)
        #         new_data.__dict__['hour_'+str(k)] = current_reading
        #         add = round(random.uniform(0, 0.3), 2)
        #         current_reading += add
        #         new_data.save()
        
        return Response({'Msg': 'success'}, status=200)
