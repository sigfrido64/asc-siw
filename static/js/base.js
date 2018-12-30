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

  comboAnnoFormativo.jqxComboBox({placeHolder: 'Anno Formativo', source: dataAdapter_af,
    displayMember: "anno_formativo", valueMember: "pk"});

  comboAnnoFormativo.on('bindingComplete', function (event) {
    comboAnnoFormativo.val(af_val);
  });

  comboAnnoFormativo.on('change', function (event) {
    let args = event.args;
    if (args) {
      // index represents the item's index.
      let item = args.item;
      // get item's label and value.
      let label = item.label;
      $.ajax({
          url: set_af_url,
          data: {
            'anno_formativo': label
          }
      });
    }
  });
});