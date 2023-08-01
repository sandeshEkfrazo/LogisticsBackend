from django.db import models

class UserRoleRef(models.Model):
    user_role_name = models.CharField(max_length=250, blank=True, null=True)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp")
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp")

    def _str_(self):
        return self.user_role_name

class Status(models.Model):
    status_name= models.CharField(max_length=250, blank=True, null=True)
    colour = models.CharField(max_length=250, blank=True, null=True)
    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)

    def _str_(self):
        return self.status_name

class Filesize(models.Model):
    file_type = models.CharField(max_length=100, blank=True, null=True) 
    size = models.CharField(max_length=100, blank=True, null=True) 

class Queries(models.Model):
    questions = models.CharField(max_length=100, blank=True, null=True)
    answer = models.TextField(blank=True, null=True) 
    isfor = models.ForeignKey(UserRoleRef, on_delete=models.CASCADE, blank=True, null=True, related_name="is_for")
    status= models.CharField(max_length=100, blank=True, null=True)
    # user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True,null=True)

    def __str__(self):
        return self.questions

class Language(models.Model):
    name=models.CharField(max_length=200, null=True, blank=True)

class Subscriptionplan(models.Model):
    time_period=models.CharField(max_length=100,blank=True,null=True)
    validity_days=models.IntegerField(blank=True, null=True)
    amount=models.FloatField(blank=True,null=True)
    type_of_service= models.CharField(max_length=100,blank=True,null=True)
    status=models.CharField(max_length=100,blank=True,null=True)


class Aboutus(models.Model):
    logo = models.ImageField(blank=True, null=True)
    heading = models.CharField(max_length=300, blank=True, null=True)
    paragraph = models.TextField(blank=True, null=True)
    phone_number=models.CharField(max_length=10, blank=True, null=True)
    alternate_phone_number=models.CharField(max_length=10, blank=True, null=True)
    text=models.TextField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)


class BookingDistance(models.Model):
    threshold_value = models.IntegerField()
    incremented_value = models.IntegerField()
    description = models.TextField()
    last_km_value = models.IntegerField(null=True,blank=2)

    def __str__(self):
        return self.threshold_value

class Timesearch(models.Model):
    time = models.IntegerField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.time)


