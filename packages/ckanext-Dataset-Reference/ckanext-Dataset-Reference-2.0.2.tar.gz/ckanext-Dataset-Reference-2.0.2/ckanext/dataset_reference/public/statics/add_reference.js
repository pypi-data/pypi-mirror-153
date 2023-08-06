$(document).ready(function(){        
    $('#ref_submit_btn').click(function(e){    
        if($('#doi_or_bibtex').val() === 'doi'){  // the entry is a doi url/id
            let doi_input = $('#doi').val();
            $.ajax({
                url: $('#doi-validity-url').val(),
                cache:false,   
                data: {'doi_url': doi_input},            
                type: "POST",
                success: function(result){
                    if(result != '1'){                               
                        $('#doi_validation_message').text(result);           
                    }
                    else{
                        $('#ref-form').submit();
                    }                        
                }
            }); 
        }
        else{ // the entry is a bibtex
            let bibtex_input = $('#bibtex').val();
            $.ajax({
                url: $('#bibtex-validity-url').val(),
                cache:false,   
                data: {'bibtex': bibtex_input},            
                type: "POST",
                success: function(result){
                    if(result != '1'){                               
                        $('#bibtex_validation_message').text(result);           
                    }
                    else{
                        $('#ref-form').submit();
                    }                        
                }
            }); 
        }    
    });

    $('#doi').focusin(function(){
        $('#doi').css("background-color", 'white');
        $('#doi').addClass('link-enabled');
        $('#bibtex').removeClass('link-enabled');
        $('#bibtex').css("background-color", '#EBEBEB');
        $('#bibtex').val('');
        $('#doi_or_bibtex').val('doi');
        $('#bibtex_validation_message').text(''); 
    });


    $('#bibtex').focusin(function(){
        $('#bibtex').css("background-color", 'white');
        $('#bibtex').addClass('link-enabled');
        $('#doi').css("background-color", '#EBEBEB');
        $('#doi').removeClass('link-enabled');
        $('#doi').val('');
        $('#doi_or_bibtex').val('bibtex');
        $('#doi_validation_message').text('');   
    });

    $('#bibtex').keydown(function(){
        $('#bibtex_validation_message').text('');   
    });

    $('#doi').keydown(function(){
        $('#doi_validation_message').text('');   
    });

    $('#ref_add_close_btn').click(function(){
        $('#doi').val('');
        $('#bibtex').val('');
        $('#bibtex_validation_message').text('');  
        $('#doi_validation_message').text(''); 
    });
});