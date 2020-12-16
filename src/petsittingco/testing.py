from unittest import TestCase
import requests

class Owner_Dash_Test(TestCase):

    def test_pet_create(self):
        r = requests.get("http://aiji.cs.loyola.edu/petownerdashboard/pet_forms.html?")
        check_status_code = r.status_code
        assert check_status_code < 400

    def test_job_create(self):
        r = requests.get("http://aiji.cs.loyola.edu/petownerdashboard/createjob.html?")
        check_status_code = r.status_code
        assert check_status_code < 400

    def test_modify_pet(self):
        r = requests.get("http://aiji.cs.loyola.edu/petownerdashboard/change_pet.html?pet_id=468fe121-7a50-4d50-b553-0471d7a1cb28")
        check_status_code = r.status_code
        assert check_status_code < 400

    def test_delete_pet(self):
        r = requests.get("http://aiji.cs.loyola.edu/petownerdashboard/delete.html?pet_id=83d52f98-df81-4e44-97f2-2b2b78eef915")
        check_status_code = r.status_code
        assert check_status_code < 400 

    def test_job_list(self):
        r = requests.get("http://aiji.cs.loyola.edu/petownerdashboard/jobs.html")
        check_status_code = r.status_code
        assert check_status_code < 400

class Sitter_Dash_Test(TestCase):

    def test_accept_job(self):
        r = requests.get("http://aiji.cs.loyola.edu/petsitterdashboard/accept.html?job_id=37ac2dc7-1134-4656-9a75-2c2222f8e598")
        check_status_code = r.status_code
        assert check_status_code < 400

    def test_accepted_list(self):
        r = requests.get("http://aiji.cs.loyola.edu/petsitterdashboard/acceptedjobs.html?")
        check_status_code = r.status_code
        assert check_status_code < 400

class Main_Dash_Test(TestCase):

    def test_sign_in(self):
        r = requests.get("http://aiji.cs.loyola.edu/signin.html")
        check_status_code = r.status_code
        assert check_status_code < 400

    def test_sign_up(self):
        r = requests.get("http://aiji.cs.loyola.edu/signup.html")
        check_status_code = r.status_code
        assert check_status_code < 400

    def test_logout(self):
        r = requests.get("http://aiji.cs.loyola.edu/logout.html")
        check_status_code = r.status_code
        assert check_status_code < 400

class Shelter_Dash_Test(TestCase):

    def test_shelter_dash(self):
        r = requests.get("http://aiji.cs.loyola.edu/shelter/shelteraccview/")
        check_status_code = r.status_code
        assert check_status_code < 400
    
class Admin_Dash_Test(TestCase):

    def test_admin_account(self):
        r = requests.get("http://aiji.cs.loyola.edu/admin/account/")
        check_status_code = r.status_code
        assert check_status_code < 400

    def test_admin_pet(self):
        r = requests.get("http://aiji.cs.loyola.edu/admin/pet/")
        check_status_code = r.status_code
        assert check_status_code < 400

    def test_admin_job(self):
        r = requests.get("http://aiji.cs.loyola.edu/admin/job/")
        check_status_code = r.status_code
        assert check_status_code < 400

    def test_admin_modify_account(self):
        r = requests.get("http://aiji.cs.loyola.edu/admin/account/edit/?id=338eec95-44ab-4b35-a343-2f089b47dcf1&url=%2Fadmin%2Faccount%2F%3Fsearch%3DHannah")
        check_status_code = r.status_code
        assert check_status_code < 400
    
    def test_admin_create_account(self):
        r= requests.get("http://aiji.cs.loyola.edu/admin/account/new/?url=%2Fadmin%2Faccount%2F%3Fsearch%3DHannah")
        check_status_code = r.status_code
        assert check_status_code < 400

    def test_admin_modify_job(self):
        r = requests.get("http://aiji.cs.loyola.edu/admin/job/edit/?id=f05f7a48-41c7-45a4-94e4-2631020f30b1&url=%2Fadmin%2Fjob%2F")
        check_status_code = r.status_code
        assert check_status_code < 400

    def test_admin_modify_pet(self):
        r = requests.get("http://aiji.cs.loyola.edu/admin/pet/edit/?id=8c4cb78d-7efa-43b4-b1fa-25056e430e01&url=%2Fadmin%2Fpet%2F")
        check_status_code = r.status_code
        assert check_status_code < 400

    def test_admin_create_job(self):
        r = requests.get("http://aiji.cs.loyola.edu/admin/job/new/?url=%2Fadmin%2Fjob%2F")
        check_status_code = r.status_code
        assert check_status_code < 400
    
    def test_admin_create_pet(self):
        r = requests.get("http://aiji.cs.loyola.edu/admin/pet/new/?url=%2Fadmin%2Fpet%2F")
        check_status_code = r.status_code
        assert check_status_code < 400