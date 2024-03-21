from django.db import models
from logisticsapp.models import *

# Create your models here.


#for storing the different types of roles
# class UserRoleRef(models.Model):
#     user_role_name = models.CharField(max_length=250, blank=True, null=True)
#     create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp")
#     last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp")

# class City(models.Model):
#     city_name= models.CharField(max_length=250, blank=True, null=True)

#     create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp")
#     last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp")


# class CustomUser(models.Model):

#     first_name = models.CharField(max_length=250, blank=True, null=True)
#     last_name = models.CharField(max_length=250, blank=True, null=True)
#     mobile_number=models.CharField(max_length=150, blank=True, null=True)
#     company_name = models.CharField(max_length=250, blank=True, null=True)
#     email= models.EmailField(max_length=250, blank=True, null=True)
#     alternate_number= models.CharField(max_length=250, blank=True, null=True)
#     zip_code= models.CharField(max_length=250, blank=True, null=True)
#     address= models.CharField(max_length=250, blank=True, null=True)
#     adhar_card= models.CharField(max_length=250, blank=True, null=True)
#     reset_otp = models.CharField(max_length=100, null=True, blank=True)
#     profile_image_path=models.TextField(blank=True, null=True)
#     base64=  models.TextField(blank=True, null=True)

#     profile_image = models.FileField(null=True, blank=True)

#     adhar_card_front_side_img= models.TextField(blank=True, null=True)
#     adhar_card_front_side_img_path= models.FileField(null=True, blank=True)
#     # adhar_card_front_side_mandatory=models.BooleanField(default=True)
    
#     adhar_card_back_side_img= models.TextField(blank=True, null=True)
#     adhar_card_back_side_img_path= models.FileField(null=True, blank=True)
#     # adhar_card_back_side_img_mandatory=models.BooleanField(default=True)

#     pan_card= models.CharField(max_length=250, blank=True, null=True)
#     pan_image_path=models.TextField(blank=True, null=True)
#     pan_card_base64=  models.TextField(blank=True, null=True)

#     create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
#     last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)

#     whatsup_number  = models.CharField(max_length=100, null=True, blank=True)

#     # user  = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     role= models.ForeignKey(UserRoleRef, on_delete=models.CASCADE, blank=True, null=True, related_name="account_role")
#     city= models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True, related_name="account_city")

#     # driver= models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, null=True)
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True, related_name="account_vehicle")

# class Driver(models.Model):

#     user  = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name="account_user")
#     account  = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name="account_account")
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True, related_name='account_vehicle')
#     owner_id= models.CharField(max_length=250, blank=True, null=True)
#     subcription = models.ForeignKey(Subscription, on_delete=models.CASCADE, blank=True, null=True)
#     account  = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
#     notification_history  = models.CharField(max_length=3000, blank=True, null=True)

#     driver_driving_license= models.CharField(max_length=250, blank=True, null=True)
    
#     badge= models.CharField(max_length=250, blank=True, null=True)
#     driving_license_image_path = models.CharField(max_length=250, blank=True, null=True)
#     # base64=  models.TextField(max_length=50000, blank=True, null=True)

#     # license_status= models.CharField(max_length=100, blank=True, null=True)

#     validity_start_date_time= models.CharField(max_length=250, blank=True, null=True)
#     validity_end_date_time = models.CharField(max_length=250, blank=True, null=True)
#     driver_status = models.CharField(max_length=100, blank=True, null=True)
#     date_online=models.DateTimeField(null=True, blank=True)
#     date_offline=models.DateTimeField(null=True, blank=True)

    
#     license_img_front = models.FileField(null=True, blank=True)
#     # license_img_front_mandatory=models.BooleanField(default=False)
#     license_img_back = models.FileField(null=True, blank=True)
#     # license_img_back_license_mandatory=models.BooleanField(default=False)
#     license_expire_date = models.DateField(null=True, blank=True)
    
#     # emission_test_img = models.CharField(max_length=100, blank=True, null=True)
#     insurence_img = models.FileField(blank=True, null=True)
#     insurance_expire_date = models.DateField(null=True, blank=True)

#     # rc_img = models.CharField(max_length=100, blank=True, null=True)

#     passbook_img = models.FileField(blank=True, null=True)
#     # passbook_img=models.BooleanField(default=True)

#     # fitness_certificate_front_side_img = models.TextField(blank=True, null=True)
#     fitness_certificate_front_side_img_path = models.FileField(blank=True, null=True)
#     # fitness_certificate_front_side_img_mandatory=models.BooleanField(default=True)
#     fitness_certificate_back_side_img_path = models.FileField(blank=True, null=True)
#     # fitness_certificate_back_side_img_mandatory=models.BooleanField(default=True)
#     fitness_certificate_expire_date = models.DateField(null=True, blank=True)
    

#     live_lattitude = models.CharField(max_length=100, blank=True, null=True)
#     live_longitude = models.CharField(max_length=100, blank=True, null=True)

#     is_online = models.BooleanField(default=False)
#     time=models.IntegerField(blank=True, null=True)

#     create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
#     last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)

#     is_active = models.BooleanField(default=True)



# class PaymentDetails(models.Model):

#     in_order  = models.ForeignKey(InOrder, on_delete=models.CASCADE, blank=True, null=True, related_name="account_inorder")
#     amount = models.CharField(max_length=250, blank=True, null=True)
#     provider = models.CharField(max_length=250, blank=True, null=True)
#     payment_status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=True, null=True, related_name="account_payment")

#     create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
#     last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)
