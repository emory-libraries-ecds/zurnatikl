from django.contrib import admin
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe 
from danowski.apps.geo.models import GeonamesCountry, GeonamesContinent, StateCode, Location
from danowski.apps.people.models import School, Person
from danowski.apps.journals.models import Journal, Issue
from danowski.apps.admin.models import LinkedInline

# admin.site.register(GeonamesContinent)
# admin.site.register(GeonamesCountry)
# admin.site.register(StateCode)

def get_admin_url(obj):
    module_name = obj._meta.module_name.split('_')[0]
    id = obj.id
    url = "admin:%s_%s_change" % (obj._meta.app_label, module_name)
    for property, value in vars(obj).iteritems():
      if(property == module_name+"_id"):
        print property, ": ", value
        id = value
    return reverse(url, args=(id,))

        
class SchoolInline(LinkedInline):
    model = School

class PersonInline(admin.TabularInline):
    model = Person.dwelling.through
    extra = 0
    verbose_name = "Associated People"
    verbose_name_plural = verbose_name
    readonly_fields = ['link']
    
    def link(self, obj):
        url = get_admin_url(obj)
        return mark_safe("<a href='%s'>edit</a>" % url)  

    # the following is necessary if 'link' method is also used in list_display
    link.allow_tags = True
    

class JournalPublicationInline(LinkedInline):
    model = Issue
    fk_name = 'publication_address'
    extra = 0
    verbose_name = "Publication Addresses for Journals"
    verbose_name_plural = verbose_name

class JournalPrintingInline(LinkedInline):
    model = Issue
    fk_name = 'print_address'
    extra = 0
    verbose_name = "Printing Addresses for Journals"
    verbose_name_plural = verbose_name
    admin_model_parent = 'journals'
    
class JournalMailingInline(admin.TabularInline):
    model = Issue.mailing_addresses.through
    extra = 0
    verbose_name = "Mailing Addresses for Journals"
    verbose_name_plural = verbose_name
    admin_model_parent = 'journals'
    readonly_fields = ['link']
    
    def link(self, obj):
        url = get_admin_url(obj)
        return mark_safe("<a href='%s'>edit</a>" % url)  

    # the following is necessary if 'link' method is also used in list_display
    link.allow_tags = True
    

class LocationAdmin(admin.ModelAdmin):
    class Media:
      js = (settings.STATIC_URL + 'js/admin/collapseTabularInlines.js',)
      css = { "all" : (settings.STATIC_URL +"css/admin/hide_admin_original.css",) }
     
    list_display = ['street_address', 'city', 'state', 'zipcode', 'country']
    search_fields = ['street_address', 'city', 'state', 'zipcode', 'country']
    inlines = [
        PersonInline, 
        SchoolInline,
        JournalPublicationInline,
        JournalPrintingInline,
        JournalMailingInline
        ]
    
admin.site.register(Location, LocationAdmin)
