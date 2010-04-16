/**
 * Clone form elements in Django forms. JQuery
 * is required by this function.
 */
function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id});
        if($(this).attr('type')!='hidden')$(this).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    newElement.css("display","none");
    $(selector).after(newElement);
    newElement.show("fast");
}

/**
 * A utility to name and create form elements
 */
function make_decs_for(node){
    var set = node.id.match(/[a-z]+-\d+/)[0]; // get django formset prefix
    return {'select':set+"-combodecs",
            'div':set+'-decstools',
            'input':set+'-searchfield',
            'button':set+'-searchbutton',
            'id':function(e){return 'id_'+ this[e];},
            'create':function(e){return $('<'+e+'>').attr('id',this.id(e)).attr('name',this[e]);},
            'set':set};
}

/**
 * This is the callback for decsclient app
 */
function make_decstool_callback(decs){
    return function(data){
        for(var i=0; i<data.length;i++){
            $("<option>").attr("value",data[i].fields.label)
                .html(data[i].fields.description)
                .appendTo('#'+decs.id('select'));
        }
        $('#'+decs.id('select')).change(function(evt){
            decs = make_decs_for(evt.target);
            $("input#id_"+decs.set+"-code")
                .attr("value",this.value);
            $("input#id_"+decs.set+"-text")
                .attr("value",$(this).find("option[selected]").html());
        });
    }
}

/**
 * Extend the django form and insert decs elements
 */
function getterm_event(decsclient_url) {
    return function(){
        this.parentNode.className = "";
        if(this.value === 'DeCS'){
            this.parentNode.className = "showdecs";
            var decs = make_decs_for(this);

            if($('#'+decs.id('select')).length === 0){
                decs.create('div')
                    .attr('class','decstool')
                    .appendTo(this.parentNode)
                    .append(decs.create('select'));

                $.get(decsclient_url,'',
                    make_decstool_callback(decs),"json");
            }
        }
    }
};

/**
 * Extend the django form and insert decs elements
 */
function search_event(decsclient_url,label) {
    return function(){
        this.parentNode.className = "";
        if(this.value === 'DeCS'){
            this.parentNode.className = "showdecs";
            var decs = make_decs_for(this);

            if($('#'+decs.id('input')).length === 0){

                decs.create('div')
                   .attr('class','decstool')
                   .appendTo(this.parentNode)
                   .append(decs.create('input'))
                   .append(decs.create('button').html(label));

                $('#'+decs.id('button'))
                    .click(function(evt){
                        var decs = make_decs_for(evt.target);
                        if($('#'+decs.id('select')).length === 0){
                            decs.create('select')
                                .insertAfter(this);
                        }
                        $('#'+decs.id('select')).html('');

                        $.get(decsclient_url+$('#'+decs.id('input')).val(),'',
                            make_decstool_callback(decs),
                            'json');
                        return false;
                    });
            }
        }
    }
};
