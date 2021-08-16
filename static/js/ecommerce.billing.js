$(document).ready(function(){
var stripeFormModule = $(".stripe-payment-form")
var stripeModuleToken = stripeFormModule.attr('data-token')
var stripeModuleNextUrl = stripeFormModule.attr('data-next-url')
var stripeModuleBtnTitle = stripeFormModule.attr('data-btn-title') || 'Add card'


var stripeTemplate = $.templates("#stripeTemplate")
var stripTemplateDataContext = {
    publishKey: stripeModuleToken,
    nextUrl: stripeModuleNextUrl,
    btnTitle: stripeModuleBtnTitle,
}
var stripeTemplateHtml = stripeTemplate.render(stripTemplateDataContext)

stripeFormModule.html(stripeTemplateHtml)

var paymentForm = $(".payment-form")
if (paymentForm.length > 1){
    $.alert({
        title: "Oops...",
        content: "Only one payment form is allowed per page",
        theme: 'dark theme'
    })
    paymentForm.css("display", 'none')
} else if (paymentForm.length == 1){

var publishKey = paymentForm.attr('data-token')
var nextUrl = paymentForm.attr('data-next-url')

var stripe   = Stripe(publishKey)
var elements = stripe.elements()

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
            stripeTokenHandler(nextUrl, result.token);
            
        }
    });
});

function redirectToNext(nextPath){
    if (nextPath){
        setTimeout(function(){
            window.location.href = nextPath
        }, 2000)
    }
}

function stripeTokenHandler(nextUrl, token){
    var paymentMethodEndpoint = '/payment/create/'
    var data = {
        'token': token.id,
    }
    $.ajax({
        data: data,
        url: paymentMethodEndpoint,
        method: 'POST',
        success: function(data){
            var successMsg = data.message
            if (nextUrl){
                successMsg += "<br><br><i class='fa fa-spin fa-spinner'></i> Redirect..."
            }
            card.clear()
            $.alert({title: "Success", content: successMsg, theme: 'modern'})
            redirectToNext(nextUrl)
        },
        error: function(error){
            $.alert({
                title: "Oops...",
                content: "An error occurred",
                theme: 'dark theme'
            })}})}}})