///crft
function getCSRFToken() {
    return $('meta[name="csrf-token"]').attr('content');
}
//console.log("CSRF Token:", getCSRFToken());
//menu filter
$(document).ready(function() {
    // Your JavaScript code here
    //toggle menu
    $("#event-filter-btn").on("click", function(e) {
        e.stopPropagation();
        $("#event-filter-menu").toggleClass("hidden");
    });

    //fermer le menu en cliquant en dehors
    $(document).on("click", function() {
        $("#event-filter-menu").addClass("hidden");
    });

});

/////----- POPOVER BUTTON ------/////
$(document).ready(function() {

    $(".option-btn").on("click", function(e) {
        e.stopPropagation();
        let id = $(this).data("id");
        let name = $(this).data('name')

        $("#popoverItemName").text(name);

        //fermer les autres menus
        $(".options-menu").addClass("hidden");

        //ouvrir celui cliquer
        $(this).next('.options-menu').toggleClass("hidden");
    });

});
//fermer le menu en cliquant en dehors
$(document).on("click", function() {
    $(".options-menu").addClass("hidden");
});

/////-------- NAVIGATION --------////
$(document).on("click", ".row-click", function() {
    window.location = $(this).data("url");
});

///---- INSERTION D'UN EVENEMENT -----///
$(document).ready(function(){

    $('#addEvenementBtn').on('click', function(){

        let nom = $("#nom_event").val().trim();

        if (nom === "" ){
            $("#nom_event").addClass("border-red-600").next(".error").removeClass("hidden");
        }
        else{
            $("#nom_event").removeClass("border-red-600").next(".error").addClass("hidden");
        }

        $.ajax({
            type: "POST",
            url: "new-event/",
            header:{
                'X-CSRFToken': getCSRFToken()
            },
            data:{
                nom : $("#nom_event").val(),
                csrfmiddlewaretoken: getCSRFToken()
            },
            success: function(response) {
                console.log("Evenement ajouté avec succès !!!"+response);
            },
            error: function (response) { console.log('Erreur AJAX !!!'+response);}

        }).done(function(){
            console.log(" ajouté avec succès !");
            window.location.reload();
        });

    });

    $('#nom_event').on("input", function (){
        $(this).removeClass("border-red-600").next(".error").addClass("hidden");
    });

});

////-------- FILTRAGR ICI ---------////
$(document).ready(function (){

    $('#champ_filtre').on("keyup", function(){
        let value = $(this).val().toLowerCase();

        $(".indicator-card").each(function () {
            let name = $(this).data("name");

            $(this).toggle(name.includes(value));
        });

    });

});

$(document).ready(function (){

    // $('#champ_filtre').on("keyup", function(){
    //     let value = $(this).val().toLowerCase();

    //     $(".indicator-card").each(function () {
    //         let name = $(this).data("name");

    //         $(this).toggle(name.includes(value));
    //     });

    // });

    function applyFilter(){
        let champ_filtre = $("#champ_filtre").val().toLowerCase();
        let filterType = $('#filterType').val();

        $(".indicator-card").each(function () {
            let fieldValue = $(this).data(filterType);

            if(!fieldValue){
                $(this).hide();
                return;
            }

            $(this).toggle(fieldValue.includes(champ_filtre));
        });    
    }

    $('#champ_filtre').on("keyup", applyFilter);
    $('#filterType').on("change", applyFilter);

});

/////-------DELETE UN INVESTISSEUR ---------/////
$(document).ready(function () {
    $(".delete-btn").on("click", function (e){
        e.stopPropagation();

        let card = $(this).closest(".indicator-card");
        let id = card.find(".option-btn").data("id");
        let name = card.find(".option-btn").data("name");

        //injection dans le popoever
        $("#delete").data("id", id);
        $("#popoverItemName").text(name);

        //console.log("id envoye au popover :", id); 
    });

    $("#delete_element").on("click", function(){
        let id = $("#delete").data("id").toLowerCase().toString();

        $.ajax({
            type: "POST",
            url: "delete_investisseur/",
            header:{
                'X-CSRFToken': getCSRFToken()
            },
            data:{
                id : id,
                csrfmiddlewaretoken: getCSRFToken()
            },
            success: function(response) {
                console.log("Element supprimer avec succès !!!"+response);
            },
            error: function (response) { console.log('Erreur AJAX !!!'+response);}

        }).done(function(){
            console.log(" Supprimer avec succès !");
            window.location.reload();
        });

        //console.log("Supprion de l ID : ", (typeof id));
    });
});

////-------  CONTROLE DE FORMULAIR ---------//////

function connxVald(e){
    e.preventDefault();//on bloque au depart

    let valid = true;

    let nom = $("#name").val().trim();
    let email = $("#email").val().trim();

    if (nom === "" ){
        valid = false;
        $("#bordure").addClass("border-red-600");
        $("#name").addClass("border-red-600").next(".error").removeClass("hidden");
    }
    else{
        $("#bordure").removeClass("border-red-600");
        $("#name").removeClass("border-red-600").next(".error").addClass("hidden");
    }

    if(email === ""){
        valid = false;
        $("#bordure").addClass("border-red-600");
        $("#email").addClass("border-red-600").next(".error").removeClass("hidden");
    }
    else{
        $("#bordure").removeClass("border-red-600");
        $("#email").removeClass("border-red-600").next(".error").addClass("hidden");
    }

    if(valid){
        this.submit();
    }
}

function netoiyage(){
    $(this).removeClass("border-red-600").next(".error").addClass("hidden");
    $("#bordure").removeClass("border-red-600");
}

$(document).ready(function () {

    $("#connexionForm").on("submit", connxVald);

    $('#name').on("input", netoiyage);
    $('#email').on("input", netoiyage);
    
    /////----------\\\\\\

    $("#inscripForm").on("submit", function (e){
        ///
        e.preventDefault();//on bloque au depart
        
        let valid = true;

        let nom = $("#nom_ins").val().trim();
        let postNom = $("#postNom").val().trim();
        let prenom = $("#prenom").val().trim();
        let email = $("#email_ins").val().trim();

        if(nom === ""){
            valid = false;
            $("#nom_ins").addClass("border-red-600").next(".error").removeClass("hidden");
        }else{
            $("#nom_ins").removeClass("border-red-600").next(".error").addClass("hidden");
        }
        if(postNom === ""){
            valid = false;
            $("#postNom").addClass("border-red-600").next(".error").removeClass("hidden");
        }else{
           $("#postNom").removeClass("border-red-600").next(".error").addClass("hidden");
        }
        if(prenom === ""){
            valid = false;
            $("#prenom").addClass("border-red-600").next(".error").removeClass("hidden");
        }else{
           $("#prenom").removeClass("border-red-600").next(".error").addClass("hidden");
        }
        if(email === ""){
            valid = false;
            $("#email_ins").addClass("border-red-600").next(".error").removeClass("hidden");
        }else{
           $("#email_ins").removeClass("border-red-600").next(".error").addClass("hidden");
        }

        if(valid){this.submit();}
    });

    $('#nom_ins').on("input", netoiyage);
    $('#postNom').on("input", netoiyage);
    $('#prenom').on("input", netoiyage);
    $('#email_ins').on("input", netoiyage);

});

//INVESTISSEUR FORM
function netoiyage2(){
    $(this).removeClass("border-red-600").next(".error").addClass("hidden");
    $("#bordureIvt2").removeClass("border-red-600");
    $("#bordureIvt3").removeClass("border-red-600");
    $("#bordureIvt4").removeClass("border-red-600");
    $("#bordureIvt5").removeClass("border-red-600");
    $("#bordureIvt6").removeClass("border-red-600");
}

$(document).ready(function () {
    //INVESTISSEUR FORM

    $("#investisseurForm").on("submit", function (e){
        e.preventDefault();//on bloque au depart

        let valid = true;

        let evenement = $("#evenement").val();

        let nom = $("#nom_comp").val().trim();
        let qualif = $("#qualif").val().trim();
        let email_invst = $("#email_invst").val().trim();
        let phone = $("#phone").val().trim();
        let pays = $("#pays").val().trim();

        if(nom === ""){
            valid = false;
            $("#bordureIvt2").addClass("border-red-600");
            $("#nom_comp").addClass("border-red-600").next(".error").removeClass("hidden");
        }else{
            $("#bordureIvt2").removeClass("border-red-600");
            $("#nom_comp").removeClass("border-red-600").next(".error").addClass("hidden");
        }
        if(qualif === ""){
            valid = false;
            $("#bordureIvt3").addClass("border-red-600");
            $("#qualif").addClass("border-red-600").next(".error").removeClass("hidden");
        }else{
            $("#bordureIvt3").removeClass("border-red-600");
            $("#qualif").removeClass("border-red-600").next(".error").addClass("hidden");
        }
        if(email_invst === ""){
            valid = false;
            $("#bordureIvt4").addClass("border-red-600");
            $("#email_invst").addClass("border-red-600").next(".error").removeClass("hidden");
        }else{
            $("#bordureIvt4").removeClass("border-red-600");
            $("#email_invst").removeClass("border-red-600").next(".error").addClass("hidden");
        }
        if(phone === ""){
            valid = false;
            $("#bordureIvt5").addClass("border-red-600");
            $("#phone").addClass("border-red-600").next(".error").removeClass("hidden");
        }else{
            $("#bordureIvt5").removeClass("border-red-600");
            $("#phone").removeClass("border-red-600").next(".error").addClass("hidden");
        }
        if(pays === ""){
            valid = false;
            $("#bordureIvt6").addClass("border-red-600");
            $("#pays").addClass("border-red-600").next(".error").removeClass("hidden");
        }else{
            $("#bordureIvt6").removeClass("border-red-600");
            $("#pays").removeClass("border-red-600").next(".error").addClass("hidden");
        }

        if(!evenement){
            //valid = false;
            $("#bordureIvt1").addClass("border-red-600");
            $("#evenement").addClass("border-red-600").next(".error").removeClass("hidden");
            return;
        }else{
           // $("#bordureIvt1").removeClass("border-red-600");
            $("#evenement").removeClass("border-red-600").next(".error").addClass("hidden");
        }
    
        if(valid){
            this.submit();
        }
    });

    $("#evenement").on("change", function(){
        $(this).removeClass("border-red-600").next(".error").addClass("hidden");
        $("#bordureIvt1").removeClass("border-red-600");
    });

    $('#nom_comp').on("input", netoiyage2);
    $('#qualif').on("input", netoiyage2);
    $('#email_invst').on("input", netoiyage2);
    $('#phone').on("input", netoiyage2);
    $('#pays').on("input", netoiyage2);
    
});

////INVESTISSEMNT \\\\

function netoiyage3(){
    $(this).removeClass("border-red-600").next(".error").addClass("hidden");
    $("#bordureIvss1").removeClass("border-red-600");
    $("#bordureIvss2").removeClass("border-red-600");
    
}

$(document).ready(function () {
    $("#investissementForm").on("submit", function (e){
        e.preventDefault();//on bloque au depart

        let valid = true;

        let objet = $("#objet").val().trim();
        let secteur = $("#secteur").val().trim();
        let statut = $("#statut").val();

        if(objet === ""){
            valid = false;
            $("#objet").addClass("border-red-600").next(".error").removeClass("hidden");
            $("#bordureIvss1").addClass("border-red-600");
        }
        else{
            $("#objet").removeClass("border-red-600").next(".error").addClass("hidden");
        }
        if(secteur === ""){
            valid = false;
            $("#secteur").addClass("border-red-600").next(".error").removeClass("hidden");
            $("#bordureIvss2").addClass("border-red-600");
        }else{
            $("#secteur").removeClass("border-red-600").next(".error").addClass("hidden");
        }

        if(!statut){
            $("#statut").addClass("border-red-600").next(".error").removeClass("hidden");
            $("#bordureIvss3").addClass("border-red-600");
        }else{
            $("#statut").removeClass("border-red-600").next(".error").addClass("hidden");
        }

        if(valid){
            this.submit();
        }

    });

    $('#objet').on("input", netoiyage3);
    $('#secteur').on("input", netoiyage3);

    $("#statut").on("change", function(){
        $(this).removeClass("border-red-600").next(".error").addClass("hidden");
        $("#bordureIvss3").removeClass("border-red-600");
    });

});

$(document).ready(function () {

});