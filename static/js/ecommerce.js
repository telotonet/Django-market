$(document).ready(function(){

    ///
    var contactForm = $(".contact-form")
    var contactMethod = contactForm.attr("method")
    var contactUrl = contactForm.attr("action")
   

    function sendContact(submitBtn, defaultText, doSubmit){
        if (doSubmit){
            submitBtn.addClass('disabled')
            submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending... ")
        } else {
                submitBtn.removeClass('disabled')
                submitBtn.html(defaultText)
        }}

    contactForm.submit(function(){
        event.preventDefault()
        var contactBtn = contactForm.find("[type='submit']")
        var contactBtnTxt = contactBtn.text()
        var contactFormData = contactForm.serialize()
        var thisContactForm = $(this)
        sendContact(contactBtn, "", true)
        $.ajax({
            method: contactMethod,
            url: contactUrl,
            data: contactFormData,
            success: function(data){

                thisContactForm[0].reset()
                $.alert({
                    title: "Success",
                    content: data.message,
                    theme: 'modern'
                })
                setTimeout(function(){
                    sendContact(contactBtn, contactBtnTxt, false)}, 1000)
            },
            error: function(error){
                
                var jsonData = error.responseJSON
                var msg = ''
                $.each(jsonData, function(key, value){
                    msg += "<li>" + value[0].message + "</li>" + "</br>"
                })
               $.alert({
                    title: "Error",
                    content: msg,
                    theme: 'modern'
                })
                 setTimeout(function(){
                    sendContact(contactBtn, contactBtnTxt, false)}, 500)
            }
        })
    })


    /// Auto Search
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='search']")
    var typingTimer;
    var typingInterval = 500
    var searchBtn = searchForm.find("[type='submit']")

    searchInput.keyup(function(event){
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)
    })
    searchInput.keydown(function(event){
        clearTimeout(typingTimer)
    })

    function doSearch(){
        searchBtn.addClass('disabled')
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching... ")
    }

    function performSearch(){
        doSearch()
        var query = searchInput.val()
        setTimeout(function(){
            window.location.href= "/search/?search=" + query
        }, 1000)
        
    }


    /// Cart + Add Products
    var productForm = $('.form-product-ajax')
    productForm.submit(function(event){
        event.preventDefault();
        var thisForm = $(this)
        // var actionEndpoint = thisForm.attr('action'); // API Endpoint
        var httpMethod = thisForm.attr('method');
        var formData = thisForm.serialize();
        var actionEndpoint = thisForm.attr('data-endpoint');
        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function(data){
                var currentPath = window.location.href
                console.log(currentPath)
                var submitSpan = thisForm.find('.submit-span')
                if (data.added){
                    
                    submitSpan.html('<button type="submit" class="btn btn-warning">Remove</button>')
                } else {
                    submitSpan.html('<button type="submit" class="btn btn-success">Add to cart</button>')
                 }
                var cartCounter = $('.navbar-cart-counter')
                cartCounter.text(data.cartItemCounter)
                if (currentPath.indexOf('cart') != -1) {
                    refreshCart()
                }
            },
            error: function(errorData){
                $.alert({
                    title: "Oops...",
                    content: "An error occurred. Please try again later :)",
                    theme: 'dark theme'

                })
            }})})

        function refreshCart(){
            console.log('refresh cart is ready')
            var cartTable = $('.cart-table')
            var cartBody  = cartTable.find('.cart-body')
            var cartTotal = $('.cart-total')
            var cartProducts = cartBody.find('.cart-products')
            var currentUrl = window.location.href



            var refreshCartUrl    = '/api/cart/'
            var refreshCartMethod = 'GET'
            var data = {}
            $.ajax({
                url: refreshCartUrl,
                method: refreshCartMethod,
                data: data,
                success: function(data){
                    var hiddentCartItemRemoveForm = $('.cart-item-remove-form')
                    if (data.products.length > 0)
                    {
                    cartProducts.html('')
                    i = data.products.length
                    $.each(data.products, function(index,value){
                        var newCartItemRemove = hiddentCartItemRemoveForm.clone()
                        newCartItemRemove.css('display', 'block')
                        newCartItemRemove.find('.cart-item-product-id').val(value.id)
                        cartBody.prepend('<tr><th scope="row">' + i + '</th><td><a href="' + value.url + '">' + value.title + '</a></td>' + '<td>' + value.description + '</td><td>' + value.price + ' $ </td>'  + '<td>' + newCartItemRemove.html() + '</td></tr>')
                        i--
                    })
                    cartTotal.text(data.total)
                    } else {
                        window.location.href = currentUrl
                    }

                },
                error: function(errorData){
                $.alert({
                    title: "Oops...",
                    content: "An error occurred. Please try again later :)",
                    theme: 'dark theme'

                })
                }})
                            }

})
