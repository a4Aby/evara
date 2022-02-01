$( document ).ready(function() {
    calculate();
});

$('#cartList > tbody  > tr > td.quantity').find('.qty-val').change(function() { 
    // var operation = $(this).attr('class');
    // var currentDiv = $(this).parent();
    // var availability = parseInt(currentDiv.data('availability'));
    // var count = parseInt(currentDiv.find('.qty-val').text());

    // if(operation == 'qty-up'){
    //     if(count > availability){
    //         console.log('hit')
    //         currentDiv.find('.qty-val').html(count);
    //     }
    // }else if(operation == 'qty-down'){
    //     console.log('down');
    // }
    calculate();
});

function calculate(){
    var subTotalArr = [];
    var currency = '₹'; 
    $('#cartList > tbody  > tr.data-tr').each(function(index, tr) { 
        var price = parseFloat($(this).find('td.price').data('price'));
        var quantityDiv = $(this).find('td.quantity');
        var quantity = quantityDiv.find('.qty-val').val();
        var subTotal = price*quantity;
        subTotalArr.push(subTotal);
        $(this).find('td.subTotal').find('span').html(currency+' '+subTotal);
     });
     var total = 0;
     $.each(subTotalArr,function(){total+=parseFloat(this) || 0;});
     $('#totalPrice').html(currency+' '+total);
     $('#finalPrice').html(currency+' '+total);
}

