from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
import random
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
import stripe
from django.conf import settings 

# Create your views here.

def index(request):
    return render(request,'index.html')


def home(request):
    return render(request,'home.html')

def user_register(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        phone_number=request.POST['phone_number']
        gender=request.POST['gender']
        address=request.POST['address']

        if password!=confirm_password:
            messages.error(request,"Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already exists")
            return redirect('register')

        user=User.objects.create_user(username=username,email=email,password=password)
        User_details.objects.create(user_id=user,phone_number=phone_number,gender=gender,address=address)

        messages.success(request,"Registration successfull! Please login")
        return redirect('login')
    
    return render(request,'register.html')


def user_login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)

        admin_user=authenticate(request,username=username,password=password)

        if admin_user is not None and admin_user.is_staff:
            login(request,admin_user)
            return redirect('admin_dash')

        if user is not None:
            login(request,user)
            messages.success(request,"Login successfull")
            return redirect('home')
        else:
            messages.error(request,"Invalid username or password")
            return redirect('login')
    
    return render(request,'login.html')


def user_logout(request):
    logout(request)
    messages.success(request,"You have successfully logged out")
    return redirect('login')

@login_required(login_url='login')
def user_profile(request):
    if not request.user.is_authenticated:
        messages.error(request,"You must login to view your profile.")
        return redirect('login')
    
    user_details=User_details.objects.get(user_id=request.user)
    return render(request,'profile.html',{'user_details':user_details})

@login_required(login_url='login')
def update_profile(request):
    if not request.user.is_authenticated:
        messages.error(request,"you must login to your profile")
        return redirect('login')
    
    user_details=User_details.objects.get(user_id=request.user)

    if request.method == 'POST':
        user_details.phone_number=request.POST['phone_number']
        user_details.gender=request.POST['gender']
        user_details.address=request.POST['address']
        user_details.save()

        request.user.email=request.POST['email']
        request.user.save()

        messages.success(request,"Profile updated successfully")
        return redirect('profile')
    
    return render(request,'update_profile.html',{'user_details':user_details})


#------admin--------
@login_required(login_url='login')
def admin_dash(request):
    return render(request,'admin_dash.html')

@login_required(login_url='login')
def view_users(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('admin_dash')
    
    users=User_details.objects.all()
    return render(request,'view_users.html',{'users':users})

@login_required(login_url='login')
def hall_details(request):
    halls=Halls.objects.all()
    return render(request,'hall_details.html',{'halls':halls})

@login_required(login_url='login')
def add_hall(request):
    if not request.user.is_staff:
        messages.error(request,"You are not authorized to perform this action.")
        return redirect('admin_dash')

    if request.method == 'POST':
        name=request.POST['name']
        location=request.POST['location']
        capacity=request.POST['capacity']
        price_per_day=request.POST['price_per_day']
        description=request.POST.get('description', '')
        photo=request.FILES.get('photo',None)

        if not photo:
            messages.error(request, "Please upload a hall photo.")
            return redirect('add_hall')

        obj=Halls.objects.create(name=name,location=location,capacity=capacity,price_per_day=price_per_day,description=description,photo_url=photo,)
        obj.save()
        messages.success(request,"Hall added successfully!")
        return redirect('hall_details')
    
    return render(request,'add_hall.html')


@login_required(login_url='login')
def update_hall(request, hall_id):
    hall = get_object_or_404(Halls, id=hall_id)

    if not request.user.is_staff:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('hall_details')

    if request.method == 'POST':
        hall.name = request.POST['name']
        hall.location = request.POST['location']
        hall.capacity = request.POST['capacity']                                    #extra added
        hall.price_per_day = request.POST['price_per_day']
        hall.description = request.POST.get('description', '')

        if 'photo' in request.FILES:
            hall.photo_url = request.FILES['photo']

        hall.save()
        messages.success(request, "Hall updated successfully!")
        return redirect('hall_details')

    return render(request, 'update_hall.html', {'hall': hall})

@login_required(login_url='login')
def hall_detail_view(request, hall_id):
    hall = get_object_or_404(Halls, id=hall_id)
    return render(request, 'view_hall_detail.html', {'hall': hall})

@login_required(login_url='login')
def delete_hall(request, hall_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('hall_details')

    hall = get_object_or_404(Halls, id=hall_id)
    hall.delete()  # This deletes the hall and all its related data.
    
    messages.success(request, "Hall deleted successfully!")
    return redirect('hall_details')

#above code is full hall related


@login_required(login_url='login')
def food_details(request):
    foods=Food.objects.all()
    return render(request,'food_details.html',{'foods':foods})

@login_required(login_url='login')
def add_food(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('admin_dash')

    if request.method == 'POST':
        food_name=request.POST['food_name']
        food_price=request.POST['food_price']
        food_image=request.FILES['food_image']

        obj=Food.objects.create( food_name=food_name,food_price=food_price,food_image=food_image)
        obj.save()
        messages.success(request,"Food item added successfully!")
        return redirect('food_details')
    
    return render(request,'add_food.html')


@login_required(login_url='login')
def update_food(request, food_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('admin_dash')

    food = get_object_or_404(Food, id=food_id)

    if request.method == 'POST':
        food.food_name = request.POST['food_name']
        food.food_price = request.POST['food_price']
        if 'food_image' in request.FILES:
            food.food_image = request.FILES['food_image']
        food.save()
        messages.success(request, "Food item updated successfully!")
        return redirect('food_details')

    return render(request, 'update_food.html', {'food': food})

#above code is related to food

#----passwords-----
def send_otp(email):
    otp = random.randint(100000, 999999)
    print(otp)
    send_mail(
        'Your OTP Code',
        f'Your OTP code is: {otp}',
        'siansarjith@gmail.com',
        [email],
        fail_silently=False,
    )
    return otp

def password_reset_request(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        try:
            user = User.objects.get(email=email)
            otp = send_otp(email)
            context = {
                "email": email,
                "otp": otp,
                "message": "OTP has been sent to your email."
            }
            return render(request, 'forgot_password2.html', context)
        except User.DoesNotExist:
            context["error"] = "Email address not found."
    return render(request, 'forgot_password1.html', context)

def verify_otp(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        otpold = request.POST.get('otp1')
        otp = request.POST.get('otp2')

        if otpold == otp:
            context = {
                'otp': otp,
                'email': email,
                "message": "OTP verified successfully."
            }
            return render(request, 'forgot_password3.html', context)
        else:
            context = {
                "email": email,
                "error": "Invalid OTP. Please try again."
            }
    return render(request, 'forgot_password2.html', context)

def set_new_password(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if new_password == confirm_password:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                context["success"] = "Password has been reset successfully. Please log in."
                return redirect(user_profile)
            except User.DoesNotExist:
                context["error"] = "User does not exist."
        else:
            context = {
                "email": email,
                "error": "Passwords do not match. Please try again."
            }
    context["email"] = email
    return render(request, 'forgot_password3.html', context)


#----decorations----
@login_required(login_url='login')
def decoration_details(request):
    decorations=Decoration.objects.all()
    return render(request,'decoration_details.html',{'decorations':decorations})

@login_required(login_url='login')
def add_decoration(request):
    if not request.user.is_staff:
        messages.error(request,"You are not authorized to perform this action.")
        return redirect('admin_dash')
    
    if request.method == 'POST':
        decoration_name=request.POST['decoration_name']
        decoration_price=request.POST['decoration_price']
        decoration_image=request.FILES['decoration_image']

        obj=Decoration.objects.create(decoration_name=decoration_name,decoration_price=decoration_price,decoration_image=decoration_image)
        obj.save()
        messages.success(request,"Decoration added successfully!")
        return redirect('decoration_details')
    
    return render(request,'add_decoration.html')


@login_required(login_url='login')
def update_decoration(request, id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('admin_dash')
    
    decoration = get_object_or_404(Decoration, id=id)

    if request.method == 'POST':
        decoration.decoration_name = request.POST['decoration_name']
        decoration.decoration_price = request.POST['decoration_price']

        if 'decoration_image' in request.FILES:
            decoration.decoration_image = request.FILES['decoration_image']
        
        decoration.save()
        messages.success(request, "Decoration updated successfully!")
        return redirect('decoration_details')

    return render(request, 'update_decoration.html', {'decoration': decoration})


@login_required(login_url='login')
def delete_decoration(request, id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('admin_dash')

    decoration = get_object_or_404(Decoration, id=id)
    decoration.delete()
    messages.success(request, "Decoration deleted successfully!")
    return redirect('decoration_details')


#above code is decoration related

@login_required(login_url='login')
def admin_view_booking(request):
    book = Bookings.objects.select_related('user_id', 'hall_id', 'food', 'decoration').all().order_by('-booking_date')
    return render(request, 'admin_view_booking.html', {'data': book})


@login_required(login_url='login')
def accept_reject_booking(request,id):
    data=Bookings.objects.get(id=id)
    if request.method == 'POST':
        value=request.POST.get('Status')
        if value == 'Accept':
            data.event_status='Accept'
        elif value == 'Reject':
            data.event_status='Reject'
        data.save()
        return redirect(admin_view_booking)
    return redirect(admin_view_booking)

@login_required(login_url='login')
def booking_detail(request, id):
    booking = get_object_or_404(Bookings.objects.select_related('user_id', 'hall_id', 'food', 'decoration'), id=id)
    return render(request, 'booking_detail_.html', {'booking': booking})



#----Booking---

@login_required(login_url='login')
def booking_page(request):
    halls=Halls.objects.all()
    foods=Food.objects.all()
    decorations=Decoration.objects.all()
    photography_price=5000

    if request.method == 'POST':
        event_date=request.POST['event_date']
        hall_id=request.POST['hall']
        food_id=request.POST.get('food')                #paranthesis bcz it's optional
        decoration_id=request.POST.get('decoration')
        photography=request.POST.get('photography')
        no_of_persons=int(request.POST['no_of_persons'])

        hall=Halls.objects.get(id=hall_id)
        food=Food.objects.get(id=food_id)if food_id else None                           #fetch hall,food and decoration object
        decoration=Decoration.objects.get(id=decoration_id)if decoration_id else None

        total_cost=0
        total_cost=hall.price_per_day
        if food:
            total_cost +=food.food_price*no_of_persons

        if decoration:                                                      #Calculation of total price
            total_cost +=decoration.decoration_price*no_of_persons
        
        if photography=='yes':
            total_cost +=photography_price

        booking=Bookings.objects.create(event_date=event_date,user_id=request.user,hall_id=hall,food=food,
            decoration=decoration,
            photography_cost=photography_price if photography == 'yes' else 0,
            no_of_persons=no_of_persons,
            total_payment=total_cost,
            payment_status="pending",
        )

        booking.save()
        return redirect('booking_view')
    
    context = {'halls':halls,'foods':foods,'decorations':decorations,'photography_price':photography_price}
    return render(request,'booking_page.html',context)


@login_required(login_url='login')
def booking_view(request):
    booking = Bookings.objects.filter(user_id=request.user).order_by('-id').first()
    
    if not booking:
        messages.error(request, "No booking found.")
        return redirect('booking_page')

    context = {
        'booking': booking
    }
    return render(request, 'booking_view.html', context)

@login_required(login_url='login')
def view_bookings(request):
    user=User.objects.get(id=request.user.id)
    bookings = Bookings.objects.filter(user_id=user)            # Fetch bookings for the logged-in user
    return render(request,'view_bookings.html',{'bookings':bookings})

#---payment----

stripe.api_key = settings.STRIPE_SECRET_KEY

def stripe_payments(request,id):
    try:
        data=Bookings.objects.get(id=id)
        total_amount = data.total_payment

        intent = stripe.PaymentIntent.create(
            amount=int(total_amount*100),
            currency="usd",
            metadata={"data":data.id,"user_id":request.user.id},

        )
        context = {
            'client_secret': intent.client_secret,
            'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
            'total_amount':total_amount,
            'data':data,
        }
        return render(request,'stripe_payments.html',context)
    except Bookings.DoesNotExist:
        return redirect(booking_view)
    

def payment_status(request, id):
    data=get_object_or_404(Bookings,id=id) 
    data.payment_status="Completed"
    data.save()
    return redirect('view_bookings') 



#navbar
@login_required(login_url='login')
def service(request):
    return render(request,'service.html')

@login_required(login_url='login')
def aboutus(request):
    return render(request,'aboutus.html')

@login_required(login_url='login')
def gallery(request):
    return render(request,'gallery.html')

@login_required(login_url='login')
def testimonial(request):
    return render(request,'testimonial.html')










