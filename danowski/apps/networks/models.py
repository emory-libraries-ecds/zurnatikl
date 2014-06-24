from django.db import models
from danowski.apps.geo.models import GeonamesCountry, StateCode
from django_date_extensions import fields as ddx


def country_choices():
    return tuple((c.code, '%s (%s)' % (c.name, c.code)) for c in GeonamesCountry.objects.all())

def state_choices():
    return tuple((s.code, '%s (%s)' % (s.name, s.code),) for s in StateCode.objects.all())



class Location(models.Model):
    """
    Locations or Addresses
    """

    street_address = models.CharField(max_length=255, blank=True, help_text='Street name and number')
    '''Street name and number'''
    city = models.CharField(max_length=255, help_text='City name')
    '''City name'''
    state = models.CharField(max_length=2, blank=True, help_text='State name', choices=state_choices())
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=2, help_text='Country name', choices=country_choices())
    ''' Country name'''

    def __unicode__(self):
        return '%s %s %s %s %s' \
               % (self.street_address, self.city, self.state, self.zipcode, self.country)

    class Meta:
        unique_together = ('street_address', 'city', 'state', 'zipcode', 'country')


class School(models.Model):
    '''School of poetry'''

    CATEGORIZER_CHOICES =(
        ('Donald Allen', 'Donald Allen'),
    )

    name = models.CharField(max_length=255)
    ''' Name of school of poetry'''
    categorizer = models.CharField(max_length=100, blank=True, choices=CATEGORIZER_CHOICES)
    '''Name of categorizer'''
    location = models.ForeignKey('Location', blank=True, null=True)
    ''':class:`Location` of school of poetry'''
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'categorizer', 'location')


class Name(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    person = models.ForeignKey('Person')

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

class PenName(models.Model):
    name = models.CharField(max_length=200)
    person = models.ForeignKey('Person')

    def __unicode__(self):
        return self.name


class PlaceName(models.Model):
    name = models.CharField(max_length=200)
    person = models.ForeignKey('IssueItem')

    def __unicode__(self):
        return self.name



class Person(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    RACE_CHOICES = (
        ('White', 'White'),
        ('Black or African American', 'Black or African American'),
        ('American Indian or Alaska Native', 'American Indian or Alaska Native'),
        ('Asian', 'Asian'),
        ('Native Hawaiian or Other Pacific Islander', 'Native Hawaiian or Other Pacific Islander'),
        ('Hispanic', 'Hispanic'),
        ('Latino', 'Latino'),
    )

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    race = models.CharField(max_length=50, blank=True, choices=RACE_CHOICES)
    racial_self_description = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=1, blank=True, choices=GENDER_CHOICES)
    schools = models.ManyToManyField('School', blank=True)
    uri = models.URLField(blank=True)
    dwelling = models.ManyToManyField('Location', blank=True)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        verbose_name_plural = 'People'
        unique_together = ('first_name', 'last_name')

class Journal(models.Model):
    title = models.CharField(max_length=255)
    uri = models.URLField(blank=True)
    publisher = models.CharField(max_length=100)
    issn = models.CharField(max_length=50, blank=True)
    schools = models.ManyToManyField('School', blank=True)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.title


class Issue(models.Model):

    SEASON_CHOICES = (
        ('Winter', 'Winter'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Fall', 'Fall')
    )

    journal = models.ForeignKey('Journal')
    volume = models.CharField(max_length=255)
    issue = models.CharField(max_length=255)
    publication_date = ddx.ApproximateDateField(help_text='YYYY , MM/YYYY, MM/DD/YYYY')
    season = models.CharField(max_length=10, blank=True, choices=SEASON_CHOICES)
    editors = models.ManyToManyField("Person")
    contributing_editors = models.ManyToManyField("Person", related_name='contributing_editors', blank=True, null=True)
    publication_address = models.ForeignKey("Location", help_text="address of publication", related_name='publication_address')
    print_address = models.ForeignKey("Location", blank=True, help_text="address where issue was printed", related_name='print_address', null=True)
    mailing_addresses  = models.ManyToManyField("Location", blank=True, help_text="addresses where issue was mailed", related_name='mailing_addresses', null=True)
    physical_description = models.CharField(max_length=255)
    numbered_pages = models.BooleanField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return '%s vol. %s issue %s' % (self.journal, self.volume, self.issue)


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class IssueItem(models.Model):
    issue = models.ForeignKey('Issue')
    title = models.CharField(max_length=255)
    creators = models.ManyToManyField('Person', through='CreatorName', related_name='creators_name')
    anonymous = models.BooleanField(help_text='check if labeled as by Anonymous')
    no_creator = models.BooleanField(help_text='check if no author is listed [including Anonymous')
    translator = models.ManyToManyField('Person', related_name='translator_name', blank=True, null=True)
    start_page = models.IntegerField(max_length=6)
    end_page = models.IntegerField(max_length=6)
    genre = models.ManyToManyField('Genre')
    abbreviated_text = models.BooleanField(help_text='check if the text contains abbreviations such as wd, yr, etc')
    persons_mentioned= models.ManyToManyField('Person', related_name='persons_mentioned', blank=True, null=True)
    addresses = models.ManyToManyField('Location', blank=True, null=True)
    literary_advertisement = models.BooleanField()
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

class CreatorName(models.Model):
    issue_item = models.ForeignKey("IssueItem")
    person = models.ForeignKey("Person")
    name_used = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title