if (localStorage.getItem('cart') == null) {
    var cart = {};
} else {
    cart = JSON.parse(localStorage.getItem('cart'));
    document.getElementById('cart').innerHTML = Object.keys(cart).length;
    updateCart(cart);
}

// Find out cart is availabe or need to be created
if (localStorage.getItem('cart') == null) {
    var cart = {};
} else {
    cart = JSON.parse(localStorage.getItem('cart'));
    document.getElementById('cart').innerHTML = Object.keys(cart).length;
}

//Add item in cart when it is clicked
$('.cart').click(function() {
    var idstr = this.id.toString();
    console.log(idstr);
    if (cart[idstr] != undefined) {
        cart[idstr] = cart[idstr] + 1;
    } else {
        cart[idstr] = 1;
    }
    console.log(cart);
    localStorage.setItem('cart', JSON.stringify(cart));
    document.getElementById('cart').innerHTML = Object.keys(cart).length;
});

// If the add to cart button is clicked, add/increment the item
$('.cart').click(function() {
    var idstr = this.id.toString();
    if (cart[idstr] != undefined) {
        cart[idstr] = cart[idstr] + 1;
    } else {
        cart[idstr] = 1;
    }
    updateCart(cart);

});

//Add Popover to cart
$('#popcart').popover();
document.getElementById("popcart").setAttribute('data-content', '<h5>Cart for your items in my shopping cart</h5>');

function updatePopover(cart) {
    console.log('We are inside updatePopover');
    var popStr = "";
    popStr = popStr + "<h5> Cart for your items in my shopping cart </h5><div class='mx-2 my-2'>";
    var i = 1;
    for (var item in cart) {
        popStr = popStr + "<b>" + i + "</b>. ";
        popStr = popStr + document.getElementById('name' + item).innerHTML.slice(0, 19) + "... Qty: " + cart[item] + '<br>';
        i = i + 1;
    }
    popStr = popStr + "</div>"
    console.log(popStr);
    document.getElementById('popcart').setAttribute('data-content', popStr);
    $('#popcart').popover('show');
}

function updateCart(cart) {
    for (var item in cart) {
        document.getElementById('div' + item).innerHTML = "<button id='minus" + item + "' class='btn btn-primary minus'>-</button> <span id='val" + item + "''>" + cart[item] + "</span> <button id='plus" + item + "' class='btn btn-primary plus'> + </button>";
    }
    localStorage.setItem('cart', JSON.stringify(cart));
    document.getElementById('cart').innerHTML = Object.keys(cart).length;
    updatePopover(cart);
}
// If plus or minus button is clicked, change the cart as well as the display value
$('.divpr').on("click", "button.minus", function() {
    a = this.id.slice(7, );
    cart['pr' + a] = cart['pr' + a] - 1;
    cart['pr' + a] = Math.max(0, cart['pr' + a]);
    document.getElementById('valpr' + a).innerHTML = cart['pr' + a];
    updateCart(cart);
});
$('.divpr').on("click", "button.plus", function() {
    a = this.id.slice(6, );
    cart['pr' + a] = cart['pr' + a] + 1;
    document.getElementById('valpr' + a).innerHTML = cart['pr' + a];
    updateCart(cart);
});