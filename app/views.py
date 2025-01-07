from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory,CheckboxInput,FileInput
from django.contrib import messages
from django.core.files import File
from django.db.models import Q
from io import BytesIO
from django.core.mail import send_mail
from datetime import datetime,timedelta,date
import razorpay
import qrcode
import uuid
from .models import *
from .forms import *
# Create your views here.
@login_required
def home(r):
    slides=Slider.objects.order_by('-id')
    categories=Category.objects.all()
    products=""
    if Profile.objects.filter(user=r.user).exists():
        products=Post.objects.exclude(user=r.user).filter(location__icontains=Profile.objects.get(user=r.user).city)
    else:
        messages.error(r,'Please fill your profile first')
        return redirect('/accounts/profile')
    return render(r,'index.html',{"slides":slides,"products":products,"categories":categories})
@login_required
def search(r):
    if not Profile.objects.filter(user=r.user).exists():
        messages.error(r,'Please fill your profile first')
        return redirect('/accounts/profile')
    query = r.GET.get('query', '').strip()
    category = r.GET.get('category', '').strip()
    price = r.GET.get('price', '').strip()
    location = r.GET.get('location', '').strip()
    gender = r.GET.get('gender', '').strip()
    categories = Category.objects.all()
    pd = Post.objects.exclude(user=r.user)
    if query:
        pd = pd.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category and category.lower()!="all categories":
        pd = pd.filter(category__name__iexact=category)
    if gender and gender.lower()!="all genders":
        pd = pd.filter(gender__icontains=gender)
    if price:
        try:
            price_range = price.split('-')
            if len(price_range) == 2:
                min_price = float(price_range[0])
                max_price = float(price_range[1])
                pd = pd.filter(price__gte=min_price, price__lte=max_price)
            elif len(price_range) == 1:
                pd = pd.filter(price__lte=float(price_range[0]))
        except ValueError:
            pass 
    if location:
        pd = pd.filter(location__icontains=location)
    return render(r, 'search.html', {"data": pd,"category": categories,"query": query,"selected_category": category,"price": price,"location": location,"selected_gender":gender})
@login_required()
def profile(r):
    form =ProfileForm()
    profile=""
    if Profile.objects.filter(user=r.user).exists():
        profile=Profile.objects.get(user=r.user)
        form = ProfileForm(instance=profile)
    if r.method=='POST':
        form = ProfileForm(r.POST,instance=profile or None,files=r.FILES)
        if form.is_valid():
            k=form.save(commit=False)
            k.user=r.user
            k.save()
            messages.success(r,'Profile Updated Successfully')
            return redirect('/accounts/profile')
    return render(r,'account/profile.html',{"form":form,"profile":profile})
@login_required()
def new_post(request):
    if not Profile.objects.filter(user=request.user).exists():
        messages.error(request,'Please fill your profile first')
        return redirect('/accounts/profile')
    product_form = PostForm(request.POST or None,request.FILES or None)
    images_formset = inlineformset_factory(Post, PostImage, fields=('image',), extra=3,can_delete=True)(request.POST or None,request.FILES or None, instance=Post()) 
    for form in images_formset:
        for field in form.fields.values():
            if isinstance(field.widget, FileInput):
                field.widget.attrs.update({'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'})
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs.update({'class': 'w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800'})
    if request.method == 'POST':
        if product_form.is_valid() and images_formset.is_valid():
            p = product_form.save(commit=False)
            p.user = request.user
            p.profile = Profile.objects.get(user=request.user)
            p.save()
            images_formset.instance = p
            images_formset.save()
            messages.success(request,'Post Created Successfully')
            return redirect(f'/post/edit/{p.id}')
        print(product_form.errors)
    return render(request, 'new_post.html', {'form': product_form, 'formset': images_formset})
@login_required
def editpost(request, id):
    if not Profile.objects.filter(user=request.user).exists():
        messages.error(request,'Please fill your profile first')
        return redirect('/accounts/profile')
    p=Post.objects.get(id=id)
    if not p.user==request.user:
        messages.error(request,'You are not the owner of this post')
        return redirect('/post/all')
    product_form = PostForm(request.POST or None,request.FILES or None,instance=p)
    images_formset = inlineformset_factory(Post, PostImage, fields=('image',), extra=3,can_delete=True)(data=request.POST or None,files=request.FILES or None, instance=p) 
    for form in images_formset:
        for field in form.fields.values():
            if isinstance(field.widget, FileInput):
                field.widget.attrs.update({'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'})
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs.update({'class': 'w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800'})
    if request.method == 'POST':
        if product_form.is_valid() and images_formset.is_valid():
            product_form.save()
            images_formset.save()
            messages.success(request,'Post Updated Successfully')
            return redirect(f'/post/edit/{id}')
    return render(request, 'new_post.html', {'form': product_form, 'formset': images_formset,"pid":id})
@login_required
def deletepost(request,id):
    if not Profile.objects.filter(user=request.user).exists():
        messages.error(request,'Please fill your profile first')
        return redirect('/accounts/profile')
    p=Post.objects.get(id=id)
    if p.user==request.user:
        p.delete()
        messages.success(request,'Post Deleted Successfully')
        return redirect('/post/all')
    messages.error(request,'You are not the owner of this post')
    return redirect('/post/all')
@login_required
def user_posts(request):
    if not Profile.objects.filter(user=request.user).exists():
        messages.error(request,'Please fill your profile first')
        return redirect('/accounts/profile')
    posts = Post.objects.filter(user=request.user).order_by("-id")
    return render(request, 'user_posts.html', {'data': posts})
@login_required
def post_reviews(request):
    if not Profile.objects.filter(user=request.user).exists():
        messages.error(request,'Please fill your profile first')
        return redirect('/accounts/profile')
    comments=Comment.objects.filter(post__user=request.user).order_by("-id")
    return render(request, 'user_post_reviews.html', {"data":comments})
@login_required
def profile_reviews(request):
    if not Profile.objects.filter(user=request.user).exists():
        messages.error(request,'Please fill your profile first')
        return redirect('/accounts/profile')
    comments=Review.objects.filter(profile__user=request.user).order_by("-id")
    return render(request, 'user_profile_reviews.html', {"data":comments})
@login_required
def view_post(request,id):
    form=CommentForm()
    posts = Post.objects.get(id=id)
    buy=posts.availability and date.today()<=posts.period and posts.user!=request.user and posts.quantity>0
    m=10 if posts.quantity>10 else posts.quantity
    avail=posts.availability and date.today()<=posts.period
    similar_posts = Post.objects.filter(category=posts.category).exclude(user=request.user).exclude(id=id)
    if request.method == 'POST':
        if request.user==posts.user:
            messages.error(request,'You cannot comment on your own post')
            return redirect(f'/post/view/{id}')
        form = CommentForm(request.POST,request.FILES)
        if form.is_valid():
            pp=form.save(commit=False)
            pp.post=posts
            pp.user=Profile.objects.get(user=request.user)
            pp.empty="*"*(5-len(form.cleaned_data["rating"]))
            pp.save()
    comments=Comment.objects.filter(post=id)
    return render(request, 'post.html', {'data': posts,"buy":buy,"max":m,"available":avail,"similar":similar_posts,"form":form,"comments":comments})


@login_required
def makeorder(r,id,q):
    product=Post.objects.get(id=id)
    form=MakeOrderForm()
    if q>product.quantity or q>10 or q<1:
        messages.error(r,'Quantity is more than available ')
        return redirect(f'/post/view/{product.id}')
    if not product.availability or date.today()>product.period:
        messages.error(r,'Product is not available')
        return redirect(f'/post/view/{product.id}')
    if product.user==r.user:
        messages.error(r,'You can not buy your own product')
        return redirect(f'/post/view/{product.id}')
    client=razorpay.Client(auth=("rzp_test_euB1g3Ioe7wejB","k0phaX9LIQtibmploFiUPjs0"))
    
    if r.method=="POST":
        form=MakeOrderForm(r.POST)
        if form.is_valid():
            start=form.cleaned_data['rent_start']
            end=form.cleaned_data['rent_end']
            if end > product.period:
                form.add_error('rent_end', "Not Available till this date") 
            if form.errors:
                return render(r, 'makeorder.html', {"form": form})
            amount=round((product.price//int(product.rent_method))*(end-start).days)
            payment=client.order.create({"amount":float(amount*q*100+5000),'currency':'INR','payment_capture':1})
            shipping=50 if form.cleaned_data['delivery_type']=="Courier" else 0
            ecom=uuid.uuid4()
            new_order=Order (
                ecommerce_id=ecom,
                order_id=payment['id'],
                delivery_status="Pending",
                user=r.user,
                product=product,
                quantity=q,
                amount=amount,
                subtotal=q * amount,
                shipping=shipping,
                platform_fee=(q*amount*0.05),
                total=(q * amount) +(q*amount*0.05)+ shipping,
                address=form.cleaned_data['address'],
                full_name=form.cleaned_data['full_name'],
                mobile_no=form.cleaned_data['mobile_no'],
                alternate_no=form.cleaned_data['alternate_no'],
                pin_code=form.cleaned_data['pin_code'],
                delivery_type=form.cleaned_data['delivery_type'],
                order_date=datetime.today(),
                delivery_date=datetime.today() + timedelta(days=7),
                rent_start=start,
                rent_end=end
                )
            new_order.save()
            return redirect(f"/order/payment/{new_order.id}")
    return render(r,'makeorder.html',{"form":form})
@login_required
def orderpayment(r,id):
    ord=Order.objects.get(id=id)
    return render(r,'payment.html',{"order":ord})
@login_required
def paysuccess(r,pay,id):
    for i in Order.objects.filter(order_id=id):
        if Post.objects.filter(id=i.product_id):
            pp=Post.objects.get(id=i.product_id)
            pp.quantity=pp.quantity-i.quantity
            pp.save()
            pp=pp.profile
            pp.wallet=pp.wallet+float(i.total)
            pp.save()
        update_order(i.ecommerce_id,pay,True)
    return redirect('/orders')
@login_required
def payfailed(r,pay,id):
    for i in Order.objects.filter(order_id=id):
        update_order(i.ecommerce_id,pay,False)
    return redirect('/orders')

def update_order(id, pay, status):
    try:
        ob = Order.objects.get(ecommerce_id=id)
        ob.payment_id = pay
        ob.order_status = True
        ob.payment_status = status

        # Set delivery status for failed payment
        if not status:
            ob.delivery_status = "Payment Failed"

        # Common email details
        order_summary = f"""
Order ID: {ob.order_id}
Order Date: {ob.order_date.strftime('%d-%b-%Y') if ob.order_date else 'N/A'}
        """+f"Estimated Delivery Date: {ob.delivery_date.strftime('%d-%b-%Y') if ob.delivery_date else 'N/A'}" if ob.delivery_type=="Courier" else ""
        # Return Before: {(ob.delivery_date + timedelta(days=7)).strftime('%d-%b-%Y') if ob.delivery_date else 'N/A'}

        product_summary = f"""
Product Name: {ob.product.title}
Product ID: {ob.product.id}
Price per Unit: ₹{ob.product.price}
Amount per Unit: ₹{ob.amount}
Quantity: {ob.quantity}
Subtotal: ₹{ob.subtotal}
        """

        delivery_summary = f"""
Delivery Type: {ob.delivery_type}
Recipient Name: {ob.full_name}
Mobile Numbers: {ob.mobile_no}, {ob.alternate_no}
Address: {ob.address}
Pin Code: {ob.pin_code}
        """

        payment_summary = f"""
Payment ID: {ob.payment_id if ob.payment_id else 'N/A'}
Payment Status: {"Paid" if ob.payment_status else "Not Paid"}
Shipping Charges: ₹{ob.shipping}
Plaform Fee: ₹{ob.platform_fee}
Total Amount: ₹{ob.total}
        """

        # Subject lines based on delivery status
        delivery_status = ob.delivery_status
        buyer_subject = f"Order {delivery_status} - Wardrobe Share"
        seller_subject = f"New Order Notification - Order {delivery_status}"

        # Buyer email body
        buyer_body = f"""
Dear {ob.user.username},

Your order with Wardrobe Share is currently {delivery_status}. Below are your order details:

Order Summary:
{order_summary}

Product Details:
{product_summary}

User Details:
{delivery_summary}

Payment Summary:
{payment_summary}

Thank you for shopping with Wardrobe Share. If you have any questions, feel free to contact us at support@wardrobeshare.com.

Warm regards,
Wardrobe Share Team
        """

        # Seller email body
        seller_body = f"""
Dear {ob.product.user.username},

A new order has been placed for your product. Below are the details:

Order Summary:
{order_summary}

Buyer Information:
Buyer Name: {ob.user.username}
Buyer Email: {ob.user.email}
{delivery_summary}

Product Details:
{product_summary}

Payment Summary:
{payment_summary}

Please prepare the product for delivery promptly. If you have any questions, feel free to contact us at support@wardrobeshare.com.

Best regards,
Wardrobe Share Team
        """

        # Adjust for payment failure
        if not status:
            buyer_subject = "Order Payment Failed - Wardrobe Share"
            buyer_body = f"""
Dear {ob.user.username},

Unfortunately, the payment for your order could not be processed. Below are the details of your order:

Order Summary:
{order_summary}

Please try placing the order again or contact us at support@wardrobeshare.com for assistance.

Warm regards,
Wardrobe Share Team
            """
            seller_body = None  # No email to seller for failed payment

        # Send emails
        send_mail(buyer_subject, buyer_body, "no-reply@wardrobeshare.com", [ob.user.email])
        if seller_body:
            send_mail(seller_subject, seller_body, "no-reply@wardrobeshare.com", [ob.product.user.email])

        # Generate QR code for order details
        qr_data = f"""
Order Details:
{order_summary}

Product Details:
{product_summary}

Delivery Details:
{delivery_summary}

Payment Summary:
{payment_summary}
        """
        qr = qrcode.make(qr_data)
        stream = BytesIO()
        qr.save(stream, 'PNG')
        ob.qrcode.save('qrcode.png', File(stream))

        ob.save()

    except Order.DoesNotExist:
        print(f"Order with ecommerce_id {id} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

#orders
@login_required
def orders(r):
    ord = Order.objects.filter(user=r.user, order_status=True).order_by("-id")  # Corrected filter chain

    # Loop through the orders queryset
    for order in ord:  # Use `ord` here instead of `orders`
        if order.rent_end and order.rent_start:
            order.rent_duration = order.rent_end - order.rent_start
        else:
            order.rent_duration = timedelta(days=0)

    return render(r, 'orders.html', {"orders": ord})

@login_required
def orderdetails(r,id):
    i=Order.objects.get(ecommerce_id=id)
    returndate=i.delivery_date+timedelta(days=7)
    pending=0
    confirmed=0
    cancelled=0
    shipping=0
    shipped=0
    outfordelivery=0
    delivered=0
    returned=0
    refunded=0
    refundcancel=0
    cancel=0
    refund=0
    if i.delivery_status=="Pending":
        pending=1
    elif i.delivery_status=="Confirmed":
        confirmed=1
    elif i.delivery_status=="Cancelled":
        cancelled=1
    elif i.delivery_status=="Shipping":
        shipping=1
    elif i.delivery_status=="Shipped":
        shipped=1
    elif i.delivery_status=="Out for Delivery":
        outfordelivery=1
    elif i.delivery_status=="Delivered":
        delivered=1
    elif i.delivery_status=="Returned":
        returned=1
    elif i.delivery_status=="Refunded":
        refunded=1
    elif i.delivery_status=="Refund Cancel":
        refundcancel=1
    if pending or confirmed or shipped or shipping or outfordelivery:
        cancel=1
    if delivered and datetime.now().date()<=returndate:
        refund=1
    context={
        "i":i,
        "pending":pending,
        "returndate":returndate,
        "confirmed":confirmed,
        "cancelled":cancelled,
        "shipping":shipping,
        "shipped":shipped,
        "outfordelivery":outfordelivery,
        "returned":returned,
        "refunded":refunded,
        "refundcancel":refundcancel,
        "delivered":delivered,
        "cancel":cancel,
        "refund":refund
    }
    

    return render(r,'orderdetails.html',context)
@login_required
def cancelorder(r,id):
    o=Order.objects.get(id=id)
    o.delivery_status="Cancelled"
    o.save()
    return redirect(f'/order/{o.ecommerce_id}')
@login_required
def returnorder(r,id):
    o=Order.objects.get(id=id)
    o.delivery_status="Returned"
    o.save()
    return redirect(f'/order/{o.ecommerce_id}')
@login_required
def user_orders(r):
    if not Profile.objects.filter(user=r.user).exists():
        messages.error(r,'Please fill your profile first')
        return redirect('/accounts/profile')
    order=Order.objects.filter(order_status=True,product__user=r.user).order_by("-id")
    return render(r,'user_orders.html',{"data":order})
@login_required
def post_profile(request,id):
    profile=Profile.objects.get(id=id)
    order=Post.objects.filter(user=profile.user)
    reviews=Review.objects.filter(profile=profile)
    form=ReviewForm()
    if request.method == 'POST':
        if request.user==profile.user:
            messages.error(request,'You cannot comment on your own profile')
            return redirect(f'/post/profile/{id}')
        form = ReviewForm(request.POST,request.FILES)
        if form.is_valid():
            pp=form.save(commit=False)
            pp.profile=profile
            pp.user=Profile.objects.get(user=request.user)
            pp.empty="*"*(5-len(form.cleaned_data["rating"]))
            pp.save()
    return render(request,'profile_reviews.html',{"data":order,"reviews":reviews,"profile":profile,"form":form})
@login_required
def user_orders_confirm(r,id):
    order=Order.objects.get(id=id)
    if  order.product.user==r.user:
        order.delivery_status="Confirmed"
        order.save()
        update_order(order.ecommerce_id,order.payment_id,order.payment_status)
        messages.success(r,'Order has been confirmed')
        return redirect('/post/orders')
    return redirect('/post/orders')
@login_required
def user_orders_cancel(r,id):
    order=Order.objects.get(id=id)
    if  order.delivery_status=="Pending" and order.product.user==r.user:
        order.delivery_status="Cancelled"
        order.save()
        update_order(order.ecommerce_id,order.payment_id,order.payment_status)
        messages.success(r,'Order has been cancelled')
        return redirect('/post/orders')
    return redirect('/post/orders')

@login_required
def user_orders_update(r,id):
    form=OrderForm()
    order=Order.objects.get(id=id)
    form=OrderForm(instance=order)
    if r.method=="POST":
        form=OrderForm(r.POST,instance=order)
        if form.is_valid():
            form.save()
            update_order(order.ecommerce_id,order.payment_id,order.payment_status)
            return redirect(f'/post/orders')
    return render(r,"user_orders_update.html",{"form":form})