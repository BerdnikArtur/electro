from django.http import HttpRequest, JsonResponse
from django.db import transaction
from django.core.paginator import Paginator

from .forms import ReviewForm
from .models import Review

import json

class ProductPageReviewsService:

    @staticmethod
    def create_review(request: HttpRequest) -> JsonResponse:
        data = json.load(request)
        form = ReviewForm(data)
        if form.is_valid():
            with transaction.atomic():
                review = form.save()
                rating = review.product_rating
                rating.update_rating(review.rating)
            rating_list = [rating.one_star, rating.two_star, rating.three_star, rating.four_star, rating.five_star]
                
            response_data = {
                'rating': rating.rating,
                'rating_list': rating_list,
            }
            return JsonResponse(response_data)
        
    @staticmethod
    def load_reviews(request: HttpRequest) -> JsonResponse:
        product_rating_id = request.GET.get("product_rating_id")
        reviews = Review.objects.filter(product_rating=product_rating_id).order_by("-date_created")

        paginator = Paginator(reviews, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        reviews_data = list(page_obj.object_list.values('text', 'rating', 'date_created', 'user__username'))
        for review in reviews_data:
            review['date_created'] = review['date_created'].strftime("%d %B %Y, %-I:%M %p")

        data = {
            'reviews_data': reviews_data,
            'num_pages': [i for i in paginator.page_range],
            'current_page': page_number,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(), 
        }

        return JsonResponse(data)