$(document).ready(function () {
  let comboAnnoFormativo = $("#id_anno_formativo");
  let load_af_url = comboAnnoFormativo.attr("load-af-url");
  let set_af_url = comboAnnoFormativo.attr("set-af-url");
  let af_val = comboAnnoFormativo.attr("af");

          let source_af = {
             datatype: "json",
             datafields: [
                 {name: 'pk'},
                 {name: 'anno_formativo'}
             ],
             url: load_af_url
          };
          let dataAdapter_af = new $.jqx.dataAdapter(source_af);

          $("#id_anno_formativo").jqxComboBox({placeHolder: 'Anno Formativo', source: dataAdapter_af,
            displayMember: "anno_formativo", valueMember: "pk"});
          $("#id_anno_formativo").on('bindingComplete', function (event) {
            $("#id_anno_formativo").val(af_val);
            });
          $("#id_anno_formativo").on('change', function (event)
           {
              var args = event.args;
              if (args) {
              // index represents the item's index.
              var index = args.index;
              var item = args.item;
              // get item's label and value.
              var label = item.label;
              var value = item.value;
              var type = args.type; // keyboard, mouse or null depending on how the item was selected.

              $.ajax({                       // Inizializza la richiesta AJAX
                  url: set_af_url,                    // Imposta l'url della richiesta (= localhost:8000/attesta/ajax/load-corsi/)
                  data: {
                    'anno_formativo': label
                  }
              });
           }
           });
});