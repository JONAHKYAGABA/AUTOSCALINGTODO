import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import Task

import xmlrunner
import os


class TaskModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='This is a test task.',
            complete=False,
            due=datetime.now() + timedelta(days=2),
            time=datetime.now().time()
        )

    def test_task_creation(self):
        task = self.task
        self.assertTrue(isinstance(task, Task))
        self.assertEqual(task.__str__(), task.title)

    def test_task_completed(self):
        task = self.task
        self.assertFalse(task.complete)
        task.complete = True
        task.save()
        self.assertTrue(task.complete)

    def test_task_due_date(self):
        task = self.task
        self.assertIsNotNone(task.due)
        self.assertLess(datetime.now(), task.due)

    def test_task_time(self):
        task = self.task
        self.assertIsNotNone(task.time)

class TaskTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            email='testuser@example.com', 
            password='testpass'
        )
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='This is a test task.',
            complete=False,
            due='2023-12-31',
            time='12:00'
        )
    
    def test_task_list_view(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task List')
        self.assertQuerysetEqual(response.context['tasks'], [repr(self.task)])

    def test_task_detail_view(self):
        response = self.client.get(reverse('task_detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_create_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('task_create'), {
            'title': 'New Test Task',
            'description': 'This is a new test task.',
            'complete': False,
            'due': '2023-12-31',
            'time': '12:00'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 2)

    def test_task_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('task_update', args=[self.task.pk]), {
            'title': 'Updated Test Task',
            'description': 'This is an updated test task.',
            'complete': True,
            'due': '2024-01-31',
            'time': '14:00'
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Test Task')
        self.assertEqual(self.task.complete, True)

    def test_task_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)

    def test_register_page_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_custom_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')
if __name__ == '__main__':
     # Set the path where the XML report will be stored
     path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test-results.xml')
     # Run the tests with the xmlrunner package and output the results to the XML file
     unittest.main(
         testRunner=xmlrunner.XMLTestRunner(output=path),
         failfast=False,
         buffer=False,
         catchbreak=False
     )
