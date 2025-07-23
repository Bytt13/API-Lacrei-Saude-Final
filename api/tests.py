import uuid
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Profissional, Consulta
from django.utils import timezone


class ProfissionalTests(APITestCase):
    # Config inicial para todos os metodos da classe
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.profissional_data = {
            "nome_social": "Dr. James",
            "profissao": "oncologista",
            "endereco": "Rua do james, 123",
            "contato": "987654321",
        }
        self.profissional = Profissional.objects.create(**self.profissional_data)

    def test_criar_profissional(self):
        url = reverse("profissional-list")
        data = {
            "nome_social": "Dr. House",
            "profissao": "infectologista",
            "endereco": "Rua do house, 123",
            "contato": "123456789",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profissional.objects.count(), 2)

    def test_list_profissionais(self):
        url = reverse("profissional-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_profissional(self):
        url = reverse("profissional-detail", kwargs={"pk": self.profissional.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nome_social"], self.profissional.nome_social)

    def test_update_profissional(self):
        url = reverse("profissional-detail", kwargs={"pk": self.profissional.pk})
        updated_data = {
            "nome_social": "Dr. House",
            "profissao": "nefrologista",
            "endereco": "Rua do house, 123",
            "contato": "111111111",
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profissional.refresh_from_db()
        self.assertEqual(self.profissional.profissao, "nefrologista")

    def test_delete_profissional(self):
        url = reverse("profissional-detail", kwargs={"pk": self.profissional.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Profissional.objects.count(), 0)

    def test_create_profissional_missing_data(self):
        url = reverse("profissional-list")
        invalid_data = {"nome_social": "Dr.Fantasma"}
        response = self.client.post(url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_non_existent_profissional(self):
        fake_uuid = uuid.uuid4()
        url = reverse("profissional-detail", kwargs={"pk": fake_uuid})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ConsultaTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser2", password="testpassword123"
        )
        self.client.force_authenticate(user=self.user)
        self.profissional = Profissional.objects.create(
            nome_social="Dra. Lisa Cuddy",
            profissao="Administradora",
            endereco="Hospital Plainsboro",
            contato="555",
        )
        self.consulta = Consulta.objects.create(
            profissional=self.profissional, data_consulta=timezone.now()
        )

    def test_criar_consulta(self):
        url = reverse("consulta-list")
        data = {'profissional': str(self.profissional.pk), 'data_consulta': (timezone.now() + timezone.timedelta(days=1)).isoformat()}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Consulta.objects.count(), 2)

    def test_list_conultas(self):
        url = reverse("consulta-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_consulta(self):
        url = reverse("consulta-detail", kwargs={"pk": self.consulta.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['profissional']), str(self.profissional.pk))

    def test_update_consulta(self):
        url = reverse("consulta-detail", kwargs={"pk": self.consulta.pk})
        nova_data = (timezone.now() + timezone.timedelta(days=5))
        updated_data = {
            'profissional': str(self.profissional.pk), 'data_consulta': nova_data.isoformat()
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.consulta.refresh_from_db()
        self.assertEqual(self.consulta.data_consulta.strftime('%Y-%m-%d %H:%M:%S'), nova_data.strftime('%Y-%m-%d %H:%M:%S'))

    def test_delete_consulta(self):
        url = reverse("consulta-detail", kwargs={"pk": self.consulta.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Consulta.objects.count(), 0)

    def test_get_consultas_por_profissional(self):
        outro_profissional = Profissional.objects.create(
            nome_social="Dra. Lisa Lisa",
            profissao="Recepcionista",
            endereco="Hospital Plainsboro",
            contato="777",
        )
        Consulta.objects.create(
            profissional=outro_profissional, data_consulta=timezone.now()
        )
        base_url = reverse("consulta-list")
        url = f"{base_url}?profissional_id={self.profissional.pk}"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            str(response.data[0]["profissional"]), str(self.profissional.pk)
        )

    def test_create_consulta_invalid_profissional(self):
        url = reverse("consulta-list")
        fake_uuid = uuid.uuid4()
        data = {
            "profissional": str(fake_uuid),
            "data_consulta": timezone.now().isoformat(),
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
