function categoryfilter(cId){
    $('.productList').each(function( index ) {
        console.log( $(this).attr('category'));
        if(cId == $(this).attr('category') )
            $(this).hide();
        else
            $(this).show();
    });
}
