document.addEventListener("DOMContentLoaded", async function() {

    const form = document.getElementById("credit-card-form");

    if (!form) {
        return;
    }

    const submitButton = document.getElementById("order-button");
    const terms = document.getElementById("terms");
    const csrf_token = form.elements['csrfmiddlewaretoken'].value;

    terms.addEventListener("change", function() {
        if (terms.checked) {
            submitButton.disabled = false;
        } else {
            submitButton.disabled = true;
        }
    });

    let {stripe, cardNumberElement} = await stripe_payment(form, csrf_token)

    form.addEventListener("submit", async function(e) {
        e.preventDefault()
        try {

            let stripe_token = await getStripeToken(stripe, cardNumberElement)

            const data = new FormData();
            data.append('csrfmiddlewaretoken', csrf_token);

            data.append('billing_address', JSON.stringify({
                'first_name': form.elements['first_name'].value,
                'last_name': form.elements['last_name'].value,
                'address': form.elements['address'].value,
                'city': form.elements['city'].value,
                'state': form.elements['state'].value,
                'country': form.elements['country'].value,
                'zip_code': form.elements['zip_code'].value,
                'telephone': form.elements['telephone'].value,
            }));

            data.append('shiping_address', JSON.stringify({
                'first_name': form.elements['first_name_ship'].value,
                'last_name': form.elements['last_name_ship'].value,
                'address': form.elements['address_ship'].value,
                'city': form.elements['city_ship'].value,
                'state': form.elements['state_ship'].value,
                'country': form.elements['country_ship'].value,
                'zip_code': form.elements['zip_code_ship'].value,
                'telephone': form.elements['telephone_ship'].value,
            }));
 
            data.append('order_notes', form.elements['order_notes'].value);

            const selectedPayment = form.querySelector('input[name=payment]:checked');
            if (selectedPayment) {
                data.append('payment_method', selectedPayment.ariaLabel);
            }

            // try {
            //     const [data1, data2] = await Promise.all([
            //         fetch_checkout_fields(data, csrf_token),
            //         stripeTokenHandler(stripe_token, form, stripe, cardNumberElement)
            //     ]);
            
            //     console.log('Both fetch requests were successful');
            //     console.log('Data from request 1:', data1);
            //     console.log('Data from request 2:', data2);
            
            //     // Proceed with further actions using data1 and data2
            // } catch (error) {
            //     console.error('One or both fetch requests failed:', error);
            // }
            try {
                const data1 = await fetch_checkout_fields(data, csrf_token);

                if (!data1.status == 'error') {
                    throw new Error('fetch_checkout_fields failed with status ' + response.status);
                }
            
                // Proceed to stripeTokenHandler only if fetch_checkout_fields was successful
                const data2 = await stripeTokenHandler(stripe_token, form, stripe, cardNumberElement);
            
                console.log('Both fetch requests were successful');
                console.log('Data from fetch_checkout_fields:', data1);
                console.log('Data from stripeTokenHandler:', data2);
            
                // Proceed with further actions using data1 and data2
            } catch (error) {
                console.error('One or both fetch requests failed:', error);
            }

        } catch (error) {
            console.error('Error sending fileds\' and payment data', error);
        };

        async function fetch_checkout_fields(data, csrf_token) {
            const billingAddressJSON = data.get("billing_address");

            const billingAddressObj = JSON.parse(billingAddressJSON);

            const billingAddressData = new FormData();
            for (const [key, value] of Object.entries(billingAddressObj)) {
                billingAddressData.append(key, value);
            }
            
            let result = await fetch(window.location.href, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrf_token,
                },
                body: billingAddressData,
            });

            return await result.json()
        }
    })
});