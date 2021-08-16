var stripe = Stripe('pk_test_6pRNASCoBOKtIshFeQd4XMUh');
var elements = stripe.elements();

var style = {
    base: {
        color: '#32325d',
        lineHeight: "24px",
        fonFamily: '"Helvetica Neue", Halvetica, sans-serif',
        fontSmoothing: 'antialiased',
        '::placeholder': {
            color: "#aab7c4"
        }
    },
    invalid: {
        color: "#fa755a",
        iconColor: "#fa755a"
    }
};

var card = elements.create('card', {style:style});

card.mount("#card-element")
card.addEventListener('change', function(event){
    var displayError = document.getElementById('card-errors');
    if (event.error){
        displayError.textContent= event.error.messsage;
    } else {
        displayError.textContent = '';
    }
});

var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event){
    event.preventDefault();

    stripe.createToken(card).then(function(result){
        if (result.error){
            var errorElement = document.getElementById('card-errors');
            errorElement.textContent = result.error.messsage;
        } else {
            stripeTokenHandler(result.token);
        }
    });
});
function stripeTokenHandler(token){
}
