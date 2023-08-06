from django.db import models


class Position(models.Model):
    """Reusable position that can be used in multiple elections
    
    The definition of a position simply defines a single position that can be 
    used in multiple elections, e.g. Chair. The Chair position can be included 
    in many elections

    Attributes:
        title (str): The title of the position, e.g. Chair, Treasurer
        admin_title (str): A verbose title, for if there are similar positions 
            which have the same name, but are mutually exclusive in their 
            jurisdiction. Use this if running elections for 2 different 
            societies. Only displayed on the admin pages.
        description (str): What the position entails, a job description
    """
    title = models.CharField(
        max_length=100
    )
    admin_title = models.CharField(
        max_length=500,
        help_text='Long title to give to position in admin pages to '
        'differentiate between similar roles that are mutually exclusive in '
        'their purpose, e.g. Chair for two different societies'
    )
    description = models.TextField()

    def __str__(self):
        return self.admin_title
