# from django.contrib import admin

# from .models import (ImageResearchField, CoverResearchField, 
#                      ImagePerson, CoverPerson, PicProfilePerson, 
#                      ImageNews, CoverNews, 
#                      CoverCarousel, 
#                      CoverTool)
# # from apps.notes.models import ReferenceNote


# # research 

# class ImageResearchFieldAdmin(admin.ModelAdmin):
#     list_display = ["id", "image", "reffield"]

#     class Meta: 
#         model = ImageResearchField


# class CoverResearchFieldAdmin(admin.ModelAdmin):
#     list_display = ["id", "image", "reffield", "isCover"]

#     class Meta: 
#         model = CoverResearchField


# # people

# class ImagePersonAdmin(admin.ModelAdmin):
#     list_display = ["id", "image", "reffield"]

#     class Meta: 
#         model = ImagePerson


# class CoverPersonAdmin(admin.ModelAdmin):
#     list_display = ["id", "image", "reffield", "isCover"]

#     class Meta: 
#         model = CoverPerson


# class PicProfilePersonAdmin(admin.ModelAdmin):
#     list_display = ["id", "image", "reffield", "isPic"]

#     class Meta: 
#         model = PicProfilePerson


# # news 

# class ImageNewsAdmin(admin.ModelAdmin):
#     list_display = ["id", "image", "reffield"]

#     class Meta: 
#         model = ImageNews


# class CoverNewsAdmin(admin.ModelAdmin):
#     list_display = ["id", "image", "reffield", "isCover"]

#     class Meta: 
#         model = CoverNews


# # carousel

# class CoverCarouselAdmin(admin.ModelAdmin):
#     list_display = ["id", "image", "reffield", "isCover"]

#     class Meta: 
#         model = CoverCarousel


# # tools

# class CoverToolAdmin(admin.ModelAdmin):
#     list_display = ["id", "image", "reffield", "isCover"]

#     class Meta: 
#         model = CoverTool


# admin.site.register(ImageResearchField, ImageResearchFieldAdmin)
# admin.site.register(CoverResearchField, CoverResearchFieldAdmin)
# admin.site.register(ImagePerson, ImagePersonAdmin)
# admin.site.register(CoverPerson, CoverPersonAdmin)
# admin.site.register(PicProfilePerson, PicProfilePersonAdmin)
# admin.site.register(ImageNews, ImageNewsAdmin)
# admin.site.register(CoverNews, CoverNewsAdmin)
# admin.site.register(CoverCarousel, CoverCarouselAdmin)
# admin.site.register(CoverTool, CoverToolAdmin)