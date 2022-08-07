var stripe = Stripe('pk_test_51L3WtpIU7sBPiFFAyGeQx7lRvAkF8XCzvNWiwK5VgloVlxxzPHOgP2vj7mde43C9FzSmFDILMa020v1GQ6jdyvrY00ILiwrCOG');
    var elements = stripe.elements();

    var card = elements.create('card');
    

    card.mount('#card-element');

    var form = document.getElementById('payment-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        console.log('card', card)

        stripe.createToken(card).then(function(result) {
            if (result.error) {
                var errorElement = document.getElementById('card-errors');
                errorElement.textContent = 'test error';
            } else {
                stripeTokenHandler(result.token);
            }
        });
    });

    function stripeTokenHandler(token) {
        var form = document.getElementById('payment-form');
        var hiddenInput = document.createElement('input');
        hiddenInput.setAttribute('type', 'hidden');
        hiddenInput.setAttribute('name', 'stripe_token');
        hiddenInput.setAttribute('value', token.id);
        form.appendChild(hiddenInput);

        form.submit();
    }