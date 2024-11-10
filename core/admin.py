from django.contrib import admin

from .models import (Teacher, Course, Category, Variant, VariantItem, Cart, CartOrder, CartOrderItem, Question_Answer, 
                     Question_Answer_Message, EnrolledCourse, Certificate, CompletedLesson, Country, Coupon, Review, Notifications, Note, WishList)



admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Variant)
admin.site.register(VariantItem)
admin.site.register(Cart)
admin.site.register(CartOrder)
admin.site.register(CartOrderItem)
admin.site.register(Question_Answer)
admin.site.register(Question_Answer_Message)
admin.site.register(EnrolledCourse)
admin.site.register(Certificate)
admin.site.register(CompletedLesson)
admin.site.register(Country)
admin.site.register(Coupon)
admin.site.register(Review)
admin.site.register(Notifications)
admin.site.register(Note)
admin.site.register(WishList)
