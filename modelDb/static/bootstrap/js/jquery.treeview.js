   <script type="text/javascript">
        var d=true;
        $(function () {
            $('.tree li:has(ul)').addClass('parent_li').find(' > span').attr('title', 'Collapse this branch');
            $('.tree li.parent_li > span').on('click', function (e) {
                var d = $(this).siblings('ul').is(":visible");
                $(this).siblings('ul').slideToggle('fast');//.siblings('dt').css('background-position','right -40px');
                if (d) {
                    console.log($(this).find(">i"));
                    $(this).find(">i").addClass('icon-minus-sign').removeClass('icon-plus-sign');
                    
                } else {
                  //  $(this).find(' > i').addClass('icon-minus-sign').removeClass('icon-plus-sign');
                    $(this).find(">i").addClass('icon-plus-sign').removeClass('icon-minus-sign');
                }
                e.stopPropagation();
            });
        });
 
    </script>
