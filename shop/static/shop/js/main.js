(function($) {
	"use strict"

	if (localStorage.getItem('scrollPosition')) {
        window.scrollTo(0, parseInt(localStorage.getItem('scrollPosition')));
        localStorage.removeItem('scrollPosition');
    }

	// Mobile Nav toggle
	$('.menu-toggle > a').on('click', function (e) {
		e.preventDefault();
		$('#responsive-nav').toggleClass('active');
	})

	// Fix cart dropdown from closing
	$('.cart-dropdown').on('click', function (e) {
		e.stopPropagation();
	});

	/////////////////////////////////////////

	// Products Slick
	$('.products-slick').each(function() {
		var $this = $(this),
				$nav = $this.attr('data-nav');

		$this.slick({
			slidesToShow: 4,
			slidesToScroll: 1,
			autoplay: true,
			infinite: true,
			speed: 300,
			dots: false,
			arrows: true,
			appendArrows: $nav ? $nav : false,
			responsive: [{
	        breakpoint: 991,
	        settings: {
	          slidesToShow: 2,
	          slidesToScroll: 1,
	        }
	      },
	      {
	        breakpoint: 480,
	        settings: {
	          slidesToShow: 1,
	          slidesToScroll: 1,
	        }
	      },
	    ]
		});
	});

	// Products Widget Slick
	$('.products-widget-slick').each(function() {
		var $this = $(this),
				$nav = $this.attr('data-nav');

		$this.slick({
			infinite: true,
			autoplay: true,
			speed: 300,
			dots: false,
			arrows: true,
			appendArrows: $nav ? $nav : false,
		});
	});

	/////////////////////////////////////////

	// Product Main img Slick
	$('#product-main-img').slick({
    infinite: true,
    speed: 300,
    dots: false,
    arrows: true,
    fade: true,
    asNavFor: '#product-imgs',
  });

	// Product imgs Slick
  $('#product-imgs').slick({
    slidesToShow: 3,
    slidesToScroll: 1,
    arrows: true,
    centerMode: true,
    focusOnSelect: true,
		centerPadding: 0,
		vertical: true,
    asNavFor: '#product-main-img',
		responsive: [{
        breakpoint: 991,
        settings: {
					vertical: false,
					arrows: false,
					dots: true,
        }
      },
    ]
  });

	// Product img zoom
	var zoomMainProduct = document.getElementById('product-main-img');
	if (zoomMainProduct) {
		$('#product-main-img .product-preview').zoom();
	}

	/////////////////////////////////////////

	// Input number
	$('.input-number').each(function() {
		var $this = $(this),
		$input = $this.find('input[type="number"]'),
		up = $this.find('.qty-up'),
		down = $this.find('.qty-down');

		down.on('click', function () {
			var value = parseInt($input.val()) - 1;
			value = value < 1 ? 1 : value;
			$input.val(value);
			$input.change();
			updatePriceSlider($this , value)
		})

		up.on('click', function () {
			var value = parseInt($input.val()) + 1;
			$input.val(value);
			$input.change();
			updatePriceSlider($this , value)
		})
	});

	var priceInputMax = document.getElementById('price-max'),
		priceInputMin = document.getElementById('price-min');

	if(priceInputMax && priceInputMin){
		priceInputMax.addEventListener('change', function(event){
			event.preventDefault();
			updatePriceSlider($(this).parent() , this.value)
		});
	
		priceInputMin.addEventListener('change', function(event){
			event.preventDefault();
			updatePriceSlider($(this).parent() , this.value)
		});
	}

	function updatePriceSlider(elem , value) {
		if ( elem.hasClass('price-min') ) {
			console.log('min')
			priceSlider.noUiSlider.set([value, null]);
		} else if ( elem.hasClass('price-max')) {
			console.log('max')
			priceSlider.noUiSlider.set([null, value]);
		}
	}

	// Price Slider
	var priceSlider = document.getElementById('price-slider'),
		savedValueMin = localStorage.getItem('savedInputValueMin'),
		savedValueMax = localStorage.getItem('savedInputValueMax');

	if(savedValueMax){
		var beginning_max = savedValueMax
	}
	else{var beginning_max = 9999}

	if(savedValueMin){
		var beginning_min = savedValueMin
	}
	else{var beginning_min = 1}

	if (priceSlider) {
		noUiSlider.create(priceSlider, {
			start: [beginning_min, beginning_max],
			connect: true,
			step: 1,
			range: {
				'min': 1,
				'max': 9999
			}
		});

		priceSlider.noUiSlider.on('update', function( values, handle ) {
			var value = values[handle];
			//handle ? priceInputMax.value = value : priceInputMin.value = value
			if (handle) {
				priceInputMax.value = value;
				localStorage.setItem('savedInputValueMax', value);
			} else {
				priceInputMin.value = value;
				localStorage.setItem('savedInputValueMin', value);
			}
		});
	}

	function getCookie(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie !== "") {
		  const cookies = document.cookie.split(";");
		  for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + "=")) {
			  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
			  break;
			}
		  }
		}
		return cookieValue;
	}

	$('#newsletter-form').on('submit', function(e) {
		e.preventDefault();

		var email = $('#email-id');
		var request = $(this).attr('action');
		var csrf = $(this).find('input[name=csrfmiddlewaretoken]');

		var data = {
			csrfmiddlewaretoken: csrf.val(),
			email: email.val(),
			reqdata: request,
		}

		$.ajax({
			type: 'post',
			url: request,
			data: JSON.stringify(data),
			headers: {
				"X-Requested-With": "XMLHttpRequest",
				"X-CSRFToken": csrf.val(),  
			},
			success: function() {
				console.log('success: ', data)
			},
			error: function() {
				alert('js-error-newsletter')
			}
		});
	});

	$(document).ready(function(){
		$('.delete-wishlist-item-form').on('submit', function(e){
			e.preventDefault();
	
			var form = $(this);
			var item_pk = form.find('input[name=item-pk]').val();
			var request = form.attr('action');
			var csrf = $('input[name=csrfmiddlewaretoken]').val();
	
			var data = {
				csrfmiddlewaretoken: csrf,
				item: item_pk,
				type: "WishListOrderProduct",
				reqdata: request,
			}
	
			$.ajax({
				type: 'post',
				url: request,
				data: JSON.stringify(data),
				headers: {
					"X-Requested-With": "XMLHttpRequest",
					"X-CSRFToken": csrf,  
				},
				success: function(responseData) {
					console.log(responseData);
					$('#qty-wish').html(responseData['qty']);
					$('#qty-2-wish').html(responseData['qty-2']);
					$('#subtotal-wish').html(responseData['subtotal']);
					form.closest('.product-widget').remove();
					console.log('success: ', data);
				},
				error: function() {
					alert('js-error-delete-cart-item');
				}
			});
		});
	});

	$(document).ready(function(){
		$('.delete-cart-item-form').on('submit', function(e){
			e.preventDefault();
	
			var form = $(this);
			var item_pk = form.find('input[name=item-pk]').val();
			var request = form.attr('action');
			var csrf = $('input[name=csrfmiddlewaretoken]').val();
	
			var data = {
				csrfmiddlewaretoken: csrf,
				item: item_pk,
				type: "CartOrderProduct",
				reqdata: request,
			}
	
			$.ajax({
				type: 'post',
				url: request,
				data: JSON.stringify(data),
				headers: {
					"X-Requested-With": "XMLHttpRequest",
					"X-CSRFToken": csrf,  
				},
				success: function(responseData) {
					console.log(responseData);
					$('#qty').html(responseData['qty']);
					$('#qty-2').html(responseData['qty-2']);
					$('#subtotal').html(responseData['subtotal']);
					form.closest('.product-widget').remove();
					console.log('success: ', data);
				},
				error: function() {
					alert('js-error-delete-cart-item');
				}
			});
		});
	});

	$(document).ready(function() {
		$("button[data-action]").on("click", function(e) {
			e.preventDefault();
			
			let actionUrl = $(this).attr('data-action');
			let csrfToken = $('input[name=csrfmiddlewaretoken]').val();

			let data = {
				'csrfmiddlewaretoken': [csrfToken],
				'size': $("#size").val(),
				'color': $("#color").val(),
				'qty': $("input[name=qty]").val(),
				'product': $("#object-pk").val(),
			};

			$.ajax({
				type: 'POST',
				url: actionUrl,
				data: JSON.stringify(data),
				headers: {
					"X-Requested-With": "XMLHttpRequest",
					"X-CSRFToken": csrfToken
				},
				success: function(responseData) {
					window.location.reload(); 
				},
				error: function() {
					alert('An error occurred while processing your request.');
				}
			});
		});
	});

	$(document).ready(function() {
		$(".add-to-wishlist").on("click", function(e) {
			e.preventDefault();

			localStorage.setItem('scrollPosition', window.scrollY);

			let actionUrl = $(this).attr('data-action-by-default');
			let csrfToken = $(this).attr('csrf-token');

			let data = {
				'csrfmiddlewaretoken': [csrfToken],
				'type-collection': $(this).attr('type-collection'),
				'qty': '1',
				'product': $(this).attr("item-pk"),
			};

			$.ajax({
				type: 'POST',
				url: actionUrl,
				data: JSON.stringify(data),
				headers: {
					"X-Requested-With": "XMLHttpRequest",
					"X-CSRFToken": csrfToken
				},
				success: function(responseData) {
					console.log(responseData.items_of_collection)
					window.location.reload()
				}, 
				error: function(e) {
					alert('An error occurred while processing your request.');
				}
			});
		});
	});

	$(document).ready(function() {
		$(".add-to-cart-flag").on("click", function(e) {
			e.preventDefault();

			localStorage.setItem('scrollPosition', window.scrollY);

			const actionUrl = $(this).attr('data-action-by-default');
			const csrfToken = $(this).attr('csrf-token');

			let data = {
				'csrfmiddlewaretoken': [csrfToken],
				'type-collection': $(this).attr('type-collection'),
				'color': $(this).attr('default-color'),
				'size': $(this).attr('default-size'),
				'qty': '1',
				'product': $(this).attr("item-pk"),
			};

			$.ajax({
				type: 'POST',
				url: actionUrl,
				data: JSON.stringify(data),
				headers: {
					"X-Requested-With": "XMLHttpRequest",
					"X-CSRFToken": csrfToken
				},
				success: function(responseData) {
					console.log(responseData.items_of_collection)
					window.location.reload()
				}, 
				error: function(e) {
					alert('An error occurred while processing your request.');
				}
			});
		});
	});

	$(".add-to-compare").on("click", function(e) {
		e.preventDefault()

		const productUrl = $(this).attr("data-product-url");

		navigator.clipboard.writeText(productUrl).then(function() {
            alert('Product link copied to clipboard!');
        }).catch(function(err) {
            console.error('Failed to copy text: ', err);
            alert('Failed to copy product link.');
        });
	})

	document.addEventListener("DOMContentLoaded", function() {
		const modal = document.getElementById("modal");
		const openModalButton = document.querySelectorAll(".openModalButton");
		const closeButton = document.querySelector(".close");
		const modalImage = document.getElementById("modal-image");
	
		// Function to open the modal
		openModalButton.forEach(button => {
			button.addEventListener("click", function() {
				const image = $(this).attr("image-url");
				const description = $(this).attr("descrtiption");

				modalImage.src = image;
				
				modal.style.display = "block";
			});
		});
	
		// Function to close the modal
		closeButton.addEventListener("click", function() {
			modal.style.display = "none";
		});
	
		// Close the modal when clicking outside of the modal content
		window.addEventListener("click", function(event) {
			if (event.target === modal) {
				modal.style.display = "none";
			}
		});
	});

	function update_rating(rating, rating_list = []) {
		let container = $("#rating-avg")
		let container2 = $("#rating")
		if (rating == null && rating_list.length == 0) {
			rating = parseFloat(container.find("span").text())

			container2.find("li .sum ").each(function(index, element) {
				rating_list.push(element.textContent)
			})
			rating_list.reverse()
		} else {
			container.find("span").text(rating.toFixed(2))

			container2.find("li .sum ").each(function(index, element) {
				element.textContent = rating_list[(rating_list.length - 1) - index]
			})
		}

		container.find(".rating-stars i").each(function(index, element) {
			if (rating >= index + 1) {
				$(element).removeClass("fa fa-star-o").addClass("fa fa-star")
			}
		})

		let full_rating = 0;
		for (let i = 0; i < rating_list.length; i++) {
			full_rating += parseFloat(rating_list[i])
		}

		$(".rating-progress div").each(function(index, element) {
			let percent = (rating_list[(rating_list.length - 1) - index] / full_rating) * 100
			element.style.width = percent + "%"
		})
	}

	$('#review-form-id').on('submit', function(e) {
		e.preventDefault()
 
		let form = $(this);
		let text = form.find('textarea[name=review-text]');
		let rating = form.find('input[name=rating]:checked').val();
		let product_rating = form.find('input[name=review-product-rating]').val();
		let user = form.find('input[name=review-user]').val();
		let request = form.attr('action');
		let csrf = form.find('input[name=csrfmiddlewaretoken]').val();

		var data = {
			csrf: csrf,
			reqdata: request,
			text: text.val(),
			rating: rating,
			product_rating: product_rating,
			user: user,
		}

		$.ajax({
			type: 'post',
			url: request,
			data: JSON.stringify(data),
			headers: {
				"X-Requested-With": "XMLHttpRequest",
				"X-CSRFToken": csrf,  
			},
			success: function(responseData) {
				let rating_list = responseData["rating_list"]

				update_rating(rating=responseData["rating"], rating_list=rating_list)	
				fetch_reviews(1)

				text.val("");
			},
			error: function() {
				alert('js-error-create-review');
			}
		})
	})

	function fetch_reviews(page) {
		let product_rating_id = $("#product-rating-pk").val()
		$.ajax({
			url: `load_reviews/?product_rating_id=${product_rating_id}&page=${page}`,
			type: 'GET',
			success: function(respond) {
				console.log(respond)
				updateReviews(respond.reviews_data)
				updatePagination(respond)
			},
			error: function(error) {
				console.error("Error fetching reviews: ", error)
			}
		})
	}

	function updateReviews(reviews) {
		let reviewsContainer = $(".reviews")
		reviewsContainer.empty()

		reviews.forEach(element => {
			let html = '<li>' +
				'<div class="review-heading">' +
				'<h5 class="name">' + element["user__username"] + '</h5>' +
				'<p class="date">' + element["date_created"] + '</p>' +
				'<div class="review-rating">' +
				'<i class="fa fa-star"></i>'.repeat(Math.round(element["rating"])) +
				'<i class="fa fa-star-o"></i>'.repeat(5 - Math.round(element["rating"])) +
				'</div>' +
				'</div>' +
				'<div class="review-body">' +
				'<p class="random-text">' + element["text"] + '</p>' +
				'</div>' +
				'</li>';

			reviewsContainer.append(html)
		});
	}

	function updatePagination(data) {
		let cp = data.current_page
		let paginationContainer = $(".reviews-pagination")
		paginationContainer.empty()

		if (data.has_previous) {
			let prevPageButton = $(`<li><a href="javascript:void(0)"><i class="fa fa-angle-left"></i></a></li>`)
			prevPageButton.click(function() {
				fetch_reviews(parseInt(cp)-1)
			})
			paginationContainer.append(prevPageButton)
		}

		for (let i = cp-2; i <= cp+2; i++) {
			if (data.num_pages.indexOf(i) !== -1) {
				if (i == cp) {
					paginationContainer.append(`<li class="active">${i}</li>`)
				} else {
					let pageButton = $(`<li><a href="javascript:void(0);">${i}</a></li>`)
					pageButton.click(function() {
						fetch_reviews(i)
					})
					paginationContainer.append(pageButton)
				}
			}
		}

		if (data.has_next) {
			let nextPageButton = $(`<li><a href="javascript:void(0)"><i class="fa fa-angle-right"></i></a></li>`)
			nextPageButton.click(function() {
				fetch_reviews(parseInt(cp)+1)
			})
			paginationContainer.append(nextPageButton)
		}
	}

	if($("#reviews").length) {
		update_rating()
		fetch_reviews(1)
	}
	
})(jQuery);
