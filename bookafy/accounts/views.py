from django.contrib.auth import login,authenticate ,update_session_auth_hash , logout
from django.utils.decorators import method_decorator
from django.shortcuts import redirect ,render,HttpResponseRedirect
from accounts.models import User, SMSActivation
from accounts.forms import SignUpForm, LoginForm, PasswordChangeCustomForm , UserUpdateForm
from django.views.generic import (View,ListView, CreateView, UpdateView, TemplateView)
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from userprofiles.forms import UserProfileForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import RedirectView


   
 
class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name= 'customer_signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userprofile_form'] = UserProfileForm()
        return context

    def dispatch(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                return redirect('home')
        except :
           pass
        return super().dispatch(request, *args, **kwargs)
  

    def form_valid(self, form):
        userprofile_form = UserProfileForm(self.request.POST)
        if userprofile_form.is_valid():
            self.object = form.save()
            userprofile = userprofile_form.save(commit=False)
            userprofile.user = self.object
            userprofile.save()
            user = form.save()
            self.request.session['username_or_email'] = user.email
            return redirect('cverify')
        else:
            context = self.get_context_data(form=form)
            context['userprofile_form'] = userprofile_form
            return render(self.request, self.template_name, context)
        



def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = LoginForm(request.POST or None)
        valuenext= request.POST.get('next')
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username_or_email, password=password)
            if user is not None:
                request.session['username_or_email'] = username_or_email
                try:
                    obj = SMSActivation.objects.get(user=user, activated=True)
                    login(request, user)
                    del request.session['username_or_email']
                    if valuenext:
                        return HttpResponseRedirect(valuenext)
                    return redirect('home')
                    
                except SMSActivation.DoesNotExist :
                    qs , qsCreated = SMSActivation.objects.get_or_create(phone=user.phone,email=user.email,user=user)
                    qs.regenerate()
                    qs.send_activation()
                    messages.warning(request, "Verify Your Mobile Number.")
                    return redirect('cverify')

        return render(request, 'customer_login.html',  {'form': form })



class CustomerInfo(ListView):
    model = User
    template_name = "customerinfo.html"



def user_logout(request):
    logout(request)
    return redirect('user_login')

 
@login_required(login_url='/login/')
def user_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your personal information has been updated!')
            return redirect('customerinfo')
    else: 
        form = UserUpdateForm(instance=request.user)
        context = {
            'form': form,
        } 
        return render(request, 'user_update.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('customerinfo')
    else:
        form = PasswordChangeCustomForm(request.user)
    return render(request, 'change_password.html', {'form': form })


def customer_verify(request):
    username_or_email = request.session.get('username_or_email')
    if username_or_email == None:
        return redirect('home')
    else:
        if request.method == "POST":
            code = request.POST["code"]
            try:
                qs = SMSActivation.objects.get(Q(email=username_or_email)|Q(phone=username_or_email),code=code)
                qs.activate()
                qs.send_reset()
                user = qs.user
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect('home')
            except:
                messages.warning(request, "Invalid Verification Code")
                return redirect('cverify')
        else:
            username_or_email = request.session.get('username_or_email')
            context = {'username_or_email': username_or_email}
            return render(request, "verify.html",context)



def resend(request):
    url = request.META.get('HTTP_REFERER')
    phone = request.session.get('phone')
    try:
        obj = SMSActivation.objects.get(phone=phone)

        if obj.resend < 10 :
            obj.regenerate()
            obj.send_activation()
            messages.success(request, "Verification Code Send. Check Your Phone.")
        else:
            messages.warning(request, "Please contact customer care to activate your account.")
    except:
        pass
    return HttpResponseRedirect(url)




# def custom_password_reset(request):
#     if request.method == "POST":
#         mobile = request.POST['mobile']
#         try:
#             phone = SMSActivation.objects.get(phone=mobile)
#             phone.regenerate() 
#             request.session['phone'] = mobile
#             messages.success(request, 'Please verify your phone number.')
#             return redirect('reset_password_verify')
#         except:
#            messages.warning(request, "We cannot find an account with that mobile number.")
#            return redirect('custom_password_reset')
#     return render(request, 'registration/password_reset_form.html')


#Reset Password

def custom_password_reset(request):
    if request.method == "POST":
        username_or_phone = request.POST['username_or_phone']
        try:
            phone = SMSActivation.objects.get(Q(phone=username_or_phone)|Q(email=username_or_phone))
            phone.regenerate() 
            request.session['username_or_phone'] = username_or_phone
            return redirect('reset_password_verify')
        except:
           messages.warning(request, "We cannot find an account with that mobile number.")
           return redirect('custom_password_reset')
    return render(request, 'registration/password_reset_form.html')




def reset_password_verify(request):
    username_or_phone = request.session.get('username_or_phone')
    if request.method == "POST":
        code = request.POST["code"]
        try:
            qs = SMSActivation.objects.get(Q(phone=username_or_phone)|Q(email=username_or_phone),code=code)
            qs.send_reset()
            user = qs.user
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            return redirect('password_reset_confirm', uidb64=uid ,token=token)
        except:
           messages.warning(request, "Invalid Verification Code")
           return redirect('reset_password_verify')
    else:
        username_or_email = request.session.get('username_or_phone')
        context = {'username_or_email': username_or_email}
        return render(request, "verify.html",context)


class PasswordResetCompleteView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse_lazy('home')
        else:
            return reverse_lazy('user_login')