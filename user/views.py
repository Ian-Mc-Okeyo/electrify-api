from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, ProfileCreateSerializer, UserDetailsSerilizer, DayDataSerializer, MeterCreateSerializer
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
                print

                request.data['meter']['user'] = newProfile.id

                meterSerializer = MeterCreateSerializer(data = request.data['meter'])
                
                if meterSerializer.is_valid():
                    meterSerializer.save()

                    responseData = {
                        "token": AuthToken.objects.create(user)[1],
                        "user":UserDetailsSerilizer(user).data
                    }
                
                    return Response(responseData, status=201)
            

                return Response(meterSerializer.errors, status=400)
            
            return Response(profileSerializer.errors, status=400)
        return Response(userSerializer.errors, status=400)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        user = authenticate(username = request.data['email'], password = request.data['password'])
        if user is not None:
            profile = UserProfile.objects.filter(user = user).first()
            mtrNumber = UserMeterNumber.objects.filter(user=profile, flag=1).first()
            responseData = {
                "token": AuthToken.objects.create(user)[1],
                "user":UserDetailsSerilizer(user).data,
                'mtrNumber': mtrNumber.meterNumber,
            }
            return Response(responseData, status=200)
        return Response({'Msg': 'Invlid Details'}, status=401)


class DataToday(APIView):
    def get(self, request, userEmail, meterNumber, *args, **kwargs):
        today = date.today()
        print(today.weekday)
        print("Today is: ", today)


        userProfile = UserProfile.objects.filter(user__username = userEmail).first()

        #create todays data
        # today_new = MeterData(day = today, user = userProfile)
        # today_new.save()
        # userTodayData = MeterData.objects.filter(day = today, user = userProfile).first()
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

        current_hour = datetime.datetime.now().hour

        userProfile = UserProfile.objects.filter(user__username = userEmail).first()
        # userDayData = MeterData(day = before_yesterday, user = userProfile)
        # userDayData.save()

        #regenerate 2 days ago data.
        # day_before_2_days_ago = before_yesterday - timedelta(days = 1)
        # day_before_2_days_ago_reading = MeterData.objects.filter(user = userProfile, day = day_before_2_days_ago).first().hour_24
        
        # before_yesterday_data = MeterData.objects.filter(day = before_yesterday, user = userProfile).first()
        # current_value = float(day_before_2_days_ago_reading)
        # for j in range(1, 25):
        #     print(current_value)
        #     add = round(random.uniform(0, 0.3), 2)
        #     current_value += add
        #     print(current_value)
        #     before_yesterday_data.__dict__['hour_'+str(j)] = current_value
        # before_yesterday_data.save()
        meter = UserMeterNumber.objects.filter(user = userProfile, meterNumber=meterNumber).first()
        yesterday_reading = MeterData.objects.filter(meter=meter, day = yesterday).first().hour_24
        before_yesterday_reading = MeterData.objects.filter(meter=meter, day = before_yesterday).first().hour_24
        today_reading = MeterData.objects.filter(meter=meter, day = today).first()

        print(today_reading)
        print(yesterday_reading)

        today_data = []
        for i in range(1, current_hour+1):
            if i == 1:
                today_data.append(round(float(today_reading.__dict__['hour_'+str(i)]) - float(yesterday_reading), 2))
            else:

                today_data.append(round(float(today_reading.__dict__['hour_'+str(i)]) - float(today_reading.__dict__['hour_'+str(i-1)]), 2))
        
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
        meterNumber = request.data['mtrNo']
        meter = UserMeterNumber.objects.filter(meterNumber = meterNumber, flag=1).first()
        if meter is None:
            return Response({'Msg': 'Meter Not Found'}, status=404)
        timeNow = datetime.datetime.now()
        current_hour = timeNow.hour
        mtr_data = MeterData.objects.filter(meter=meter, day = date.today()).first()

        if mtr_data.__dict__[f'hour_{current_hour}'] != 0:
            mtr_data.__dict__[f'hour_{current_hour}'] = float(mtr_data.__dict__[f'hour_{current_hour}']) + 0.01
        else:
            lastUpdate = mtr_data.lastUpdate
            for i in range(lastUpdate.hour + 1, timeNow.hour+1):
                mtr_data.__dict__[f'hour_{i}'] = mtr_data.__dict__[f'hour_ {lastUpdate.hour}']
            
            mtr_data.__dict__[f'hour_{timeNow.hour}'] =  float(mtr_data.__dict__[f'hour_{timeNow.hour}']) + 0.01
        mtr_data.save()

        #connect to the websocket

        return Response({'Msg': 'Success'}, status=201)
    # def get(self, request, *args, **kwargs):
    #     print(request.data)
    #     return Response({'Msg':'success'}, status=200)

class DashboardView(APIView):
    def get(self, request, meterNumber, userEmail, *args, **kwargs):
        user = UserProfile.objects.filter(user__username = userEmail).first()
        meter = UserMeterNumber.objects.filter(meterNumber=meterNumber, user=user).first()
        meterReadings = MeterData.objects.filter(meter = meter, day=date.today()).first()
        hour  = datetime.datetime.now().hour
        
        data = {
            'currentReading': meterReadings.__dict__[f'hour_{hour}'],
            # 'user': user.user.username,
            # 'meter': meter.meterNumber,
            # 'hour': hour,
        }

        return Response({'data': data}, status=200)
class WeeksData(APIView):
    def get(self, request, userEmail, meterNumber, *args, **kwargs):
        #get current hour reading
        today = date.today()
        current_hour = datetime.datetime.today().hour

        userProfile = UserProfile.objects.filter(user__username = userEmail).first()
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
        userProfile = UserProfile.objects.filter(user__username = userEmail).first()
        meter = UserMeterNumber.objects.filter(user = userProfile, meterNumber=meterNumber).first()
        count = 1
        this_week_data = []

        while (count <= day_difference):
            current_day = last_day_last_week + timedelta(days = count)
            previous_day = current_day - timedelta(days = 1)

            previous_day_reading = MeterData.objects.filter(meter=meter, day = previous_day).first().hour_24

            if count == day_difference:
                current_hour = datetime.datetime.today().hour
                current_day_reading = MeterData.objects.filter(meter=meter, day = current_day).first().__dict__['hour_'+str(current_hour)]
            else:
                 current_day_reading = MeterData.objects.filter(meter=meter, day = current_day).first().hour_24
            
            this_week_data.append(current_day_reading - previous_day_reading)
            count += 1
        
        #differences
        last_week_reading = MeterData.objects.filter(meter=meter, day = last_day_last_week).first().hour_24
        print('last week reading', last_week_reading)
        amount_this_week = current_day_reading - last_week_reading
        amount_last_week = last_week_reading - MeterData.objects.filter(meter=meter, day = last_day_two_week).first().hour_24


        data = {
            'week_data': this_week_data,
            'amount_last_week': amount_last_week,
            'amount_this_week': amount_this_week
        }
        
        return Response({'data': data}, status=200)

class MonthlyData(APIView):
    def get(self, request, userEmail, meterNumber, *args, **kwargs):
        today = date.today()
        now = datetime.datetime.now()
        current_hour = now.hour
        current_month = now.month
        userProfile = UserProfile.objects.filter(user__username = userEmail).first()
        meter = UserMeterNumber.objects.filter(user=userProfile, meterNumber=meterNumber).first()
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
                last_reading_last_month = MeterData.objects.filter(day=first_day_jan, meter=meter).first().hour_1
            else:
                 last_reading_last_month = MeterData.objects.filter(day=last_month_last_day, meter=meter).first().hour_24
            
            if i+1 == current_month:
                last_reading_current_month = MeterData.objects.filter(day=today, meter=meter).first().__dict__['hour_'+str(current_hour)]
            else:
                last_reading_current_month = MeterData.objects.filter(day=current_month_last_day, meter=meter).first().hour_24
           

            amount_spent = last_reading_current_month - last_reading_last_month

            months_data.append(amount_spent)
        
        #expenditure between last month and this month
        if current_month == 1:
            last_month_expenditure = 0
        else:
            last_month_last_day = date(today.year, current_month-1, months[current_month-2])
            last_2_months_last_day = date(today.year, current_month-2, 1)
            reading_last_day_of_1_month_ago = MeterData.objects.filter(day=last_month_last_day, meter=meter).first().hour_24
            reading_last_day_of_2_months_ago = MeterData.objects.filter(day=last_2_months_last_day, meter=meter).first().hour_24

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
        #     userDayData = MeterData.objects.filter(day = current_day, user = userProfile).first()
        #     # userDayData.save()            
            
        #     # for j in range(1, 25):
        #     #     print(current_value)
        #     #     add = round(random.uniform(0, 0.3), 2)
        #     #     current_value += add
        #     #     print(current_value)
        #     #     userDayData.__dict__['hour_'+str(j)] = current_value
        #     #     userDayData.save()
            
        #     current_day_data = DayDataSerializer(MeterData.objects.filter(user = userProfile, day = current_day).first()).data
        #     data[i] = current_day_data

        # create dummy data for the whole of this year
        first_day_of_the_year = date(2023, 1, 1)
        current_reading = 20
        for i in range(365):
            current_day = first_day_of_the_year + timedelta(days=i)
            mtrNumber = '1234567891'
            mtr = UserMeterNumber.objects.filter(meterNumber=mtrNumber).first()
            new_data = MeterData(day = current_day, meter=mtr)
            for k in range(1, 25):
                print(current_reading)
                new_data.__dict__['hour_'+str(k)] = current_reading
                add = round(random.uniform(0, 0.3), 2)
                current_reading += add
                new_data.save()
        
        return Response({'Msg': 'success'}, status=200)
