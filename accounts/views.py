from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from .account_forms import UserForm,UserProfileInfoForm
from  accounts.models import UserProfileInfo
from templates.forms import NameForm
from scores.models import Scores
from posts.models import Posts
from cutovers.models import Cutovers
from orders.models import Orders
from bonuses.models import Bonuses
from routine.models import Routine
from faulty.models import Faulty
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import datetime




def register(request):
  if request.method == 'POST':
    # Get form values
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # Check if passwords match
    if password == password2:
      # Check username
      if User.objects.filter(username=username).exists():
        messages.error(request, '已注册')
        return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'email已注册')
          return redirect('register')
        else:
          # Looks good
          user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
          # Login after register
          # auth.login(request, user)
          # messages.success(request, 'You are now logged in')
          # return redirect('index')
          user.save()
          
          userProfile = UserProfileInfo(user_id = user.id, profile_phone='18602038888', profile_pic='profile_pics/selfie.png')
          userProfile.save()

          messages.success(request, '注册成功，请登录')
          return redirect('login')
    else:
      messages.error(request, '密码错误')
      return redirect('register')
  else:
    return render(request, 'accounts/register.html')



def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, '已登录')
      return redirect('dashboard')
    else:
      messages.error(request, '密码错误')
      return redirect('login')
  else:
    return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, '已退出')
        return redirect('login')



def dashboard(request):

    my_forms = {"user_form":0,"profile_form":0}
    #if POST  then update info
    if request.method =='POST':
      isUpdate = updateInfo(request,my_forms)
      user_form = my_forms["user_form"]
      profile_form = my_forms["profile_form"]
      if isUpdate:
        return redirect('login')
      else:
        return redirect('dashboard')

    #not POST, then show personal info    
    else:

      if request.user.is_authenticated:
        id = request.user.id
        #通过django的user找到id，通过id获取附件用户信息的对象profile_form
        user_basic = User.objects.get(id=id)
        user_profile = UserProfileInfo.objects.get(user_id=id)
        #给user_form，profile_form赋值，传回前端，就可以在html上显示出来
        #initial={'password':''} 的意思是初始化为空，当用户更新信息时不显示数据库中存的用户密码
        user_form = UserForm(initial={'password':''},instance=user_basic)
        profile_form = UserProfileInfoForm(instance=user_profile)
        
        #get all types of work info
        myName = str(user_basic.last_name+user_basic.first_name)
        print(myName)
        thisYear = datetime.datetime.now().year
        print(thisYear)
        myOrders = Orders.objects.all().filter(pj_leader__contains=myName,created_at__year=2020)
      
        paginator = Paginator(myOrders, 15) # Show 25 contacts per page

        page = request.GET.get('page')
        orderListings = paginator.get_page(page)

        context = {"user_form":user_form,
              "profile_form":profile_form,
              "website":user_profile.profile_site,
              "phone_number":user_profile.profile_phone,
              "selfie":user_profile.profile_pic,
              "description":user_profile.profile_descption,
              "myOrders":orderListings,
              }

        return render(request,'accounts/dashboard.html',context)
      else:
        return redirect('login')




def updateInfo(request,my_form):

    if request.method == 'POST':
        name = request.POST.get('inputUsername')
        
        # 通过名字找到user_id,username是用户表的表头
        #user的id就是扩展个人信息的user_id
        user_basic = User.objects.get(username=name)
        user_id = getattr(user_basic, 'id')

        user_pofile = UserProfileInfo.objects.get(user_id=user_id)
        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        #print(request.FILES['inputProfilePic'])

        #有instance的时候更新信息，没有instance的时候，新增信息
        user_form = UserForm(data=request.POST,instance=user_basic)
        profile_form = UserProfileInfoForm(data=request.POST,instance=user_pofile)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()
            # Hash the password
            user.set_password(user.password)
            # Update with Hashed password
            user.save()
            # Now we deal with the extra info!
            # Can't commit yet because we still need to manipulate
            pf = profile_form.save(commit=False)
            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            pf.user = user
            # Check if they provided a profile picture

           # pf.profile_pic = request.FILES['inputProfilePic']
            if 'inputProfilePic' in request.FILES:
                print('found it!!!!')
                # If yes, then grab it from the POST form reply
                pf.profile_pic = request.FILES['inputProfilePic']

            pf.profile_phone = request.POST.get('inputPhoneNumber')
            pf.profile_site = request.POST.get('inputPersonalWebsite')
            pf.profile_descption= request.POST.get('inputDesciption')
            
            # Now save model
            pf.save()



        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)
            messages.error(request, user_form.errors,profile_form.errors)            
            return False

    else:
        # Was not an HTTP post so we just render the forms as the info we get from db.
        user_form = UserForm(instance = user_basic)
        profile_form = UserProfileInfoForm(instance = user_pofile)

    # give back user_form and profile_form
    my_form['user_form'] = user_form
    my_form['profile_form'] = profile_form



# def dashboard(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return redirect('dashboard')

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()

#     return render(request, 'accounts/dashboard.html', {'form': form})

def printRequest(request):
    print(type(request))   # 打印出request的类型

    print(request.environ)   # 打印出request的header详细信息
    #循环打印出每一个键值对
    for k, v in request.environ.items():
       print(k, v)
