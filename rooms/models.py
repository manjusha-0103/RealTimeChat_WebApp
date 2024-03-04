from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Teams(models.Model):
    room_image = models.ImageField(upload_to='team_profile/', blank=True, null=True)
    room_name = models.CharField(max_length=200, blank=False, null=False, unique= True)
    slug = models.CharField(max_length=200, blank=False, null=False, unique= True)
    members = models.ManyToManyField(get_user_model())

    def __str__(self):
        return self.room_name
    
    def add_user_to_group(self, user:get_user_model()): # type: ignore
        '''A helper function to add a user to a group and create an event object'''
        self.members.add(user)
        self.event_set.create(type="Join", user=user)
        self.save()
        print("added in grp")

    def remove_user_from_group(self, user:get_user_model()): # type: ignore
        '''An helper function to remove users from group members when they \
        leave the group and create an event for the timestamp the user left the group'''
        self.members.remove(user)
        self.event_set.create(type="Left", user=user)
        self.save()
    

    
class Messages(models.Model):
    user = models.ForeignKey(get_user_model(), related_name = 'messages',on_delete=models.CASCADE)
    room = models.ForeignKey(Teams(), related_name = 'messages',on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add = True)

    

    
