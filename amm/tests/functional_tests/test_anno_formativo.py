# coding=utf-8
__author__ = "Pilone Ing. Sigfrido"
from accounts.models import User, SiwPermessi
from functional_tests.base import FunctionalTest


class LoginTest(FunctionalTest):
    # Crea l'utente per le prove.
    fixtures = ['af.json']
    
    def setUp(self):
        super().setUp()
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.user.profile.permessi = {SiwPermessi.AMM_CDC_READ, SiwPermessi.MENU_AMM, SiwPermessi.MENU_AMM_CDC}
        self.user.save(force_update=True)
        # Login
        self.siw_do_login()

    def test_af_on_page(self):
        self.wait_for_ajax()
        # Guarda se trova la stringa che corrisponde al controllo del combo-box e con valore di default AF 2018-2019
        anno_formativo = self.browser.execute_script("return $('#id_anno_formativo').jqxComboBox('val')")
        self.assertEqual(anno_formativo, 'AF 2018-2019')
        
        # Adesso scelgo un altro anno formativo
        self.browser.execute_script("$('#id_anno_formativo').jqxComboBox('selectIndex', 1);")
        self.wait_for_ajax()
    
        # Riapro la pagina home.
        self.browser.get(self.live_server_url)
        self.wait_for_ajax()

        # E rifaccio la domanda.
        # E ci dovrei trovare il valore che ho scelto prima.
        anno_formativo = self.browser.execute_script("return $('#id_anno_formativo').jqxComboBox('val')")
        self.assertEqual(anno_formativo, 'AF 2017-2018')
