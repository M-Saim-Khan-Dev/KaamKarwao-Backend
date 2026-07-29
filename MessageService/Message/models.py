from django.db import models

# Create your models here.

class Message(models.Model):
    room_id = models.IntegerField()
    sender_id = models.IntegerField()
    body = models.TextField()
    attachment_id = models.IntegerField(null=True, blank=True)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name= 'replies')
    sequence = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank= True)

    class Meta:
        # makes sure we get all the messages in a particular sequence
        ordering = ['sequence']
        # gives us the messages quickly by looking at room_id, sequence pair, this will get the messages of the entire room in sequence
        indexes = [models.Index(fields=['room_id', 'sequence'])]
    