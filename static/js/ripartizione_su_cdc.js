var prima, adesso;

function rinfresca_ripartizioni_su_cdc(){
  let div_handle = $("#id_lista_cdc_ripartizioni");
  let url = div_handle.attr("href");  // recupera l'url
  $.ajax({
    url: url,
    success: function (data) {
      div_handle.html(data.html);
    }
  });
}

function show_cdc_treeview(){
  let cdc_window = $('#choose_cdc_window');
  cdc_window.jqxWindow({ width: '80%', height: '80%', resizable: false, position: 'center', isModal: true,
    initContent : init_cdc_treeview(), title: 'Scegli Centro di Costo'
  });

  $("#button_cdc_select").jqxButton({ width: '200', height: '30', template: "success", value: "Conferma Selezione"});
  $("#button_cdc_select").on('click', function () {
    cdc_window.jqxWindow('close');
  });
  cdc_window.jqxWindow('open');
}

function init_cdc_treeview() {
  let treeView = $("#jqxTreeView");
  let cdcUrl = treeView.attr("lista-cdc-url");
  let source = {datatype: "json", datafields: [{name: 'parent'}, {name: 'nome'}, {name: 'id'}],
                url: cdcUrl, async: true };
  let dataAdapter = new $.jqx.dataAdapter(source,
    {loadComplete: function () {
         let records = dataAdapter.getRecordsHierarchy('id', 'parent', 'items', [{name: 'nome', map: 'label'}]);
         treeView.jqxTree({source: records, width: '300px'})
    }
  });
  dataAdapter.dataBind();
  treeView.on('itemClick', function(event) {setta_risultato_treeview_nel_form(event)});
}

function setta_risultato_treeview_nel_form (event) {
  // Setto la scelta nel form principale e se doppio click chiudo in quanto considero terminata la scelta.
  let args = event.args;
  let item = $('#jqxTreeView').jqxTree('getItem', args.element);
  $("#id_cdc_txt").val(item.label);
  $("#id_cdc").val(item.id);
  adesso = new Date();
  let diff = adesso - prima;
  if (diff < 500) { $('#choose_cdc_window').jqxWindow('close'); }
  prima = adesso;
}

$(document).ready(function () {
  $("#button_ripartizione_su_cdc_save").jqxButton({ width: '200', height: '30', template: "success"});

  $("#choose_cdc").jqxButton({ width: '100', height: '30', template: "success"});
  $("#choose_cdc").on('click', function () {show_cdc_treeview();});

  rinfresca_ripartizioni_su_cdc();
  prima = 1000;
});