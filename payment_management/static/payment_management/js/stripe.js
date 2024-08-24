async function stripe_payment(form, csrf_token) {
    try {
        const response = await fetch('/config/', {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrf_token,
            }
        });
        const data = await response.json();
        console.log(data);

        if (data.publicKey) {
            let stripe = Stripe(data.publicKey);
            let elements = stripe.elements();

            const cardNumberElement = elements.create('cardNumber');
            cardNumberElement.mount('#cardNumber');

            const cardExpiryElement = elements.create('cardExpiry');
            cardExpiryElement.mount('#cardExpiry');

            const cardCvcElement = elements.create('cardCvc');
            cardCvcElement.mount('#cardCvc');

            return {stripe, cardNumberElement};
        } else {
            console.log("Stripe public key is not found");
        }
    } catch (error) {
        console.log("Error fetching Stripe public key: ", error);
    }
}

async function getStripeToken(stripe, cardNumberElement) {
    try {
        const result = await stripe.createToken(cardNumberElement);
        if (result.error) {
            const errorElement = document.getElementById('card-errors');
            errorElement.textContent = result.error.message;
        } else {
            return result.token;
        }
    } catch (error) {
        alert('Insert card data into fields');
        console.error('Error creating token:', error);
    }
}

async function stripeTokenHandler(token, form, stripe, cardNumberElement) {
    try {
        const csrf_token = form.elements['csrfmiddlewaretoken'].value;

        const formData = new FormData();
        formData.append('token_id', token.id);
        formData.append('csrfmiddlewaretoken', csrf_token);

        const response = await fetch("/payment-intent/", {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrf_token,
            },
            body: formData
        });

        const respond = await response.json();

        if (respond.client_secret) {
            const result = await stripe.confirmCardPayment(respond.client_secret, {
                payment_method: {
                    card: cardNumberElement,
                }
            });

            if (result.error) {
                console.error(result.error.message);
            } else if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
                //alert('Payment successful!');
                return result
                // Optionally redirect to a success page
            }
            
        } else {
            alert('Payment failed')
        }

    } catch (error) {
        console.error('Error sending Stripe token:', error);
    }
}

// document.addEventListener("DOMContentLoaded", async function() {

//     const form = document.getElementById("credit-card-form");
//     //const submitButton = document.getElementById("register-button");

//     if (!form) {
//         return;
//     }

//     const csrf_token = form.elements['csrfmiddlewaretoken'].value;

//     try {
//         const response = await fetch('/config/', {
//             method: 'GET',
//             headers: {
//                 'X-Requested-With': 'XMLHttpRequest',
//                 'X-CSRFToken': csrf_token,
//             }
//         });
//         const data = await response.json();
//         console.log(data);

//         if (data.publicKey) {
//             initializeStripe(data.publicKey, form);
//         } else {
//             console.log("Stripe public key is not found");
//         }
//     } catch (error) {
//         console.log("Error fetching Stripe public key: ", error);
//     }


//     function initializeStripe(publicKey, form) {
//         let stripe = Stripe(publicKey);
//         let elements = stripe.elements();

//         const cardNumberElement = elements.create('cardNumber');
//         cardNumberElement.mount('#cardNumber');

//         const cardExpiryElement = elements.create('cardExpiry');
//         cardExpiryElement.mount('#cardExpiry');

//         const cardCvcElement = elements.create('cardCvc');
//         cardCvcElement.mount('#cardCvc');

//         form.addEventListener('submit', async function(event) {
//             event.preventDefault();

//             try {
//                 const result = await stripe.createToken(cardNumberElement);
//                 if (result.error) {
//                     const errorElement = document.getElementById('card-errors');
//                     errorElement.textContent = result.error.message;
//                 } else {
//                     let resultToken = await stripeTokenHandler(result.token, form, stripe, cardNumberElement);
//                 }
//             } catch (error) {
//                 console.error('Error creating token:', error);
//             }
//         });
//     }

//     async function stripeTokenHandler(token, form, stripe, cardNumberElement) {
//         try {
//             const csrf_token = form.elements['csrfmiddlewaretoken'].value;

//             const formData = new FormData();
//             formData.append('token_id', token.id);
//             formData.append('csrfmiddlewaretoken', csrf_token);

//             const response = await fetch("/payment-intent/", {
//                 method: 'POST',
//                 headers: {
//                     'X-Requested-With': 'XMLHttpRequest',
//                     'X-CSRFToken': csrf_token,
//                 },
//                 body: formData
//             });

//             const respond = await response.json();

//             if (respond.client_secret) {
//                 const result = await stripe.confirmCardPayment(respond.client_secret, {
//                     payment_method: {
//                         card: cardNumberElement,
//                     }
//                 });

//                 if (result.error) {
//                     console.error(result.error.message);
//                 } else if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
//                     alert('Payment successful!');
//                     // Optionally redirect to a success page
//                 }
                
//             } else {
//                 alert('Payment failed')
//             }

//         } catch (error) {
//             console.error('Error sending Stripe token:', error);
//         }
//     }
// });
